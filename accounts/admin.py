from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Patient)
admin.site.register(Diagnosis)
admin.site.register(riskFactor)
admin.site.register(Prediction)
