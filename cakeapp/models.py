from django.db import models

# Create your models here.
class Cake(models.Model):
    CAT=((1,'chocolate Cakes'),(2,'Flavour cakes'),(3,'Theme cakes'),(4,'Trending cakes'),(5,'Cupcakes'))
    name=models.CharField(max_length=100, verbose_name='Cake Name')
    price=models.FloatField()
    cat=models.IntegerField(max_length=100,verbose_name='Category', choices=CAT)
    cdetail=models.TextField(verbose_name='Cake Detail')
    is_active=models.BooleanField(default=True)
    cimage=models.ImageField(upload_to='image')

class Cart(models.Model):
    uid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column='uid')
    cid=models.ForeignKey('Cake',on_delete=models.CASCADE, db_column='cid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey('auth.user',on_delete=models.CASCADE, db_column='uid')
    cid=models.ForeignKey('Cake',on_delete=models.CASCADE, db_column='cid')
    qty=models.IntegerField(default=1)
    amt=models.FloatField()

class OrderHistory(models.Model):
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20)