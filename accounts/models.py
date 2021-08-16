from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	age = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)


	def __str__(self):
		return self.name


class riskFactor(models.Model):
	# CATEGORY = (
	# 		('Indoor', 'Indoor'),
	# 		('Out Door', 'Out Door'),
	# 		) 

	name = models.CharField(max_length=200, null=True)
	risk_weight = models.IntegerField(null=True)
	# category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_diagonised = models.DateTimeField(auto_now_add=True, null=True)
	# tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Prediction(models.Model):
	patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)	
	pregnancies = models.IntegerField(null=True)
	Uterine_size = models.IntegerField(null=True)
	blood_pressure = models.IntegerField(null=True)
	abortion = models.IntegerField(null=True)
	drugs = models.IntegerField(null=True)
	BMI = models.FloatField(null=True)
	diabetes = models.FloatField(null=True)


class Diagnosis(models.Model):
	STATUS = (
			('Current', 'Current'),
			('Past', 'Past'),
		
			)

	patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
	riskfactor = models.ForeignKey(riskFactor, null=True, on_delete= models.SET_NULL)
	# prediction = models.ForeignKey(Prediction, null=True, on_delete= models.SET_NULL)
	date_diagonised = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.patient.name