from datetime import datetime
from mainsite import models
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import products
from .models import Account
# from .models import Cart
from django.db.models import Q
from django.http import Http404
import random
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Prefetch
from django.core.serializers import serialize
from django.views.decorators import csrf

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv



def link(request):
    import psycopg2
    conn = psycopg2.connect(database="shop", user="postgres", password="admin", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO ewrwe.product (name ) VALUES (\'" + "123"  +"\')") 
    conn.commit()


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
    
    if 'cartQty' in request.session:
        cartQty = request.session['cartQty']
        cartPrice = request.session['cartPrice']


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


def shoppingcart(request):
    name = request.session['name']
    email= request.session['email']
  
    sql = '''
             SELECT * from  mainsite_products a join mainsite_Cart b on a.name=b.productName join mainsite_Account c on b.email=c.email where c.email = %s group by a.name order by a.qty Limit 3  '''
        
       
            
    productslist = [a for a in products.objects.raw(sql,[email])]
    print(productslist) 

    productslistjson=serialize('json', productslist)
    return render(request, 'cart.html', locals()) 
    # except:
    #     print("更新失敗") 
    #     return render(request, 'cart.html', locals()) 
@csrf_exempt
def addtocart(request):  
    name = request.session['name']
    email= request.session['email']
    print(email)
    sku = request.POST['sku']
    
    checkAccount=models.Account.objects.get(email=email)    
    if checkAccount==None:
         return JsonResponse({'status':'fail','message':'請先登入'})
    
    if sku != None:
        productlists = products.objects.get(sku=sku)
        if productlists.qty<0:
           return JsonResponse({'status':'fail','message':'庫存數不夠'})
      
        try:
            listcheck=models.Cart.objects.get(productName=productlists.name, BuyerName=name)
            listcheck.qty=listcheck.qty+1
            listcheck.save()
            cartQty=0
            cartPrice=0
           
        except:
            create=models.Cart.objects.create(productName=productlists.name, productPrice=productlists.price, BuyerName=name,qty=1, email=email,productsku=sku)
            create.save()
            
             
        return JsonResponse({'status':'success','message':productlists.name+'已加入購物車'})

        
          
        
    else:
        return JsonResponse({'status':'fail','message':'沒庫存'})
    
    
    
    
@csrf_exempt
def removefromcart(request):  
    name = request.session['name']
    email= request.session['email']
    print(email)
    sku = request.POST['sku']
   
    checkAccount=models.Account.objects.get(email=email)     
    if sku != None: 
        Cart.objects.filter(productsku=sku, BuyerName=name).delete()    
        print("資料已刪除")
    return JsonResponse({'status':'success','message':Cart.productName+'資料已刪除'})

@csrf_exempt
def updatecartqty(request):  
    name = request.session['name']
    email= request.session['email']
    print(email)
    sku = request.POST['sku']
   
    checkAccount=models.Account.objects.get(email=email)     
    if sku != None: 
        GetCart=Cart.objects.filter(productsku=sku, BuyerName=name)    
        GetCart=GetCart.qty+1
        GetCart.save
        print("數量已增加")

    JsonResponse({'status':'success','message':productlists.name+'數量已增加'})
    return render(request, 'cart.html', locals())


@csrf_exempt
def checkout(request):
   
    name = request.session['name']
    email= request.session['email']
    checkAccount=models.Account.objects.get(email=email) 

    cart=models.Cart.objects.filter(email=email)
    
    for i in range(len(cart)):
        sku=request.POST['sku'+str(i+1)]
        qty=request.POST['qty'+str(i+1)]
        cartupdate=models.Cart.objects.get(productsku=sku, BuyerName=name)
        cartupdate.qty=qty
        cartupdate.save()

    return render(request, 'cart.html', locals())

@csrf_exempt
def loginCheck(request):  
    email=request.POST['email']
    password=request.POST['password']
    checkAccount=models.Account.objects.get(email=email) 

    cartQty=0
    cartPrice=0
    
    checkqty=models.Cart.objects.filter(BuyerName=checkAccount.name)
  
    for x in checkqty:
    
  
        cartPrice= x.price  +  cartPrice
        cartQty=  x.qty  +  cartQty
        productsku=checkqty[0].productsku

    productlists = products.objects.get(sku=productsku)  
    firstimage=productlists.image
    print(cartQty)
    print(cartPrice)
    print(productsku)
    request.session['cartQty'] = cartQty
    request.session['cartPrice'] = cartPrice
    request.session['firstimage'] = firstimage
    print(firstimage)
       
   
    try:
        checkAccount=models.Account.objects.get(email=email, password=password)
    
        if checkAccount!= None:     
            name=checkAccount.name
            
            request.session['name'] = name
            request.session['email'] = email
            return render(request, 'index.html', locals())

    except:
        mess = "帳號或是密碼輸入失敗!"
       
        return render(request, 'login.html', locals())

@csrf_exempt
def logOut(request):  
           
    request.session['name'] = None
    request.session['email'] = None
    mess = "帳號已經登出!"
    return render(request, 'index.html', locals())

def main(request):                         #render "index.html"出來
    return render(request,'crawlpage.html')


def POST_crawl(request):


	#if 'title' in request.GET and request.GET['title']:
	#keywords = input('請輸入工作職缺關鍵字:')
	keywords = request.POST["title"]


	print('這是第'+ keywords +'頁')
	#url = "https://www.104.com.tw/jobs/search/?keyword=" + keywords 
    
	url = "https://www.gintiantw.com/store/sea/0309sea?page="+keywords+"&"
    
	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式

	driver = webdriver.Chrome(options=options)


	#第一頁內容
	driver.get(url) 
	with open('result.txt', 'w',encoding='utf-8') as f:
       
		
		for i in range(1,10):

			print('這是第'+ str(i) +'個商品')
            
			title = driver.find_elements_by_xpath('//*[@class="title"]')[i].text
			print('產品名稱:' + title)
			
			price = driver.find_elements_by_xpath('//*[@class="price"]')[i].text
			print('價格:' + price)
			price=price.replace('NTD ','')
			price=price.replace(',','')
			href = driver.find_elements_by_xpath('//*[@class="btn btn-primary"]')[i].get_attribute('href')
			print('網址:' + str(href))
			imagelink=driver.find_elements_by_xpath('//*[@class="img-responsive"]')[i].get_attribute('src')
			print('圖片:' + str(imagelink))
			idno=href.replace('https://www.gintiantw.com/store/product/', '')
			idno=idno.replace('?category=sea%2F0309sea', '')
			print('產品編號:' + idno)
			page=keywords
			print('第' + keywords+'頁')
			# job_content = driver.find_element_by_xpath('//*[@id="js-job-content"]/article[%d]/div[1]/p' %(i)).text
			# print('工作內容:' + job_content)
			# job_requirements = driver.find_element_by_xpath('//*[@id="js-job-content"]/article[%d]/div[1]/ul[2]' %(i)).text
			# print('工作地點與學經歷:' + '\n' + job_requirements)
			# job_salary = driver.find_element_by_xpath('//*[@id="js-job-content"]/article[%d]/div[1]/div/span[1]' %(i)).text
			# print('薪水:' + job_salary)
			# print('\n')
			# target = '這是第'+ str(i) +'個工作' + '\n' + '公司名稱:' + '公司名稱:' + job_company +'\n' + '職缺名稱:' + job_title +'\n' + '工作內容:' + job_content + '\n' + '工作地點與學經歷:' + '\n' + job_requirements + '\n' + '薪水:' + job_salary + '\n\n'
			target='產品名稱:' + title+'價格:' + price +'產品編號:' + idno + '網址:' + href +'\n'
			f.write(target)
		
			try:
				updatedata=models.products.objects.get(name=title)  
				     
				print(updatedata)
	
				
					
			except:
				create=models.products.objects.create(name=title, price=int(price), sku=idno,slug='k'+idno,image='p'+str(i),image1='p2',image2='p3',page=page,href=href,imagelink=imagelink)
				create.save()
				print(create)

		
		
		driver.close()
		value=int(keywords)+1
		newvalue=str(value)
		getmany(newvalue)

	text = []
	with open ('result.txt','r',encoding='utf-8') as f:
		for line in f:
			text.append(line)
	

	return render(request,'result.html',locals())




def getmany(nextindex):
	print("這是第"+nextindex+"頁")
	if nextindex==7:
			return render(request,'result.html',locals())
	#if 'title' in request.GET and request.GET['title']:
	#keywords = input('請輸入工作職缺關鍵字:')


	#url = "https://www.104.com.tw/jobs/search/?keyword=" + keywords 
    
	url = "https://www.gintiantw.com/store/sea/0309sea?page="+nextindex+"&"
    
	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式

	driver = webdriver.Chrome(options=options)


	#第一頁內容
	driver.get(url) 
	with open('result.txt', 'w',encoding='utf-8') as f:
       
		
		for i in range(1,10):

			print('這是第'+ str(i) +'個商品')
			try:
				title = driver.find_elements_by_xpath('//*[@class="title"]')[i].text
				print('產品名稱:' + title)
				
				price = driver.find_elements_by_xpath('//*[@class="price"]')[i].text
				print('價格:' + price)
				price=price.replace('NTD ','')
				price=price.replace(',','')
				href = driver.find_elements_by_xpath('//*[@class="btn btn-primary"]')[i].get_attribute('href')
				print('網址:' + str(href))
				imagelink=driver.find_elements_by_xpath('//*[@class="img-responsive"]')[i].get_attribute('src')
				print('圖片:' + str(imagelink))
				idno=href.replace('https://www.gintiantw.com/store/product/', '')
				idno=idno.replace('?category=sea%2F0309sea', '')
				print('產品編號:' + idno)
				page=nextindex
				print('第' + page+'頁')
				target='產品名稱:' + title+'價格:' + price +'產品編號:' + idno + '網址:' + href +'\n'
				f.write(target)
		
				

				
		
				try:
					updatedata=models.products.objects.get(name=title)  
							
					print(updatedata)

				
						
				except:
					create=models.products.objects.create(name=title, price=int(price), sku=idno,slug='k'+idno,image='p'+str(i),image1='p2',image2='p3',page=page,href=href,imagelink=imagelink)
					create.save()
					print(create)

			except:
				print('no data')
		
			
		
		driver.close()

		value=int(nextindex)+1
		newvalue=str(value)
		getmany(newvalue)

		
	text = []
	with open ('result.txt','r',encoding='utf-8') as f:
		for line in f:
			text.append(line)
	

	return render(request,'result.html',locals())



def getqty(request):

		allurl=products.objects.filter(~Q(href= 'nourl'))
		listsize=len(allurl)
		for x in range(1,listsize):
				url=allurl[x].href
				if runurl(url)=="ok":
					continue


		return render(request,'result.html',locals())




def runurl(url):


	print(url)

    
	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式

	driver = webdriver.Chrome(options=options)


	#第一頁內容
	driver.get(url) 
	with open('result.txt', 'w',encoding='utf-8') as f:
       
			title = driver.find_elements_by_xpath('//*[@class="product-title"]')[0].text
			print('產品名稱:' + title)
		
			select= Select(driver.find_element_by_name('product-quantity'))
			
			qty=0
			for op in select.options:
				
					if float(op.text)>float(qty):
							qty=float(op.text)
							qty=int(float(op.text))
			print('產品數量'+str(qty))
			body = driver.find_elements_by_xpath('//*[@class="product-description"]')
			
			x1=""
			for op1 in body:
					
					x1+=op1.text
					
					print(x1)
		
		

		
	
			updatedata=products.objects.get(name=title)  
			updatedata.qty=qty
			updatedata.body=x1
			updatedata.save()
			print(updatedata)
	
		

		
		
		
	
	

	text = []
	with open ('result.txt','r',encoding='utf-8') as f:
		for line in f:
			text.append(line)
	

	return "ok"

def getcrawl(request):

		
	for x in range(1,5):
		
			url="https://www.gintiantw.com/store/product/"+str(int(23594-x))
			
			if runurlwithindex(url)=="ok":
				continue


	return render(request,'result.html',locals())



def runurlwithindex(url):
#爬流水號

	print(url)

    
	options = Options()
	#關閉瀏覽器跳出訊息
	prefs = {
	    'profile.default_content_setting_values' :
	        {
	        'notifications' : 2
	         }
	}
	options.add_experimental_option('prefs',prefs)
	options.add_argument("--headless")            #不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           #開啟無痕模式

	driver = webdriver.Chrome(options=options)


	#第一頁內容
	driver.get(url) 
	with open('result.txt', 'w',encoding='utf-8') as f:
       
		
	

			title = driver.find_elements_by_xpath('//*[@class="product-title"]')[0].text
			print('產品名稱:' + title)
			
			#sku = filter(str.isdigit, title)留取編碼
			select= Select(driver.find_element_by_name('product-quantity'))
			
			qty=0
			for op in select.options:
				
					if float(op.text)>float(qty):
							qty=float(op.text)
							qty=int(float(op.text))
			print('產品數量'+str(qty))
			body = driver.find_elements_by_xpath('//*[@class="product-description"]')
			
			x1=""
			for op1 in body:
					
					x1+=op1.text
					
					print(x1)

			price = driver.find_elements_by_xpath('//*[@class="product-price"]')[0].text
			print('價格:' + price)
			price=price.replace('NTD ','')
			price=price.replace(',','')
			href = url
			print('網址:' + str(href))

			idno=href.replace('https://www.gintiantw.com/store/product/', '')
	
			print('產品編號:' + idno)
			imagelink="www.gintiantw.com/resources/products/"+idno+"/image0.jpg?v=1"
			print('圖片:' + str(imagelink))
			p2="www.gintiantw.com/resources/products/"+idno+"/image1.jpg?v=1"
			print('圖片:' + str(p2))

			create=models.products.objects.create(name=title, price=int(price), body=x1,sku=idno,slug=idno,qty=qty,images='p1',image1=p2,image2='p3',href=href,imagelink=imagelink)
			create.save()
			print(create)
		

	text = []
	with open ('result.txt','r',encoding='utf-8') as f:
		for line in f:
			text.append(line)	

	return "ok"




# def POST_crawl(request):
#     categories = []

#     web_site = "http://www.gintiantw.com"
#     category = "/store/recommended"

#     url = web_site+category
#     r = request.get(url)
#     html_content = r.text
#     soup = BeautifulSoup(html_content, "html.parser")

#     categorylist = soup.find_all('a', class_= "dropdown-tree-a")

#     for line in categorylist:
#         if(line.has_attr('href')):
#             categories.append(line['href'])

#     for cate in categories:
#         if('/' in cate[7:]):
#             catename = cate[7:].split('/')[1] + '.csv'
#         else:
#             catename = cate[7:]+'.csv'

#         with open(catename, 'w') as csvfile:
#             #into category website
#             url = web_site + cate
#             r = requests.get(url)
#             html_content = r.text
#             soup = BeautifulSoup(html_content, "html.parser")
#             products = soup.find_all('div', class_ = "product")

#             product_site = []
#             for product in products:
#                 product_site.append(product.select('div div a')[0]['href'])

#             #into product in the category
#             for product in product_site:
#                 url = web_site+product
#                 r = requests.get(url)
#                 html_content = r.text
#                 soup = BeautifulSoup(html_content, "html.parser")

#                 product_title = soup.find_all('h1', class_="product-title")[0].get_text()
#                 product_description = soup.find_all('div', class_="product-description")
#                 for line in product_description:
#                     product_size = line.find('p').text

#                 product_size  = product_size[product_size.find('尺寸'):].split("\n")[0]
#                 product_price = soup.find_all('h3', class_="product-price")[0].get_text()
#                 product_price = product_price[4:]
#                 product_quantity = soup.find_all('select', class_="product-quantity")[0].find_all('option')
#                 if product_quantity==None:
#                     print(url)
#                 else:
#                     try:
#                         quantity = product_quantity[len(product_quantity) - 1].text
#                     except:
#                         print(url)
#                     s = product_title.strip(" ")+','+product_size+','+product_price.strip()+','+quantity.strip()+'\n'



#                     try:
#                         csvfile.write(s)
#                     except:
#                         print(url+s)
#     return render(request,'result.html',locals())


def donwload_csv(request):

    # change export csv formatting by request parameter. ( url?encode=utf-8 )
    encode = request.GET.get('encode', 'utf-8')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'

    writer = csv.writer(response)

    writer.writerow(['品名', '價格', '型號', '數量','產品描述','圖片','圖片連結','資料連結'])
    productlist=models.products.objects.all()
    for i in range(1,4):
        writer.writerow([productlist[i].name, productlist[i].price, productlist[i].sku, productlist[i].qty,productlist[i].body,productlist[i].imagelink,productlist[i].href])
  
    return response



		