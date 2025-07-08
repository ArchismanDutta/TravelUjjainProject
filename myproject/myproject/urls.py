from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from myproject.myapp import views  # ✅ Corrected import
from myproject.myapp.views import aboutus_view  # ✅ Also correct if aboutus_view exists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('packages/', views.packages_view, name='packages'),
    path('cars/', views.cars_view, name='cars'),
    path('addons/', views.addons_view, name='addons'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('aboutus/', views.aboutus_view, name='aboutus'),  
    path('contact/', views.contact_view, name='contact'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
