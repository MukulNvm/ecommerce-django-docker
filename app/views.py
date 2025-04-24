from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum,F
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from fuzzywuzzy import process  # Import fuzzy matching library


# home view
class ProductView(View):
 def get(self,request):
  totalitem=0
  if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print("here total item is: ",totalitem)
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  return render(request, 'app/home.html',{'bottomwears':bottomwears,'topwears':topwears,'mobiles':mobiles,'totalitems':totalitem})
 

# @method_decorator(login_required,name="dispatch")
class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
      item_already_in_cart = Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
          user=request.user
          #comming from form of product_detail
          product_id = request.GET.get('prod_id')
          print(product_id)
          product=Product.objects.get(id=product_id)
          Cart(user=user,product=product).save()
          return redirect('/cart')

@login_required
def show_cart(request):
    user= request.user
    carts = Cart.objects.filter(user=user)
    # return queryset
    print(carts)
    amount=0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    # cart_product=[p for p in Cart.objects.filter(user=request.user) if request.user==user]
    # return list
    print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity * p.product.discounted_price)
        amount+=tempamount;
        total_amount=amount + shipping_amount
    print("Total amount",amount,total_amount)
    return render(request,'app/addtocart.html',{'carts':carts,'totalamount':total_amount,'amount':amount})

@login_required
def plus_cart(request):
  if request.method=="GET":
      prod_id= request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
      c.quantity+=1
      c.save()
      # to amount
      amount=0.0
      shipping_amount=70.0
      user=request.user
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
       for p in cart_product:
        tempamount=(p.quantity * p.product.discounted_price)
        amount+=tempamount;
      else:
        print("Not product id get") 
      data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount+shipping_amount
      }   
      return JsonResponse(data)

@login_required
def minus_cart(request):
  if request.method=="GET":
      prod_id= request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
      c.quantity-=1
      c.save()
      # to amount
      amount=0.0
      shipping_amount=70.0
      user=request.user
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
       for p in cart_product:
        tempamount=(p.quantity * p.product.discounted_price)
        amount+=tempamount;
      else:
        print("Not product id get") 
      data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount+shipping_amount
      }   
      return JsonResponse(data)

@login_required  
def remove_cart(request):
  if request.method=="GET":
      prod_id= request.GET['prod_id']
      c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
      c.delete()
      # to amount
      amount=0.0
      shipping_amount=70.0
      user=request.user
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
       for p in cart_product:
        tempamount=(p.quantity * p.product.discounted_price)
        amount+=tempamount;
      else:
        print("Not product id get") 
      data={
        'amount':amount,
        'totalamount':amount+shipping_amount
      }   
      return JsonResponse(data)

@login_required
def checkout(request):
 user=request.user
 address=Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user) 
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
  for p in cart_product:
          tempamount=(p.quantity * p.product.discounted_price)
          amount+=tempamount
  totalamount=amount+shipping_amount        
 return render(request, 'app/checkout.html',{'totalamount':totalamount,'address':address,'cart_items':cart_items})

# after checkout -> payment is happening
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')

    if not custid:
        messages.error(request, "Please select a valid shipping address before proceeding with payment.")
        return redirect("checkout")

    try:
        customer = Customer.objects.get(id=custid, user=user)
    except Customer.DoesNotExist:
        messages.error(request, "Selected address does not exist.")
        return redirect("checkout")

    cart = Cart.objects.filter(user=user)

    if not cart.exists():
        messages.error(request, "Your cart is empty. Add products before making a payment.")
        return redirect("cart")

    print("my cart is ", cart)

    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity
        )
        c.delete()  # Remove item from cart after order is placed

    messages.success(request, "Payment successful! Your order has been placed.")
    return redirect("orders")  # Redirect to the orders page  

@login_required
def orders(request):
      op = OrderPlaced.objects.filter(user=request.user)
      print(op)
      return render(request, 'app/orders.html',{'order_placed':op})



def buy_now(request):      
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 print("Address: ",add)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})



def mobile(request,data="None"):
  if data == 'None':
     mobiles = Product.objects.filter(category='M')
  elif data=="Redmi" or data == 'Samsung':
    mobiles = Product.objects.filter(category='M').filter(brand=data)   
  elif data=='below':
     mobiles=Product.objects.filter(category='M').filter(discounted_price__lt = 10000)  
  elif data=='above':
     mobiles=Product.objects.filter(category='M').filter(discounted_price__gt = 10000)  
  return render(request, 'app/mobile.html',{'mobiles':mobiles})


def laptop_view(request,data="None"):
      if data == 'None':
         laptops=Product.objects.filter(category='L')
      elif data == 'HP' or data=='Apple' or data == 'Dell' or data =='Lenovo':
         laptops=Product.objects.filter(category='L').filter(brand=data)   
      elif data=='below':
         laptops=Product.objects.filter(category='L').filter(discounted_price__lt = 40000)  
      elif data == 'above':
         laptops = Product.objects.filter(category='L').filter(discounted_price__gt = 40000)   
      return render(request, 'app/laptops.html',{'laptops':laptops})

def topwear_view(request, data="None"):
    if data == 'None':
        topwear = Product.objects.filter(category='TW')  # Assuming 'TW' represents Top Wears
    elif data in ['Nike', 'Adidas', 'Puma', 'Reebok']:  # Add more brands if needed
        topwear = Product.objects.filter(category='TW', brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='TW', discounted_price__lt=1000)  # Adjust price range as needed
    elif data == 'above':
        topwear = Product.objects.filter(category='TW', discounted_price__gt=1000)
    
    return render(request, 'app/topwear.html', {'topwear': topwear})

def bottom_view(request, data="None"):
    if data == 'None':
        bottomwear = Product.objects.filter(category='BW')  # Assuming 'TW' represents Top Wears
    elif data in ['Nike', 'Adidas', 'Puma', 'Reebok']:  # Add more brands if needed
        bottomwear = Product.objects.filter(category='BW', brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW', discounted_price__lt=1000)  # Adjust price range as needed
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW', discounted_price__gt=1000)
    
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear})

   
   
   

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')  # ✅ Adding success message
            # return redirect('login')  
        else:
            messages.error(request, 'Please correct the errors below.')  # ✅ Adding error message if form is invalid

        return render(request, 'app/customerregistration.html', {'form': form})


@method_decorator(login_required,name="dispatch")
class ProfileView(View):
  def get(self,request):
    form= CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  def post(self,request):
    form=CustomerProfileForm(request.POST)  
    if form.is_valid():
      user=request.user
      print("my user is: ",user)
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      print("user id:",user.id)
      reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,"Congratulations!! Profile Updated Successfully")
      form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})  


def updatedcart(request):
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print("here total item is: ", totalitem)
    else:
        totalitem = 0
    
    data = {
        'totalitems': totalitem
    }

    print("Context being passed:", data)  # ✅ Debugging

    return JsonResponse(data)

def search_product(request):
    query = request.GET.get('product_item', '').strip()  # Get search input
    products = []  # Default empty list

    if query:
        all_products = Product.objects.all().values_list('title', flat=True)  # Get all product titles
        best_matches = process.extract(query, all_products, limit=10, scorer=process.fuzz.partial_ratio)  # Find best matches

        matching_titles = [match[0] for match in best_matches if match[1] > 50]  # Get titles with >50% similarity
        products = Product.objects.filter(title__in=matching_titles)  # Fetch matching products

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'app/search_results.html', context)