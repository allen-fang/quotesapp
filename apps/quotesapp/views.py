from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

# Create your views here.
# Renders Log in page
def index(request):
	return render(request, "quotesapp/index.html")

# Renders Dashboard
def dashboard(request):
	quotes = Quote.objects.all()
	context = {
		'user': User.objects.get(id=request.session['user']),
		'quotes': quotes
	}
	return render(request, "quotesapp/dashboard.html", context)

# renders user page
def user(request, id):
	user = User.objects.get(id=id)
	quotes = Quote.objects.filter(user=user)
	context = {
		'user': user,
		'quotes': quotes
	}
	return render(request, "quotesapp/user.html", context)

# process log in and regstration
def process_logreg(request):
	if request.POST['action'] == 'register':
		postData = {
			'name': request.POST['name'],
			'alias': request.POST['alias'],
			'email': request.POST['email'],
			'password': request.POST['password'],
			'confirm_pw': request.POST['confirm_pw'],
			'birthdate': request.POST['birthdate']
		}
		user = User.objects.register(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			messages.success(request, 'Successfully registered, you may now log in.')
			return redirect('/')
	elif request.POST['action'] == 'login':
		postData = {
			'email': request.POST['email'],
			'password': request.POST['password']
		}
		user = User.objects.login(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			return redirect('/dashboard')

# Adding a quote
def addQuote(request):
	postData = {
		'quote': request.POST['quote'],
		'author': request.POST['author'],
		'user_id': request.session['user']
	}
	quote = Quote.objects.add(postData)
	if 'error' in quote:
		for message in quote['error']:
			messages.error(request, message)
	if 'thequote' in quote:
		pass
	return redirect('/dashboard')

# Adding a favorite quote
def addFavorite(request, id):
	user = User.objects.get(id=request.session['user'])
	quote = Quote.objects.get(id=id)
	quote.favorites.add(user)
	return redirect('/dashboard')

# remove a favorite quote
def removeFavorite(request, id):
	user = User.objects.get(id=request.session['user'])
	quote = Quote.objects.get(id=id)
	quote.favorites.remove(user)
	return redirect('/dashboard')

# logout 
def logout(request):
	request.session.clear()
	return redirect('/')

































