# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from models import roomManager, roomLog, payment, User

from datetime import datetime
import json

# Create your views here.
# done
def set_vote(request):
    try:
        if is_authenticated(request):
            if request.method == "GET":
                userID = request.GET['userID']
                roomManagerID = request.GET['roomManagerID']
                first_name = request.GET['first_name']
                last_name = request.GET['last_name']
                typeKleeek = request.GET['typeKleeek']
                dateKleek = datetime.now()
                user = User.objects.filter(username=userID)

                if spent_kleeek(user, typeKleeek):
                        tmpRoom = roomManager.objects.filter(id = roomManagerID).update( 
                                              ownderID = userID, 
                                              ownerName = first_name, 
                                              lastClickDate = dateKleek
                                            )
                        # tmpRoomLog = roomLog.objects.filter(roomManager = roomManagerID).update(oldOwners = (tmpRoomLog + userName))
                return HttpResponse(get_room(request))
        else:
            return HttpResponse(403)
    except Exception, e:
        return HttpResponse(0)

# done
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
                                        'image':tmpRoom.roomTypeID.image.url.replace('/',"__"),
                                        },
                        'roomPosition': str(tmpRoom.roomPosition),
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

#done
def close_rooms(request):
    try:
        managers = roomManager.objects.filter(status='active')
        for manager in managers:
            if (manager.dateLost <= datetime.today().date()):
                manager.status='close'
                manager.save()
        return get_room_list(request)
    except Exception, e:
        return HttpResponse(0)

# done
def kill_rooms(request):
    try:
        managers = roomManager.objects.filter(status='close')
        for manager in managers:
            if (manager.dateLost.day < datetime.today().date().day) or (manager.dateLost.day == 1 and datetime.today().date().day != 1):
                manager.status='kill'
                manager.save()
        return get_room_list(request)
    except Exception, e:
        return HttpResponse(0)

# done
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
                                        "image": roomManagerRec.roomTypeID.image.url.replace('/',"__"),
                                        "typeKleeek": roomManagerRec.roomTypeID.typeKleeek,
                                        },
                        "roomPosition": str(roomManagerRec.roomPosition),
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

#done
def get_user_total(request):
    try:
        structReturn = []
        if is_authenticated(request):
            userID = request.GET['userID']
            user = User.objects.filter(username=userID)
            oldPayment = payment.objects.get(userID=user)
            structReturn.append({
                'userGold': str(oldPayment.userGold),
                'userSilver': str(oldPayment.userSilver),
                'userBronze': str(oldPayment.userBronze),
            })
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

#done
def get_multiplier(typeKleeekSpent, typeKleeekAdd):
    try:
        if typeKleeekSpent==1 and typeKleeekAdd==2:
            return 10
        if typeKleeekSpent==1 and typeKleeekAdd==3:
            return 100
        if typeKleeekSpent==2 and typeKleeekAdd==1:
            return 0.1
        if typeKleeekSpent==2 and typeKleeekAdd==3:
            return 10
        if typeKleeekSpent==3 and typeKleeekAdd==1:
            return 0.01
        if typeKleeekSpent==3 and typeKleeekAdd==2:
            return 0.1
        return 1
    except Exception, e:
        return 1

#done
def conver_kleeek(request):
    try:
        if is_authenticated(request):
            userID = request.GET['userID']
            # addKleeek = abs(int(request.GET['addKleeek']))
            spentKleeek = abs(int(request.GET['spentKleeek']))
            typeKleeekAdd = abs(int(request.GET['typeKleeekAdd']))
            typeKleeekSpent = abs(int(request.GET['typeKleeekSpent']))
            user = User.objects.filter(username=userID)
            oldPayment = payment.objects.get(userID=user)
            if typeKleeekSpent==1:
                if oldPayment.userGold < spentKleeek:
                    return HttpResponse(0)
            if typeKleeekSpent==2:
                if oldPayment.userSilver < spentKleeek:
                    return HttpResponse(0)
            if typeKleeekSpent==3:
                if oldPayment.userBronze < spentKleeek:
                    return HttpResponse(0)

            spent_kleeek(user, typeKleeekSpent, spentKleeek)
            spent_kleeek(user, typeKleeekAdd, (-spentKleeek * get_multiplier(typeKleeekSpent, typeKleeekAdd))) 
            return HttpResponse(get_user_total(request))
        else:
            return HttpResponse(0)
    except Exception, e:
        return HttpResponse(0)

# done
def spent_kleeek(user, typeKleeek, countKleeek=1):
    try:
        if int(typeKleeek) == 1:
            oldGold = payment.objects.get(userID=user).userGold
            newGold = oldGold - countKleeek
            if newGold >= 0:
                payment.objects.filter(userID=user).update(userGold=newGold)
                return True
        if int(typeKleeek) == 2:
            oldSilver = payment.objects.get(userID=user).userSilver
            newSilver = oldSilver - countKleeek
            if newSilver >= 0:
                payment.objects.filter(userID=user).update(userSilver=newSilver)
                return True
        if int(typeKleeek) == 3:
            oldBronze = payment.objects.get(userID=user).userBronze
            newBronze = oldBronze - countKleeek
            if newBronze >= 0:
                payment.objects.filter(userID=user).update(userBronze=newBronze)
                return True
        return False
    except Exception, e:
        return False

#done
def set_day_bonus(request):
    try:
        payment.objects.update(dayBonus=1)
        return HttpResponse(1)
    except Exception, e:
        return HttpResponse(0)
#done
def set_bonus(request):
    try:
        if is_authenticated(request):
            userID = request.GET['userID']
            user = User.objects.filter(username=userID)
            oldPayment = payment.objects.get(userID=user)
            oldBronze = oldPayment.userBronze
            oldDayBonus = oldPayment.dayBonus
            if oldDayBonus == 1:
                payment.objects.filter(userID=user).update(dayBonus=0)
                payment.objects.filter(userID=user).update(userBronze=(oldBronze+3))
                return HttpResponse(get_user_total(request))
        return HttpResponse(0)
    except Exception, e:
        return HttpResponse(0)

# done
def structReturnFormat(structReturn):
    return str(structReturn).replace("u'","'").replace("'",'"')

def sell_kleeek(request):
    if request.user.is_authenticated():
        return HttpResponse(1)
    else:
        return HttpResponse(0)

# done
def is_authenticated(request):
    try:
        userID = request.GET['userID']
        if True:#request.META['HTTP_REFERER']=='http://vk.com/app3985490_17193680':
            if User.objects.filter(username=userID):
                return True
            else:
                first_name = request.GET['first_name']
                last_name = request.GET['last_name']
                user = User.objects.create( username=userID, 
                                            password='PBKDF2PasswordHasher', 
                                            first_name=first_name,
                                            last_name=last_name)
                paymentObj = payment.objects.create(userID=user,userGold=0,userSilver=0,userBronze=3,dayBonus=0)
                user.save()
                paymentObj.save()
                return True
        else:
            return False
    except Exception, e:
        return False