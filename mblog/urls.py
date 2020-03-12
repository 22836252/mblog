"""mblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from mainsite.views import homepage, showpost,category,register,registerinfo,loginCheck,login,logOut,about,listing,disp_detail,aboutpage,company,info,sales,contact,post,post2,testpage,showlisting,shoppingcart,addtocart,removefromcart,updatecartqty,checkout,POST_crawl,main
from django.urls import reverse


from django.conf.urls import include

my_patterns = [
    path('company/', company),
    path('sales/', sales),
    path('contact/', contact),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', homepage),
    path('', homepage),
    path('products/<slug:slug>/', showpost),
    path('register.html', register),
    path('login.html', login),
    path('logOut.html', logOut),
    
    path('category.html', category),
    path('registerinfo/', registerinfo),  
    path('loginCheck/', loginCheck), #POST傳送表單
    path('about/', about),
    path('list/', listing),
    path('list/<sku>/', disp_detail),
    path('aboutpage/<int:author_no>', aboutpage),
    path('aboutpage/', aboutpage),
    path('info/', include(my_patterns)),
    path('cart/', shoppingcart),
    path('addtocart/', addtocart),
    path('removefromcart/', removefromcart),
    # path('updatecartqty/', updatecartqty),
     path('checkout/', checkout),
    
    path('updatecartqty/<int:sku>',updatecartqty),   
    path('testpage/', testpage),  
    path('showlist/<int:yr>/<int:mon>/<int:day>/', showlisting),
    path('post/<int:yr>/<int:mon>/<int:day>/<int:post_num>/', post, name='post-url'),
 
    path('post2/<int:yr>/<int:mon>/<int:day>/<int:post_num>/', post2, name='post-url2'),
    path('crawlpage',main),   
    path('showlist/<int:yr>/<int:mon>/<int:day>/',showlisting, name='list-url'),
    path('POST_crawl/',POST_crawl) #在POST_crawl頁面執行POST_crawl函式
   
]
