from django.contrib import admin
from .models import TrainStation,TrainLog,Train
# Register your models here.

admin.site.register(TrainStation)
admin.site.register(Train)
admin.site.register(TrainLog)
