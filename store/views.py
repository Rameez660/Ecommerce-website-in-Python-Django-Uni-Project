from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.models import User

# ---------------------------------------------------------------------
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
#-----------------------------------------------------------------------
from .forms import * 

def store(request):
	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)
		if not Customer.objects.filter(user=user):
			Customer.objects.create(user=user)

		data = cartData(request)

		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		products = Product.objects.all()
		context = {'products':products, 'cartItems':cartItems}
		return render(request, 'store/store.html', context)
	else:
		data = cartData(request)

		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

		products = Product.objects.all()
		context = {'products':products, 'cartItems':cartItems}
		return render(request, 'store/store.html', context)

def viewdetail(request,myid):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.get(id=myid)

	if request.user.is_authenticated:
		profile = Customer.objects.get(user=request.user)
		reviews = Reviews.objects.filter(profile=profile,product=products).order_by('-id')
		
		# for i in reviews:
		# 	reviews1 = Reviews.objects.filter(profile=profile,product=products).exists()
		# 	if reviews1 == True:
		# 		print(reviews1)
			
		if 'bid' in request.POST:
			# if profile.counter > 0 and profile.incrementtimeStamp <= datetime:
			if request.method=='POST':
				description=request.POST.get('description')
				ratings=request.POST.get('ratings')
				# timeStamp=request.POST.get('timeStamp')
				
				#   if not subject.strip()=='':
				form = formReviews(request.POST,request.FILES)
				if form.is_valid():
					instance = form.save(commit=False)
					instance.profile = profile
					instance.product = products
					form.save()
					return redirect('viewdetail',myid=myid)

		context = {'products':products, 'cartItems':cartItems,'items':items,'reviews':reviews}
		return render(request, 'store/viewdetail.html', context)
	else:
		context = {'products':products, 'cartItems':cartItems,'items':items,}
		return render(request, 'store/viewdetail.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

@login_required(login_url='handlelogin')
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	# customer = Customer.objects.get(user=request.user)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		# customer = Customer.objects.get(user=request.user)
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def search(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	query=request.GET['query']
	if len(query)>100:
		# allPosts=[]
		allPosts=Product.objects.none()
	else:
		allPostsname=Product.objects.filter(name__icontains=query)
		allPostsprice=Product.objects.filter(price__icontains=query)

		allPosts = allPostsname.union(allPostsprice)
	# if allPosts.count() == 0:
	#     messages.error(request,"No search results found plear search with another query")
		
	# allPosts:Post.objects.all()
	return render(request, 'store/search.html' ,{'allPosts':allPosts,'query':query,'cartItems':cartItems})


def aboutus(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	return render(request, 'store/aboutus.html',{'cartItems':cartItems})
def contactus(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	return render(request, 'store/contactus.html',{'cartItems':cartItems})

def handlesignup(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method =='POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if len(username)>20:
            messages.error(request,'Your username must be under 20')
            return redirect('handlesignup')
        if pass1 != pass2:
            messages.error(request,'Your Password Donot Match')
            return redirect('handlesignup')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        if myuser:
            myuser.save()
            messages.success(request,'Your Account has been successfully created')      
            return redirect('handlelogin')
        else:
            return redirect('handlesignup')
            
    else:
        return render(request,'store/signup.html',{'signup':'set', 'cartItems':cartItems})	
	# return render(request, 'store/signup.html',{'signup':'set'})

def handlelogin(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method =='POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']   

        user = authenticate(request,username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Your Account has been Successfully logged in')
            return redirect('/')
        else:
            messages.error(request,'please try again later')
            return render(request,'store/signin.html',{'signin':'set', 'cartItems':cartItems})

    return render(request,'store/signin.html',{'signin':'set', 'cartItems':cartItems})

def handlelogout(request):
    logout(request)
    messages.success(request,'Your Account has been successfully logged out')
    return redirect('/')