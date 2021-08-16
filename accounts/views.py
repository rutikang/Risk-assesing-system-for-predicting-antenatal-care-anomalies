from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages  # enables messages such as account was craeted successfuly
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #prevents access to the pages that require logging in
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .models import *
# machine learning imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# from django.views.generic import TemplateView #chartjs
# from chartjs.views.lines import BaseLineChartView #chartjs
# Create your views here.

@login_required(login_url='login') # means log in is required to access the page and it automatically will open the home page
@admin_only
def home(request):     
    patient = Patient.objects.all()
    diagnosis = Diagnosis.objects.all()
    riskfactor = riskFactor.objects.all()
    total_patients = patient.count()
    users = Patient.objects.all()
    

    context = {'patient': patient,'diagnosis': diagnosis, 'totalpatients': total_patients, 'riskfactor':riskfactor, 'users': users}

    return render (request, 'accounts/dashboard.html', context)

@login_required(login_url='login') # means log in is required to access the page and it automatically will open the home page
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    patients = Patient.objects.get(id=pk)

    diagnosis = patients.diagnosisa.all() # way of quering the patients child object from the models field 
    diagnosis_count = diagnosis.count()
    current = diagnosis.filter(status='Current').count()
    past = diagnosis.filter(status='Past').count()
	# current = diagnosis.filter(status='Current').count()
	# past = diagnosis.filter(status='Past').count()


    context = {'patients':patients, 'diagnosis': diagnosis, 'diagnosis_count': diagnosis_count, 'current':current, 'past':past}
    return render (request, 'accounts/customers.html', context)

@login_required(login_url='login') # means log in is required to access the page and it automatically will open the home page
@allowed_users(allowed_roles=['admin'])
def products(request):
    risk = riskFactor.objects.all()
    context = {'risk': risk}
    return render (request, 'accounts/products.html',context)  

@unauthenticated_user  #decorator
def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')  #send a registered user to the home page
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password) #authenticating that the user is in the database

        if user is not None:
            login(request, user)
            return redirect('home') #if the login is sucessful and the user exists it redirects them to the home page

        else:
            messages.info(request, 'Username or password is incorrect') #returns a flash message incase wrong credentials

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user  #decorator
def registerpage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')  #send a registered user to the home page
    # else:
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')   # gets the username of the person who has just registered

            group = Group.objects.get(name = 'customer')
            user.groups.add(group)   #automatically assigns a  registerd user to the customers group
            
            Patient.objects.create(  #creates the patient user account once registered
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for '+ username)

            return redirect('login') #if registration is a sucess it redirects the user to the login page


    context = {'form' : form}
    return render(request, 'accounts/register.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	diagnosis = request.user.patient.diagnosis_set.all()
	# patients = Patient.objects.get(id=pk)

	diagnosis_count = diagnosis.count()
	current = diagnosis.filter(status='Current').count()
	past = diagnosis.filter(status='Past').count()

	# print('Diagnosis:', diagnosis, )

	context = {'diagnosis':diagnosis, 'diagnosis_count':diagnosis_count,
	'current':current,'past':past}
	return render(request, 'accounts/user.html', context)

def createriskFactor(request):
	form = riskFactorForm()
	if request.method == 'POST':
		form = riskFactorForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/riskfactor_form.html', context)



def createDiagnosis(request, pk):

	diag = Diagnosis.objects.get(id=pk)
	form = DiagnosisForm(instance=diag)

	if request.method == 'POST':
		form = DiagnosisForm(request.POST, instance=diag)
		if form.is_valid():
			form.save()
			return redirect('/')

    

	context = {'form':form}
	return render(request, 'accounts/diagnosis_form.html', context)

def createnewDiagnosis(request):

	# diag = Diagnosis.objects.get(id=pk)
	form = NewDiagnosisForm()

	if request.method == 'POST':
		form = NewDiagnosisForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

    

	context = {'form':form}
	return render(request, 'accounts/diagnosis_form.html', context)



def deleteDiagnosis(request, pk):

	diag = Diagnosis.objects.get(id=pk)

	if request.method == "POST":
		diag.delete()
		return redirect('/')

    

	context = {'item':diag}
	return render(request, 'accounts/deletediagnosis.html', context)

   

def createPatient(request):
	form = createPatientForm()
	if request.method == 'POST':
		form = createPatientForm(request.POST)
		if form.is_valid():
			form.save() 
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/patient_form.html', context)

def updateRiskfactor(request, pk):

	risk = riskFactor.objects.get(id=pk)
	form = riskFactorForm(instance=risk)

	if request.method == 'POST':
		form = riskFactorForm(request.POST, instance=risk)
		if form.is_valid():
			form.save()
			return redirect('/')

    

	context = {'form':form}
	return render(request, 'accounts/riskfactor_form.html', context)


def deleteriskfactor(request, pk):
	risk = riskFactor.objects.get(id=pk)
	if request.method == "POST":
		risk.delete()
		return redirect('/')

	context = {'item':risk}
	return render(request, 'accounts/delete.html', context)

def updatePatient(request, pk):

	patient = Patient.objects.get(id=pk)
	form = createPatientForm(instance=patient)

	if request.method == 'POST':
		form = createPatientForm(request.POST, instance=patient)
		if form.is_valid():
			form.save()
			return redirect('/')

    

	context = {'form':form}
	return render(request, 'accounts/patient_form.html', context)

def deletePatient(request, pk):

	patient = Patient.objects.get(id=pk)

	if request.method == "POST":
		patient.delete()
		return redirect('/')

    

	context = {'item':patient}
	return render(request, 'accounts/deletepatient.html', context)

def createPrediction(request):

	prediction = Prediction.objects.all()
	context = {}
	return render(request, 'accounts/predict.html', context)

	# form = PredictionForm()

	# if request.method == 'POST':
	# 	form = PredictionForm(request.POST)
	# 	if form.is_valid():
	# 		form.save()
			# return redirect('/')

    

	# context = {'form':form}
	# return render(request, 'accounts/diagnosis_form.html', context)


def predictionResult(request):

	data = pd.read_csv(r"C:\Users\hp\Desktop\Book1.csv")
	X = data.drop("Outcome", axis=1)
	Y = data['Outcome']

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

	model = LogisticRegression(solver='lbfgs', max_iter=500)
	model.fit(X_train, Y_train)

	patient = request.POST.get('pregnancies')
	pregnancies = float(request.POST.get('pregnancies'))
	Uterine_size = float(request.POST.get('Uterine_size'))
	blood_pressure = float(request.POST.get('blood_pressure'))
	abortion = float(request.POST.get('abortion'))
	drugs = float(request.POST.get('drugs'))
	BMI = float(request.POST.get('BMI'))
	diabetes = float(request.POST.get('diabetes'))
	age = float(request.POST.get('age'))


	pred = model.predict([[pregnancies, Uterine_size, blood_pressure, abortion, drugs, BMI, diabetes, age]])

	result = ""
	if pred==[1]:
		result = "High Risk"
		# predd = patient=patient,pregnancies=pregnancies,Uterine_size=Uterine_size,blood_pressure=blood_pressure,abortion=abortion,drugs=drugs,BMI=BMI,diabetes=diabetes

		# predd.save()
		# return redirect('predictionResult')
	else:
		result = "No Risk"
		print(result)
		# predd = patient=patient,pregnancies=pregnancies,Uterine_size=Uterine_size,blood_pressure=blood_pressure,abortion=abortion,drugs=drugs,BMI=BMI,diabetes=diabetes

		# predd.save()
		# return redirect('predictionResult')

	

	context = {'result':result}
	return render(request, 'accounts/predict.html', context)
