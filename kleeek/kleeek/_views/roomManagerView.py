# import datetime 
# from django.db import models
# from django.http import Http404, HttpResponse
# from django.contrib.auth.models import User
# from kleeek.kleeek.models import roomType
# from kleeek.kleeek.models import roomManager
# from kleeek.kleeek.models import roomLog

# class roomManagerView(object):
#     """docstring for roomManagerView"""
#     def __init__(self, arg):
#         super(roomManagerView, self).__init__()
#         self.arg = arg
        
#     def get_admin(self, arg):
#         try:
#             return HttpResponse("admin.html")
#         except Exception, e:
#             raise Http404()