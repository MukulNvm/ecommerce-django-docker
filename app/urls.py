from django.urls import path
from app import views
# views provide LoginView and Logout View
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from .context_processors import cart_total

urlpatterns = [
    # path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    # to current cart quantity
    path('updatedcart/',views.updatedcart,name="updatedcart"),
    path('search/', views.search_product, name='search_product'),

    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobiledata/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop_view, name='laptop'),
    path('laptopata/<slug:data>/', views.laptop_view, name='laptopdata'),
    path('topwear/', views.topwear_view, name='topwear'),
    path('topweardata/<slug:data>/', views.topwear_view, name='topweardata'),
    path('bottomwear/', views.bottom_view, name='bottomwear'),
    path('bottomweardata/<slug:data>/', views.bottom_view, name='bottomweardata'),



    # no extra class for login
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordChangeDone.html'),name="passwordchangedone"),

    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', email_template_name='app/password_reset_email.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
 
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
  
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
]
