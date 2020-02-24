from datetime import datetime
from mainsite import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import products
from .models import Account
from django.http import Http404
import random
from django.urls import reverse


# Create your views here.
def homepage(request):
    template = get_template('index.html')
    productslist = products.objects.all()
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)

def showpost(request, slug):
    template = get_template('products.html')
    try:
        productslist = products.objects.get(slug=slug)
        if productslist != None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return redirect('/')


def category(request):
    
    productslist = products.objects.all()  

    if 'name' in request.session:
        name = request.session['name']
    return render(request, 'category.html', locals())
    
    
    return render(request, 'category.html', locals())

def register(request):
    template = get_template('register.html')  
    productslist = products.objects.all()
    html = template.render(locals())
    return HttpResponse(html)

def login(request):
    template = get_template('login.html')  
    productslist = products.objects.all()
    html = template.render(locals())
    return HttpResponse(html)
@csrf_exempt
def registerinfo(request):  
    name = request.POST['name']
    password=request.POST['password']
    email=request.POST['email']
    try:
        checkAccount=models.Account.objects.get(email=email)

        if checkAccount!= None:
            mess = "帳號重複!"
        return render(request, 'register.html', locals())
    except:
       
        if request.method == "POST":       
        
            Account = models.Account.objects.create(name=name, password=password, email=email) 
            Account.save()         
            mess = "更新成功!"
            return render(request, 'index.html', locals())
        else:
            mess = "表單資料不齊全!"
        return render(request, 'register.html', locals())

@csrf_exempt
def loginCheck(request):  
    email=request.POST['email']
    password=request.POST['password']
    
    try:
        checkAccount=models.Account.objects.get(email=email, password=password)
    
        if checkAccount!= None:     
            name=checkAccount.name
            
            request.session['name'] = name
            return render(request, 'index.html', locals())
    except:
        mess = "帳號或是密碼輸入失敗!"
       
        return render(request, 'login.html', locals())


def about(request):
    quotes = ['今日事，今日畢',
    '要怎麼收穫，先那麼栽',
    '知識就是力量',
    '一個人的個性就是他的命運']
    quote = random.choice(quotes)
    return render(request, 'about.html', locals()) 


def listing(request):
    productslist = products.objects.all()
    return render(request, 'list.html', locals())

def disp_detail(request, sku):
    try:
        p = products.objects.get(sku=sku)
    except products.DoesNotExist:
        raise Http404('找不到指定的品項編號')
#return HttpResponse('找不到指定的品項編號')
#return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'disp.html', locals())

def aboutpage(request, author_no=0):
    author_no=1
    html = "<h2>Here is No:{}'s about page!</h2><hr>".format(author_no)
    return HttpResponse(html)

def company(request):

    return render(request, 'company.html', locals()) 

def sales(request):

    return render(request, 'sales.html', locals()) 
    
def contact(request):

    return render(request, 'contact.html', locals()) 

def info(request):

    return render(request, 'contact.html', locals()) 

def testpage(request):
    year = 2019
    month = 10
    day = 30
    postid=3
    html = "<a href='{}'>Show the Post</a>" \
    .format(reverse('post-url', args=(year, month, day, postid,)))
    return HttpResponse(html)

def showlisting(request, yr, mon, day):
    html = "<h2>List Date is {}/{}/{}</h2><hr>".format(yr, mon, day)
    return HttpResponse(html)    


def post(request, yr, mon, day, post_num):
    html = "<h2>{}/{}/{}:Post Number:{}</h2><hr>".format(yr, mon, day, post_num)
    return HttpResponse(html)

def post2(request, yr, mon, day, post_num):
 
    return render(request, 'post2.html', locals()) 


def shippingcart(request):

    try:
        if request!= None:  
            email=request.POST['email']
            product=request.POST['product']
        return render(request, 'shippingcart.html', locals())    
    except:
    
        return render(request, 'shippingcart.html', locals()) 