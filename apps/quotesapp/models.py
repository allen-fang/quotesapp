from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, postData):
		errors = []
		dateNow = datetime.datetime.today().strftime('%Y-%m-%d')
		if len(postData['name']) < 2:
			errors.append('Name must be at least 2 letters')
		if postData['name'].isdigit():
			errors.append('Name cannot contain numbers')
		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Invalid Email')
		if len(postData['password']) < 8:
			errors.append('Password must be at least 8 charcters')
		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match!')
		if postData['birthdate'] > dateNow:
			errors.append('Invalid date')


		if not errors:
			password = postData['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			if self.filter(email=postData['email']).exists():
				errors.append('Email is already registered.')
				return { 'error': errors }
			else:
				user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], hash_pw = hashed, birthdate=postData['birthdate'])
				return { 'theuser': user }
		else:
			return { 'error': errors }

	def login(self, postData):
		errors = []
		if self.filter(email=postData['email']).exists():
			password = postData['password'].encode('utf-8')
			stored_hashed = User.objects.get(email=postData['email']).hash_pw
			if bcrypt.hashpw(password.encode('utf-8'), stored_hashed.encode()) != stored_hashed:
				print "INCORRECT PASSWORD"
				errors.append('Incorrect password')
			else:
				print "CORRECT PASSWORD"
				user = self.get(email=postData['email'])
		else:
			errors.append('Email is not registered')
	
		if not errors:
			return { 'theuser': user }
		else:
			return { 'error': errors }

class QuoteManager(models.Manager):
	def add(self, postData):
		errors = []
		if len(postData['author']) < 4:
			errors.append('Quoted By must be longer than 3 characters')
		if len(postData['quote']) < 11:
			errors.append('Quote must be longer than 10 characters')

		if not errors:
			user = User.objects.get(id=postData['user_id'])
			quote = self.create(content=postData['quote'], author=postData['author'], user=user)
			return { 'thequote': quote }
		else:
			return { 'error': errors }

# Create your models here.
# User class
class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hash_pw = models.CharField(max_length=255)
	birthdate = models.DateField()
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Quote class, many to many relationship with User for favorites, one to many for User
class Quote(models.Model):
	content = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	user = models.ForeignKey(User)
	favorites = models.ManyToManyField(User, related_name="favorites")
	objects = QuoteManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



















