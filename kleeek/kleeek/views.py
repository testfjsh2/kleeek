from django.shortcuts import render
from django.http import HttpResponse
from models import roomManager, roomLog, payment

from datetime import datetime
import json

# Create your views here.
# all right
def set_vote(request):
    try:
        if request.user.is_authenticated():
            if request.method == "GET":
                userID = request.GET['userID']
                roomManagerID = request.GET['roomManagerID']
                userName = request.GET['userName']
                typeKleeek = request.GET['typeKleeek']

                dateKleek = datetime.now().strftime('%y-%m-%d %H:%M:%S')

                if spent_kleeek(userID, typeKleeek):
                        tmpRoom = roomManager.objects.filter(id = roomManagerID).update( 
                                              ownderID = userID, 
                                              ownerName = userName, 
                                              lastClickDate = dateKleek
                                            )
                        tmpRoomLog = roomLog.objects.filter(roomManager = roomManagerID).update(oldOwners = (tmpRoomLog + userName))
                return HttpResponse(userID)
    except Exception, e:
        return HttpResponse(0)

# all right
def get_room(request):
    structReturn = []
    try:
        # if request.user.is_authenticated():
            # if request.method == "GET":
                roomManagerID = request.GET['roomManagerID']
                tmpRoom = roomManager.objects.get(id=roomManagerID)
                structReturn.append({
                        'roomManagerID': str(tmpRoom.id),
                        'roomTypeID' : {'id': str(tmpRoom.roomTypeID.id),
                                        'name': tmpRoom.roomTypeID.name,
                                        'image':tmpRoom.roomTypeID.image.replace('/',"__"),
                                        },
                        'dateCreate' : tmpRoom.dateCreate.strftime('%Y-%m-%d %H:%M:%S'),
                        'dateLost' : tmpRoom.dateLost.strftime('%Y-%m-%d %H:%M:%S'),
                        'ownderID' : str(tmpRoom.ownderID),
                        'ownerName' : tmpRoom.ownerName,
                        'lastClickDate' : tmpRoom.lastClickDate.strftime('%Y-%m-%d %H:%M:%S'),
                        'status' : tmpRoom.status,
                    })
                return HttpResponse(structReturnFormat(structReturn))
    except Exception, e:
        return HttpResponse(0)

def close_room(roomManagerID):
    try:
        if request.user.is_authenticated():
            roomManager.objects.filter(id=roomManagerID).update(status='close')
            return get_room_list(request)
    except Exception, e:
        return HttpResponse(0)

# all right
def get_room_list(request):
    structReturn = []
    try:
        # if request.user.is_authenticated():
            # if request.method == "GET":
                roomManagerList = roomManager.objects.filter(status='active')
                for roomManagerRec in roomManagerList:
                    structReturn.append({
                        "roomManagerID": str(roomManagerRec.id),
                        "roomTypeID" : {"id": str(roomManagerRec.roomTypeID.id),
                                        "name": roomManagerRec.roomTypeID.name,
                                        "image":roomManagerRec.roomTypeID.image.replace('/',"__"),
                                        },
                        "dateCreate" : roomManagerRec.dateCreate.strftime('%Y-%m-%d %H:%M:%S'),
                        "dateLost" : roomManagerRec.dateLost.strftime('%Y-%m-%d %H:%M:%S'),
                        "ownderID" : str(roomManagerRec.ownderID),
                        "ownerName" : roomManagerRec.ownerName,
                        "lastClickDate" : roomManagerRec.lastClickDate.strftime('%Y-%m-%d %H:%M:%S'),
                        "status" : roomManagerRec.status,
                        })
                return HttpResponse(structReturnFormat(structReturn))
            # return HttpResponse(403)
    except Exception, e:
        return HttpResponse(500)

def get_user_total(request, userID=0):
    try:
        if request.user.is_authenticated():
            if userID:
                userID = request.GET['userID']
            oldPayment = payment.objects.get(userID=userID)
            structReturn = {
                'userID': userID,
                'userGold': oldPayment.userGold,
                'userSilver': oldPayment.userSilver,
                'userBronze': oldPayment.userBronze,
            }
            return HttpResponse(structReturn)
    except Exception, e:
        return HttpResponse(0)

def get_users_total(request):
    try:
        if request.user.is_authenticated():
            structReturn = []
            userPayments = payment.objects.all()
            for userPayment in userPayments:
                structReturn.append( get_user_total(request, userPayment.userID) )
            return HttpResponse(structReturn)
    except Exception, e:
        return HttpResponse(0)

def conver_kleeek(request):
    try:
        if request.user.is_authenticated():
            userID = request.GET['userID']
            addKleeek = request.GET['addKleeek']
            spentKleeek = request.GET['spentKleeek']
            typeKleeekAdd = request.GET['typeKleeekAdd']
            typeKleeekSpent = request.GET['typeKleeekSpent']

            oldPayment = payment.objects.get(userID=userID)
            if typeKleeekSpent==1:
                if oldPayment.userGold < spentKleeek:
                    return HttpResponse(0)
            if typeKleeekSpent==2:
                if oldPayment.userSilver < spentKleeek:
                    return HttpResponse(0)
            if typeKleeekSpent==3:
                if oldPayment.userBronze < spentKleeek:
                    return HttpResponse(0)

            spent_kleeek(userID, typeKleeekSpent, spentKleeek)
            spent_kleeek(userID, typeKleeekAdd, (-addKleeek)) 
            return HttpResponse(1)
        else:
            return HttpResponse(0)
    except Exception, e:
        return HttpResponse(0)

def spent_kleeek(userID, typeKleeek, countKleeek=1):
    try:
        if int(typeKleeek) == 1:
            oldGold = payment.objects.get(userID=userID).userGold
            newGold = oldGold - countKleeek
            payment.objects.filter(userID=userID).update(userGold=newGold)
            return HttpResponse(1)
        if int(typeKleeek) == 2:
            oldSilver = payment.objects.get(userID=userID).userSilver
            newSilver = oldSilver - countKleeek
            payment.objects.filter(userID=userID).update(userSilver=newSilver)
            return HttpResponse(1)
        if int(typeKleeek) == 3:
            oldBronze = payment.objects.get(userID=userID).userBronze
            newBronze = oldBronze - countKleeek
            payment.objects.filter(userID=userID).update(userBronze=newBronze)
            return HttpResponse(1)
    except Exception, e:
        return HttpResponse(0)

def set_day_bonus(request):
    try:
        if request.user.is_authenticated():
            userID = request.GET['userID']
            oldPayment = payment.objects.get(userID=userID)
            if oldPayment.dayBonus != '':
                payment.objects.filter(userID=userID).update(userBronze=(oldPayment.userBronze+1))
    except Exception, e:
        return HttpResponse(0)

def set_bonus():
    try:
        if request.user.is_authenticated():
            userID = request.GET['userID']
            oldPayment = payment.objects.get(userID=userID)
            payment.objects.filter(userID=userID).update(userBronze=(oldPayment.userBronze+1))
    except Exception, e:
        return HttpResponse(0)

def structReturnFormat(structReturn):
    return str(structReturn).replace("u'","'").replace("'",'"')

def sell_kleeek(request):
    if request.user.is_authenticated():
        return HttpResponse(1)
    else:
        return HttpResponse(0)