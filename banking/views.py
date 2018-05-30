from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def create_customer(request):
	username_temp = request.POST.get('username', '')
	password_temp = request.POST.get('password', '')
	first_name = request.POST.get('first_name', '')
	last_name = request.POST.get('last_name', '')
	user, created = User.objects.get_or_create(username = username_temp, email='NA')
	if created:
		user.set_password(password_temp)
		#profile = Profile.objects.filter(user = user)
		#profile.balance = 5000
		#profile.first_name = first_name
		#profile.last_name = last_name
		user.profile.first_name = first_name
		user.profile.last_name = last_name
		print(user.profile.first_name + user.profile.last_name) 
		user.save()
		return JsonResponse( {'message': 'Successful creation!'}, status = 200 )
	else:
		return JsonResponse( {'error': 'User already exists'}, status = 400)

def login_customer(request):
	username_temp = request.POST.get('username', '')
	password_temp = request.POST.get('password', '')
	user = authenticate(request, username = username_temp, password = password_temp)
	if user is not None:
		login(request, user)
		return JsonResponse( {'message': 'Successful login!', 'balance': user.profile.balance}, status = 200 )
	else:
		return JsonResponse( {'error': 'Invalid details!'}, status = 401 )

def logout_customer(request):
	logout(request)
	return JsonResponse({})

def delete_customer(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'error': 'Get Lost'
			})
	user_temp = request.user
	print(user_temp.profile.first_name)
	logout(request)
	Profile.objects.filter(user = user_temp).delete()
	User.objects.filter(username = user_temp.username).delete()
	return JsonResponse( {} )

def check_session(request):
	return JsonResponse( {'username': request.user.username, 
		'first_name': request.user.profile.first_name,
		}, status = 200 )

def get_balance(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'error': 'Get Lost'
		})
	return JsonResponse({
		'balance': request.user.profile.balance,
		})

def withdraw(request):
	user = request.user
	print(user.is_authenticated)
	if not request.user.is_authenticated:
		return JsonResponse({
			'error': 'Get Lost'
			})
	withdraw_amount = int(request.POST.get('amount', ''))
	#print(request.POST)
	cur_balance = user.profile.balance
	if withdraw_amount > cur_balance:
		return JsonResponse({
			'error': 'Insufficient Funds!'
			}, status = 400)
	else:
		user.profile.balance = user.profile.balance - withdraw_amount
		user.save()
		return JsonResponse({
			'message': 'Withdrawl Successful',
			'new_balance': user.profile.balance,
			}, status = 200)

def deposit(request):
	if not request.user.is_authenticated:
		return JsonResponse({
			'error': 'Get Lost'
		})
	user = request.user
	deposit_amount = int(request.POST.get('amount', ''))
	user.profile.balance = user.profile.balance + deposit_amount
	user.save()
	return JsonResponse({
		'message': 'Deposti Successful',
		'new_balance': user.profile.balance,
		}, status = 200)