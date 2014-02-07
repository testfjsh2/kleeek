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
                return HttpResponse(userID)
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

# done
def close_room(roomManagerID):
    try:
        # if request.user.is_authenticated():
        roomManager.objects.filter(id=roomManagerID).update(status='close')
        return get_room_list(0)
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
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        if request.META['REMOTE_HOST']=='vk.com':
            if User.objects.filter(username=userID):
                return True
            else:
                user = User.objects.create( username=userID, 
                                            password='PBKDF2PasswordHasher', 
                                            first_name=first_name,
                                            last_name=last_name)
                paymentObj = payment.objects.create(userID=user,userGold=0,userSilver=0,userBronze=0,dayBonus=0)
                user.save()
                paymentObj.save()
                return True
            return False
    except Exception, e:
        return False