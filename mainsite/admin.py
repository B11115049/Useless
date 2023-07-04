from django.contrib.gis import admin
from mainsite.models import *
from django.contrib.gis.db import models
from mapwidgets.widgets import MapboxPointFieldWidget
# Register your models here.

@admin.register(User)
class UserAdmin(admin.GISModelAdmin):
    list_display = ('name','email','phone','wallet')

@admin.register(Record)
class RecordAdmin(admin.GISModelAdmin):
    list_display = ('user','start','end','routeLength','point')
    formfield_overrides = {
        models.PointField: {"widget": MapboxPointFieldWidget}
    }

admin.site.register(WorldBorder, admin.GISModelAdmin)
#admin.site.register(User,PostAdmin)
