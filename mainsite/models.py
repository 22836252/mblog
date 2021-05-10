from django.db import models

from django.utils import timezone
from django.core.validators import MaxValueValidator

class products(models.Model):
    sku=models.CharField(max_length=200, default='A0001')
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    # type =  models.CharField(max_length=200, default='其他')
    body = models.TextField()
    brand = models.CharField(max_length=200, default='自有品牌')
    # images= models.CharField(max_length=200 , default='')
    # image1= models.CharField(max_length=200 , default='')
    # image2= models.CharField(max_length=200 , default='')
    pub_date = models.DateTimeField(default=timezone.now)
    pid= models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField()   
    page= models.PositiveIntegerField(default='0') 
    href=models.CharField(max_length=200 , default='nourl')
    imagelink=models.CharField(max_length=200 , default='nourl')

    # SIZES = (
    #     ('S', 'Small'),
    #     ('M', 'Medium'),
    #     ('L', 'Large'),
    #     )
    # size = models.CharField(max_length=1, default='',choices=SIZES)
    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
class Account(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email= models.CharField(max_length=200, default='')
    def __str__(self):
        return self.name 

class Cart(models.Model):
   
    productName = models.CharField(max_length=200)
    price= models.PositiveIntegerField(default=0)
    BuyerName=models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=0)
    email= models.CharField(max_length=200, default='')
    order_date = models.DateTimeField(default=timezone.now)
    productsku=models.CharField(max_length=200, default='')
    def __str__(self):
        return self.productName

class ShippingDetail(models.Model):
    shippingAddress = models.CharField(max_length=200)
    wayofShipping = models.CharField(max_length=200)
    BuyerName=models.CharField(max_length=200)
    def __str__(self):
        return self.BuyerName


class NewTable(models.Model):
    models_f = models.BigIntegerField()
    bool_f = models.BooleanField()
    date_f = models.DateField(auto_now=True)
    char_f = models.CharField(max_length=20,unique=True)
    datetime_f = models.DateTimeField(auto_now_add=True)
    decimal_f = models.DecimalField(max_digits=10,
    decimal_places=2)
    float_f = models.FloatField(null=True)
    int_f = models.IntegerField(default=2010)
    tesxt_f = models.TextField()

    def __str__(self):
        return self.tesxt_f
        #回傳在admin顯示的資料