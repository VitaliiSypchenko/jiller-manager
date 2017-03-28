from django.conf.urls import include, url
from django.contrib import admin
from company import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_view, name='home'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
]


