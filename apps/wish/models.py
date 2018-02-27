from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		print postData
		name_regex = re.compile(r'^[a-zA-Z ]+$')
		errors = {}
		if len(postData['name']) < 4:
			errors['name'] = 'Name should be atleast 3 characters'
		if len(postData['uname']) < 4:
			errors['uname'] = 'Username should be atleast 3 characters'
		if not name_regex.match(postData['name']):
			errors['letters'] = 'Letters only for name please'
		if len(postData['pword']) < 8:
			errors['pword'] = 'Password should be atleast 8 characters'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'Passwords dont match'
		if len(postData['date']) < 1:
			errors['date'] = "Please select date"
		if User.objects.filter(username = postData['uname'].lower()).exists():
			errors['exists'] = 'Username already used'
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			a = User.objects.create(name = postData['name'], username = postData['uname'],
				pword = pw, created_at = postData['date'])
			errors['id'] = a.id
		return errors

	def login_validator(self,postData):
		errors = {}
		if len(postData['luname']) < 4:
			errors['luname'] = 'Username should be atleast 3 characters'
		if len(postData['lpword']) < 8:
			errors['lpword'] = 'Password should be atleast 8 characters'
		if len(errors) == 0:
			if User.objects.filter(username = postData['luname']).exists():
				a = User.objects.get(username = postData['luname'])
				if bcrypt.checkpw(postData['lpword'].encode(), a.pword.encode()):
					errors['id'] = a.id
				else:
					errors['credentials'] = "Wrong Credentials"
			else:
				errors['credentials'] = "Wrong Credentials"
		return errors

	def item_validator(self, postData):
		errors = {}
		if len(postData['item']) < 4:
			errors['item'] = 'Item/Product field should be atleast 3 characters'
		if Item.objects.filter(name = postData['item'].lower()).exists():
			errors['exists'] = 'Item already exists'
		if len(errors) == 0:
			Item.objects.create(name = postData['item'].lower(), added_by_id = postData['uid'])
			errors['success'] = "BOOYAH!"
		return errors

	def delete_item(self, iid):
		item = Item.objects.get(id = iid)
		item.delete()
		pass

class User(models.Model):
	name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	pword = models.CharField(max_length = 255)
	created_at = models.DateTimeField()
	objects = UserManager()

class Item(models.Model):
	name = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	added_by = models.ForeignKey(User, related_name= "items")
	wish = models.ManyToManyField(User, related_name="wishes")
		