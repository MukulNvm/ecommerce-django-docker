from django.db.models import Sum
from .models import Cart
from django.http import JsonResponse

# it is a global developer
def cart_total(request):
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        print("here total item is: ", totalitem)
    else:
        totalitem = 0
    return {'totalitems': totalitem}
