from django.shortcuts import render,redirect,HttpResponse
from cakeapp.models import Cake,Cart,Order,OrderHistory
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django.contrib.auth.models import User
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.


def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        context={}
        n=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        if n=='' or p=='' or cp=='':
            context['errmsg']= 'Field Cannot Be Empty'
            return render(request,'register.html',context)
        elif len(p)<8:
            context['errmsg']='Password Must Contain Atleast 8 Characters'
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']='Password & Confirm Password must be Same'
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=n,email=n)
                u.set_password(p)
                u.save()
                context['success']='User Created Successfully'
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']='User Already Exist! Please Login'
                return render(request,'register.html',context)
            

def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        u=authenticate(username=n,password=p)
        
        if u is not None:
            login(request,u)
            return redirect('/cake')
        else:
            context={}
            context['errmsg']='Invalid Username and password'
            return render(request,'login.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/cake')

def cake(request):
    c=Cake.objects.filter(is_active=True)[:8]
    context={}
    context['data']=c
    return render(request,'index.html',context)

def cakedetail(request,cid):
    c=Cake.objects.filter(id=cid)
    context={}
    context['data']=c
    return render(request,'cake_detail.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    c=Cake.objects.filter(q1 & q2)
    context={}
    context['data']=c
    return render(request,'home.html',context)

def placeorder(request):
    cart=Cart.objects.filter(uid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in cart:
        amount=x.qty*x.cid.price 
        o=Order.objects.create(orderid=orderid,cid=x.cid,uid=x.uid,qty=x.qty,amt=amount)
        o.save()

        x.delete()
        
    return redirect('/fetchorder')

def addtocart(request,cid):
    if request.user.is_authenticated:
        context={}
        u=User.objects.filter(id=request.user.id)
        c=Cake.objects.filter(id=cid)

        q1=Q(uid=u[0])
        q2=Q(cid=c[0])
        cart=Cart.objects.filter(q1 & q2)
        n=len(cart)
        context['data']=c
        if n==1:
            context['errmsg']='Cake Already Exist'
            return render(request,'cake_detail.html',context)
        else:
            cart=Cart.objects.create(uid=u[0],cid=c[0])
            cart.save()
            context['msg']="Cake Added Successfully"
            return render(request,'cake_detail.html',context)
    else:
        return redirect('/login')
    
def viewcart(request):
    cart=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=cart
    sum=0
    for x in cart:
        sum=sum+x.cid.price*x.qty

    context['total']=sum
    context['n']=len(cart)
    return render(request,'cart.html',context)

def updateqty(request,x,cartid):
    cart=Cart.objects.filter(id=cartid)

    q=cart[0].qty

    if x == '1':
        q=q+1
    elif q>1:
        q=q-1

    cart.update(qty=q)
    return redirect('/viewcart')

def remove(request,cartid):
    cart=Cart.objects.filter(id=cartid)
    cart.delete()
    return redirect('/viewcart')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id,orderhistory__isnull=True)

    context={'data':o}
    sum=0
    for x in o:
        sum=sum+x.amt
    
    context['total']=sum
    context['n']=len(o)

    orders_to_delete = list(o)
    for order in orders_to_delete:
        OrderHistory.objects.create(order=order, payment_status='successfull')
    
    return render(request,'placeorder.html',context)

def search(request):
    query=request.GET['query']
    cname=Cake.objects.filter(name__icontains=query)
    ccat=Cake.objects.filter(cat__icontains=query)
    cdetail=Cake.objects.filter(cdetail__icontains=query)
    
    allprod=cname.union(ccat,cdetail)
    context={}
    
    if allprod.count()==0:
        context['errmsg']='Product NOT FOUND'
    
    context['data']=allprod
    return render(request,'home.html',context)

def sortbyprice(request,sv):
    
    if sv=='1':
        c=Cake.objects.order_by('-price')
        
    else:
        c=Cake.objects.order_by('price')
    
    context={}
    context['data']=c
    return render(request,'home.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_LFpDzBPlXVUw76", "JhNBqmYfIdLDva5XA0oGm77l"))
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    for x in o:
        sum+=x.amt
        orderid=x.orderid
    data = { "amount": sum*100, "currency": "INR", "receipt": "orderid" }
    payment = client.order.create(data=data)  
    #print(payment)
    context={}
    context['payment']=payment  
    return render(request,'pay.html',context)


def paymentsuccess(request):
    sub='Payment Successful'
    msg='Thanks for your Ordering..!!'
    frm='swaralichande23@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'payment_success.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')