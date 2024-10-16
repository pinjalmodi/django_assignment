from django.shortcuts import render
from .models import User,Product_mst,Product_sub_cat
from django.db.models import Q

# Create your views here.
def register(request):
	if request.method=='POST':
		try:
			User.objects.get(email=request.POST['email'])
			msg='Email id already registered'
			return render(request,'login.html',{'msg':msg})

		except:
			User.objects.create(
				usertype=request.POST['usertype'],
				fname=request.POST['fname'],
				mobile=request.POST['mobile'],
				email=request.POST['email'],
				address=request.POST['address'],
				password=request.POST['password'],
				profile_picture=request.FILES['profile_picture']

				)
			msg='User Registered Successfully'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'register.html')

def index(request):
	return render(request,'index.html')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_picture']=user.profile_picture.url
				if user.usertype=='admin':
					msg='Login Successful'
					return render(request,'upload-name.html',{'msg':msg})
				else:
					msg='Login Successful'
					return render(request,'product_search.html',{'msg':msg})

			else:
				msg='Password Incorrect'
				return render(request,'login.html',{'msg':msg})
		except:
			msg='Email id not registered'
			return render(request,'register.html',{'msg':msg})
	else:		
		return render(request,'login.html')

def upload_name(request):
	products=Product_mst.objects.all()
	if request.method=='POST':
		action=request.POST['action']
		if action=='add':
			Product_mst.objects.create(
				product_id=request.POST['id'],
				product_name=request.POST['product_name']
				)
			msg='Name Added Successfully'
			
			return render(request,'upload-details.html',{'msg':msg,'products':products})
		else:
			msg='Invalid Action'
			return render(request,'upload-name.html',{'msg':msg})
	else:
		return render(request,'upload-name.html')

def upload_details(request):
	products=Product_mst.objects.all()
	if request.method=='POST':
		act=request.POST['act']
		if act=='add':
			product_name = request.POST.get('product_name')
			
			try:
				product=Product_mst.objects.get(product_name=product_name)
				
				Product_sub_cat.objects.create(
					product_name=product,
					product_id=request.POST['product_id'],
					product_price=request.POST['product_price'],
					product_image=request.FILES['product_image'],
					product_model=request.POST['product_model'],
					product_ram=request.POST['product_ram'],
					)
				msg='Product Detail Added successfully'

				return render(request,'upload-details.html',{'msg':msg,'products':products})
			except Product_mst.DoesNotExist:
				print(f'Product with name {product_name} does not exist.')
				msg='Product name not found'
				return render(request,'upload-details.html',{'msg':msg,'products':products})
			
		

		elif act=='select':
			product_id=request.POST.get('product_id')
			product_name = request.POST.get('product_name')
			
			try:
				product_details=Product_sub_cat.objects.get(product_id=product_id)
				
				msg='Product Found'
				return render(request,'upload-details.html',{'msg':msg,'product_details':product_details,'products':products})
			except Product_sub_cat.DoesNotExist:
				msg='Product Not Found'
				return render(request,'upload-details.html',{'msg':msg})

			try:
				product=Product_mst.objects.get(product_name=product_name)
				msg='Product Found'
				return render(request,'upload-details.html',{'msg':msg,'product_details':product_details,'product':product,'products':products})
			except Product_mst.DoesNotExist:
				msg='Product Not Found'
				return render(request,'upload-details.html',{'msg':msg})
		

		elif act=='edit':
			product_id=request.POST.get('product_id')
			product_name=request.POST.get('product_name')
			try:
				product=Product_mst.objects.get(product_name=product_name)
				product_details = Product_sub_cat.objects.get(product_id=product_id)

				product_details.product_name=product
				product_details.product_id=request.POST['product_id']
				product_details.product_price=request.POST['product_price']
				if 'product_image' in request.FILES:
					product_details.product_image=request.FILES['product_image']
				product_details.product_model=request.POST['product_model']
				product_details.product_ram=request.POST['product_ram']
			
				product_details.save()
				msg='Product Updated successfully'

				return render(request,'upload-details.html',{'msg':msg,'products':products})
			except Product_mst.DoesNotExist:
				print(f'Product with name {product_name} does not exist.')
				msg='Product name not found'
				return render(request,'upload-details.html',{'msg':msg,'products':products})
		elif act=='delete':
			product_id=request.POST.get('product_id')
			product_name=request.POST.get('product_name')
			try:
				product=Product_mst.objects.get(product_name=product_name)
				product_details = Product_sub_cat.objects.get(product_id=product_id)

				product_details.delete()
				msg='Product Deleted Successfully'
				return render(request,'upload-details.html',{'msg':msg,'products':products})

			except:
				msg='Product does not exist'
				return render(request,'upload-details.html',{'msg':msg,'products':products})
		else:
			msg='Invalid Action'
			return render(request,'upload-details.html',{'msg':msg,'products':products})

	
	return render(request,'upload-details.html',{'products':products})

def product_search(request):
    query = request.POST.get('query', '')
    product_details = []

    if query:

        product_details = Product_sub_cat.objects.filter(product_name__product_name__icontains=query)
    return render(request, 'product_search.html', {'product_details':product_details,'query': query})