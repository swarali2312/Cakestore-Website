from django.urls import path
from cakeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[ 
    path('cake',views.cake),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('cakedetail/<cid>',views.cakedetail),
    path('catfilter/<cv>',views.catfilter),
    path('placeorder',views.placeorder),
    path('addtocart/<cid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('updateqty/<x>/<cartid>',views.updateqty),
    path('remove/<cartid>',views.remove),
    path('fetchorder',views.fetchorder),
    path('search',views.search),
    path('sort/<sv>',views.sortbyprice),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('about',views.about),
    path('contact',views.contact),
]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)