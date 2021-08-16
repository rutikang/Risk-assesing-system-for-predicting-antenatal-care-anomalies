from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class riskFactorForm(ModelForm):
	class Meta:
		model = riskFactor
		fields = '__all__'

class DiagnosisForm(ModelForm):
	class Meta:
		model = Diagnosis
		fields = [  'riskfactor', 'status']

class NewDiagnosisForm(ModelForm):
	class Meta:
		model = Diagnosis
		fields = [  'patient','riskfactor', 'status']

class createPatientForm(ModelForm):
	class Meta:
		model = Patient
		fields = ['name', 'phone', 'email', 'age', 'height', 'weight']

# class PredictionForm(ModelForm):
# 	class Meta:
# 		model = Prediction
# 		fields = [  'patient', 'pregnancies', 'Uterine_size', 'blood_pressure', 'abortion', 'drugs', 'BMI', 'diabetes']
