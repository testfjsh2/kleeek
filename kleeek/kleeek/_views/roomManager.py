# import datetime 
# from django.db import models
# from django.contrib.auth.models import User
# from kleeek.kleeek.models import roomType
# from kleeek.kleeek.models import roomManager
# from kleeek.kleeek.models import roomLog

# class roomManager(object):
#     """docstring for roomManager"""
#     def __init__(self, arg):
#         super(roomManager, self).__init__()
#         # self.arg = 

#     def createRoomType(self, name, image):
#         try:
#             newRoomType = roomType(name, image)
#             newRoomType.save()
#         except Exception, e:
#             raise e

#     def getListRoom(self):
#         try:
#             listRoom = roomType.object.all()
#             return listRoom
#         except Exception, e:
#             raise e

#     def createRoom(self, roomTypeID, dateLost):
#         dateCreate = datetime.now()
#         status = "active"
#         try:
#             newRoomManager = roomManager(roomTypeID=roomTypeID, dateLost=dateLost, dateCreate=dateCreate, status=status)
#             newRoomManager.save()
#         except Exception, e:
#             raise e

#     def setRoomManagerTime(self, id, dateLost):
#         try:
#             roomManagerCurrent = roomManager.object.filter(id=id)[1]
#             roomManagerCurrent(dateLost=dateLost)
#         except Exception, e:
#             raise e

#     def setRooManagerStatus(self, id, status):
#         try:
#             roomManagerCurrent = roomManager.object.filter(id=id)[1]
#             roomManagerCurrent(status=status)
#         except Exception, e:
#             raise e