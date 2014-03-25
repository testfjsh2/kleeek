from django.contrib import admin

from models import roomManager
from models import roomLog
from models import roomType
from models import payment

class roomManagerAdmin(admin.ModelAdmin):
    pass

class roomTypeAdmin(admin.ModelAdmin):
    pass

class paymentAdmin(admin.ModelAdmin):
    pass

class roomLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(roomManager, roomManagerAdmin)
admin.site.register(roomLog, roomLogAdmin)
admin.site.register(roomType, roomTypeAdmin)
admin.site.register(payment, paymentAdmin)
# Register your models here.