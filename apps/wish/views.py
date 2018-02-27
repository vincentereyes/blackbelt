from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	return redirect('/main')

def loginreg(request):
	return render(request, 'wish/index.html')

def register(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if 'id' not in errors:
			request.session['status'] = "reg"
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/main')
		else:
			request.session['id'] = errors['id']
			return redirect('/dashboard')
	return redirect('/main')

def login(request):
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		if 'id' not in errors:
			request.session['status'] = "log"
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/main')
		else:
			request.session['id'] = errors['id']
			return redirect('/dashboard')
	return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/main')

def dashboard(request):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		user = User.objects.get(id = request.session['id'])
		wishes = user.wishes.all()
		items = Item.objects.filter(added_by_id = request.session['id'])
		otheritems = Item.objects.exclude(wish = request.session['id']).exclude(added_by_id = request.session['id'])
		context = {
			'user': user,
			'wishes': wishes,
			'items': items,
			'others': otheritems
		}
		return render(request, 'wish/dashboard.html', context)

def additem(request):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		return render(request, 'wish/additem.html')

def add(request):
	if request.method == "POST":
		errors = User.objects.item_validator(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/additem')
		else:
			return redirect('/dashboard')
	return redirect('/main')

def showitem(request, iid):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		a = Item.objects.get(id = iid)
		b = a.wish.all()
		context = {
			'item': a,
			'wishers': b
		}
		return render(request, 'wish/showitem.html', context)

def addwish(request, iid):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		this_user = User.objects.get(id = request.session['id'])
		this_item = Item.objects.get(id = iid)
		this_item.wish.add(this_user)
		return redirect('/dashboard')

def delete(request, iid):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		User.objects.delete_item(iid)
		return redirect('/dashboard')

def remove(request, iid):
	if 'id' not in request.session:
		return redirect('/main')
	else:
		this_user = User.objects.get(id = request.session['id'])
		this_item = Item.objects.get(id = iid)
		this_item.wish.remove(this_user)
		return redirect('/dashboard')
	pass













