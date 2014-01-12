from django.contrib import admin

from models import roomManager
from models import roomType

class roomManagerAdmin(admin.ModelAdmin):
    pass

class roomTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(roomManager, roomManagerAdmin)
admin.site.register(roomType, roomTypeAdmin)
# Register your models here.