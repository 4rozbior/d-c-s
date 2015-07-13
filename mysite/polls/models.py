from django.db import models

# Create your models here.

class Poll(models.Model):
	question = models.CharFiled(max_length=200)
	pub_date = models.DateTimeField('data publikacji')
	
class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharFiled(max_length=200)
	votes = models.IntegerField()