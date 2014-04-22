# -*- coding: utf-8 -*-
import json
from websocket import create_connection
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from models import roomManager, roomLog, payment, User, orderTab

from datetime import datetime

def SockResponse(msg):
    ws = create_connection("ws://127.0.0.1:8888/chatsocket")
    ws.send(msg)

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
                currentManager = roomManager.objects.filter(id = roomManagerID)

                if spent_kleeek(user, typeKleeek):
                        tmpRoom = roomManager.objects.filter(id = roomManagerID).update( 
                                              ownderID = userID, 
                                              ownerName = first_name,
                                              ownerLastName = last_name,
                                              lastClickDate = dateKleek
                                            )
                        # tmpRoomLog = roomLog.objects.filter(roomManager = roomManagerID).update(oldOwners = (tmpRoomLog + userName))
                        log_statistic(currentManager, user, dateKleek)
                return HttpResponse(get_room(request))
        else:
            return HttpResponse(403)
    except Exception, e:
        return HttpResponse(0)

# done
def get_room(request):
    structReturn = []
    try:
        # if is_authenticated(request):
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
                        'ownerLastName' : tmpRoom.ownerLastName,
                        'lastClickDate' : tmpRoom.lastClickDate.strftime('%Y-%m-%d %H:%M:%S'),
                        'status' : tmpRoom.status,
                        'oldOwners': get_statistic(tmpRoom.roomlog.oldOwners) if hasattr(tmpRoom, 'roomlog') else [],
                    })
                SockResponse(structReturnFormat(structReturn))
                return HttpResponse(structReturnFormat(structReturn))
        # else:
            # return HttpResponse(403)
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
        roomManagerList = roomManager.objects.filter(status='active') | roomManager.objects.filter(status='close')
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
        # SockResponse(structReturnFormat(structReturn))
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
                "userGold": str(oldPayment.userGold),
                "userSilver": str(oldPayment.userSilver),
                "userBronze": str(oldPayment.userBronze),
                "dayBonus": str(oldPayment.dayBonus),
            })
            return HttpResponse(structReturnFormat(structReturn))
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

# done
def structReturnFormat(structReturn):
    return str(structReturn).replace("u'","'").replace("'",'"')

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
                payment.objects.filter(userID=user).update(userBronze=(oldBronze+1))
                return HttpResponse(get_user_total(request))
        return HttpResponse(0)
    except Exception, e:
        return HttpResponse(0)

#done
def set_wall_post_bonus(request):
    userID = request.GET['userID']
    user = User.objects.filter(username=userID)
    oldPayment = payment.objects.get(userID=user)
    oldBronze = oldPayment.userBronze
    wallPostBonus = oldPayment.wallPostBonus
    if wallPostBonus == 1:
        payment.objects.filter(userID=user).update(wallPostBonus=0)
        payment.objects.filter(userID=user).update(userBronze=(oldBronze+1))
    return HttpResponse(get_user_total(request))

def uncheck_friend_list_count(request):
    try:
        if is_authenticated(request):
            userID = request.GET['userID']
            user = User.objects.filter(username=userID)
            payment.objects.filter(userID=user).update(oldFriendsCount=0)
            return HttpResponse(1)
    except Exception, e:
        return HttpResponse(0)

    

#NOT DON. NEED FAST!
def set_friend_bonus(request):
    try:
        userID = request.GET['userID']
        friendsList = request.GET['friendsList']
        if is_authenticated(request):
            if  friendsList:
                friendsList = friendsList[1:-1].split(',')
                user = User.objects.filter(username=userID)
                oldFrindsList = payment.objects.get(userID=user).friendsList
                for friendID in friendsList:
                    if friendID not in oldFrindsList:
                        friend = User.objects.filter(username=friendID)
                        if friend:
                            friend = friend[0]
                            #check the register's dates
                            if friend.date_joined.__ge__(user[0].date_joined):
                                oldBronze = payment.objects.get(userID=user).userBronze
                                oldFrindsList = payment.objects.get(userID=user).friendsList
                                oldFriendsCount = payment.objects.get(userID=user).friendsCount
                                payment.objects.filter(userID=user).update(userBronze=(oldBronze+1))
                                payment.objects.filter(userID=user).update(friendsList=oldFrindsList[:-1] + friendID + ',]')
                                payment.objects.filter(userID=user).update(friendsCount=oldFriendsCount+1)
                return HttpResponse(get_user_total(request))
    except Exception, e:
        return HttpResponse(0)

def check_sign(request):
    return True

#done
def get_price(typeKleeek, countKleeek):
    price = 0
    if typeKleeek == 2:
        price = countKleeek
    if typeKleeek == 1:
        if countKleeek<=5:
            price = countKleeek * 10
        if countKleeek == 11:
            price = 100
        if countKleeek==28:
            price = 250
        if countKleeek == 60:
            price = 500
    return price

@method_decorator(csrf_exempt)
def sell_kleeek(request):
    if check_sign(request):
        returnMsg = {}
        erMsg = {}

        try:
            notification_type = request.POST['notification_type']
            itemFormat = request.POST['item'].replace('&quot;', '"');
            kleeekSell = json.loads(itemFormat)
            username = request.POST['user_id']
        except Exception, e:
            returnMsg["error"] = {
                "error_code": 11,
                "error_msg": 'incorrect request. check the item:' + itemFormat,
                "critical": True,
            }
            return HttpResponse(structReturnFormat(returnMsg))

        if notification_type == 'get_item':
            if kleeekSell['type'] == '1':
                returnMsg['response'] = {
                    "item_id": '1_' + kleeekSell['cnt'],
                    "title": kleeekSell['cnt'] + ' Gold Kleeek',
                    "photo_url": '',
                    "price": get_price(1, int(kleeekSell['cnt'])),
                }

            if kleeekSell['type'] == '2':
                returnMsg['response'] = {
                    "item_id": '2_' + kleeekSell['cnt'],
                    "title": kleeekSell['cnt'] + ' Silver Kleeek',
                    "photo_url": '',
                    "price": get_price(2, int(kleeekSell['cnt'])),
                }

        elif notification_type == 'get_item_test':
            if kleeekSell['type'] == '1':
                returnMsg['response'] = {
                    "item_id": '1_' + kleeekSell['cnt'],
                    "title": kleeekSell['cnt'] + ' Gold Kleeek(test mode)',
                    "photo_url": '',
                    "price": get_price(1, int(kleeekSell['cnt'])),
                }
            if kleeekSell['type'] == '2':
                returnMsg['response'] = {
                    "item_id": '2_' + kleeekSell['cnt'],
                    "title": kleeekSell['cnt'] + ' Silver Kleeek(test mode)',
                    "photo_url": '',
                    "price": get_price(2, int(kleeekSell['cnt'])),
                }

        elif notification_type == 'order_status_change':
            try:
                order_id = request.POST['order_id']
                user_id = request.POST['user_id']

                orderRow = orderTab.objects.create(order_id=order_id,user_id=user_id)
                orderRow.save()
                user = User.objects.filter(username=username)
                spent_kleeek(user, kleeekSell['type'], -int(kleeekSell['cnt']))
                returnMsg['response'] = {
                    "order_id": order_id,
                }
            except Exception, e:
                returnMsg["error"] = {
                    "error_code": 11,
                    "error_msg": 'incorrect request',
                    "critical": True,
                }

        elif notification_type == 'order_status_change_test':
            try:
                order_id = request.POST['order_id']
                user_id = request.POST['user_id']

                orderRow = orderTab.objects.create(order_id=order_id,user_id=user_id)
                orderRow.save()
                user = User.objects.filter(username=username)
                spent_kleeek(user, kleeekSell['type'], -int(kleeekSell['cnt']))
                returnMsg['response'] = {
                    "order_id": order_id,
                }
            except Exception, e:
                returnMsg["error"] = {
                    "error_code": 100,
                    "error_msg": 'write database error',
                    "critical": True,
                }
        else:
            returnMsg["error"] = {
                "error_code": 101,
                "error_msg": 'unknow notification type',
                "critical": True,
            }
        return HttpResponse(structReturnFormat(returnMsg))

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
                paymentObj = payment.objects.create(userID=user,userGold=1000,userSilver=1000,userBronze=3000,dayBonus=1, wallPostBonus=1,friendsList='[]')
                user.save()
                paymentObj.save()
                return True
        else:
            return False
    except Exception, e:
        return False

#done
def log_statistic(currentManagers, users, dateKleek):
    try:
        for currentManager in currentManagers:
            for user in users:
                if not hasattr(currentManager, 'roomlog'):
                    roomLog.objects.create(roomManager = currentManager,
                                           oldOwners = '')
                oldOwners = currentManager.roomlog.oldOwners
                currentManager.roomlog.oldOwners = oldOwners + '{"username":"%s", "firstLast" : "%s" ,"dateKleek": "%s"}&&&' % (
                               user.username, user.first_name + " " + user.last_name, dateKleek)
                currentManager.roomlog.save()
    except Exception, e:
        raise e

#done
def get_statistic(statSring):
    try:
        statsList = statSring.strip()[:-3].split('&&&')
        jsonStatistic = []
        for statList in statsList[-9:]:
            jsonStatistic.append(json.loads(statList))
        return jsonStatistic
    except Exception, e:
        return []
