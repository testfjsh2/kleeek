from django.shortcuts import render
from models import roomManager, roomLog, payment
from views import close_room

from datetime import datetime
import json

try:
    roomManagerIDs = []

     roomManager.objects.all()
    for room in roomManager.objects.all():
        if room.dateLost < datetime.now().strftime('%y-%m-%d %H:%M:%S'):
            roomManagerIDs.append(room.id)

    for roomManagerID in roomManagerIDs:
        close_room(roomManagerID)
except Exception, e:
    pass