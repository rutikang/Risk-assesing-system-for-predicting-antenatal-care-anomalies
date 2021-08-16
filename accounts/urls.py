from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = "home"),
    path('customers/<str:pk>/' , views.customers, name = 'customers'),
    path('products/' , views.products, name = 'products'),

    path('login/', views.loginpage , name = "login"),
    path('logout/', views.logoutUser , name = "logout"),
    path('userPage/', views.userPage, name = "user-page"),
    path('register/', views.registerpage , name = "register"),
    path('createriskFactor/', views.createriskFactor, name="createriskFactor"),
    path('createDiagnosis/<str:pk>/', views.createDiagnosis, name="createDiagnosis"), 
    path('createPatient/', views.createPatient, name="createPatient"), 
    path('updateRiskfactor/<str:pk>/', views.updateRiskfactor, name="updateDiagnosis"), 
    path('deleteriskfactor/<str:pk>/', views.deleteriskfactor, name="deleteriskfactor"), 
    path('deleteDiagnosis/<str:pk>/', views.deleteDiagnosis, name="deleteDiagnosis"), 
    path('updatePatient/<str:pk>/', views.updatePatient, name="updatePatient"), 
    path('createnewDiagnosis/', views.createnewDiagnosis, name="createnewDiagnosis"), 
    path('deletePatient/<str:pk>/', views.deletePatient, name="deletePatient"), 
    path('createPrediction/', views.createPrediction, name="createPrediction"), 
    path('createPrediction/predictionResult', views.predictionResult, name="predictionResult"), 
















    

]
