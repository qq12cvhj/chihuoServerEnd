# coding=utf-8
import re
from operator import or_, and_

from flask import Blueprint, json
from chihuo.views import SERVER_IP
from ..dbModels import action, user, food, share, watch
from ..dbConnect import db_session


aboutFriends = Blueprint('aboutFriends', __name__)


def getShrImgStr(shrId):
    try:
        shr = db_session.query(share).filter(share.shareId == shrId).first()
        imgList = re.findall(r"<img src=\"(.*?)\.jpg", shr.shareDetail)
        if imgList == []:
            return str(SERVER_IP + "static/imgsUpload/chihuo.png")
        else:
            return str(imgList[0] + ".jpg")
    except Exception, e:
        return str(SERVER_IP + "static/imgsUpload/chihuo.png")


def action2json(a):
    subject = db_session.query(user).filter(user.userId == a.subjectId).first()
    subjectName = subject.nickName
    subjectId = subject.userId
    if a.actionType == 1 or a.actionType == 3:
        actionob = db_session.query(food).filter(food.foodId == a.objectId).first()
        objectName = actionob.foodName
        objectId = actionob.foodId
        imgList = re.findall(r"/imgsUpload/(.*?)\.jpg", actionob.foodDetail)
        if imgList == []:
            titleImg = SERVER_IP + "static/imgsUpload/chihuo.png"
        else:
            titleImg = SERVER_IP + "static/imgsUpload/" + imgList[0] + ".jpg"
    elif a.actionType == 2:
        actionob = db_session.query(share).filter(share.shareId == a.objectId).first()
        objectName = actionob.shareTitle
        objectId = actionob.shareId
        imgList = re.findall(r"<img src=\"(.*?)\.jpg", actionob.shareDetail)
        if imgList == []:
            titleImg = SERVER_IP + "static/imgsUpload/chihuo.png"
        else:
            titleImg = imgList[0] + ".jpg"
    return {
        "subjectName": subjectName,
        "objectName": objectName,
        "titleImg": titleImg,
        "actionType": a.actionType,
        "actionTime": str(a.actionTime),
        "subjectId": subjectId,
        "objectId": objectId
    }


@aboutFriends.route("/getHomeActionList")
def getHomeActionList():
    aJsonList = []
    try:
        actionList = db_session.query(action).filter(or_(action.actionType == 1, action.actionType == 2)).limit(5).all()
        actionList.sort(key=lambda x: x.actionTime, reverse=True)
        for a in actionList:
            aJsonList.append(action2json(a))
    except Exception, e:
        print e
    print json.dumps(aJsonList)
    return json.dumps(aJsonList)


@aboutFriends.route("/getActionList<usrid>")
def getActionList(usrid):
    aJsonList = []
    try:
        actionList = []
        watchs = db_session.query(watch).filter(watch.userId == usrid).all()
        userIds = []
        for w in watchs:
            userIds.append(w.watchedId)
        for uid in userIds:
            actionList.extend(db_session.query(action).filter(action.subjectId == uid).all())
        actionList.extend(db_session.query(action).filter(action.subjectId == usrid))
        actionList.sort(key=lambda x: x.actionTime, reverse=True)
        for a in actionList:
            aJsonList.append(action2json(a))
    except Exception, e:
        aJsonList = []
        print e
    print "动态列表为：" + json.dumps(aJsonList)
    return json.dumps(aJsonList)


@aboutFriends.route("/watchStatus<watchedId>/<userId>")
def watchStatus(watchedId, userId):
    try:
        status = db_session.query(watch).filter(watch.watchedId == watchedId, watch.userId == userId).first()
        if status == None:
            return "0"
        else:
            return "1"
    except Exception, e:
        print e
        return "0"


@aboutFriends.route("/watchOrCancel<watchedId>/<userId>")
def watchOrCancel(watchedId, userId):
    try:
        status = db_session.query(watch).filter(watch.watchedId == watchedId, watch.userId == userId).first()
        if status == None:
            newwatch = watch(watchedId, userId)
            db_session.add(newwatch)
            db_session.commit()
            db_session.close()
            print "watch"
        else:
            try:
                db_session.delete(status)
                db_session.commit()
                db_session.close()
                print "cancel"
            except Exception, e1:
                print e1
    except Exception, e2:
        print e2
    return ""


@aboutFriends.route("/getimgs/<userId>")
def getimgs(userId):
    imglist = []
    try:
        shrlist = db_session.query(share).filter(share.shareAuthorId == userId).all()
        if len(shrlist) > 3:
            shrlist = shrlist[1: 3]
        for s in shrlist:
            imglist.append(
                {
                    "imgid": s.shareId,
                    "imgstr": getShrImgStr(s.shareId)
                })
    except Exception, e:
        print e
    print json.dumps(imglist)
    return json.dumps(imglist)
