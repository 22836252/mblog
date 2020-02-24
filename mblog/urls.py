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
from mainsite.views import homepage, showpost,category,register,registerinfo,loginCheck,login,about,listing,disp_detail,aboutpage,company,info,sales,contact,post,post2,testpage,showlisting
from django.urls import reverse


from django.conf.urls import include

my_patterns = [
    path('company/', company),
    path('sales/', sales),
    path('contact/', contact),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('products/<slug:slug>/', showpost),
    path('register.html', register),
    path('login.html', login),
    path('category.html', category),
    path('registerinfo/', registerinfo),  
    path('loginCheck/', loginCheck), #POST傳送表單
    path('about/', about),
    path('list/', listing),
    path('list/<sku>/', disp_detail),
    path('aboutpage/<int:author_no>', aboutpage),
    path('aboutpage/', aboutpage),
    path('info/', include(my_patterns)),

    path('testpage/', testpage),  
    path('showlist/<int:yr>/<int:mon>/<int:day>/', showlisting),
    path('post/<int:yr>/<int:mon>/<int:day>/<int:post_num>/', post, name='post-url'),

    path('post2/<int:yr>/<int:mon>/<int:day>/<int:post_num>/', post2, name='post-url2'),

    path('showlist/<int:yr>/<int:mon>/<int:day>/',showlisting, name='list-url'),

    # path('post1/',views.post1),  #資料新增，資料不驗證
    # path('post2/',views.post2),  #資料新增，資料作驗證

    # re_path(r'delete/(\d+)/$',views.delete),

    # re_path(r'edit/(\d+)/$',views.edit),
    # re_path(r'edit/(\d+)/(\w+)$',views.edit),  #由 瀏覽器開啟
    # re_path(r'edit2/(\d+)/(\w+)$',views.edit2),

    # path('postform',views.postform),    #表單驗證
]
