import re
from flask import Blueprint, json
from chihuo.views import SERVER_IP
from ..dbModels import action, user, food, share
from ..dbConnect import db_session

aboutFriends = Blueprint('aboutFriends', __name__)


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
        imgList = re.findall(r"src=\"(.*?)\.jpg", actionob.shareDetail)
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


@aboutFriends.route("/getActionList")
def getActionList():
    aJsonList = []
    try:
        actionList = db_session.query(action).all()
        for a in actionList:
            aJsonList.append(action2json(a))
    except Exception, e:
        print e
    print json.dumps(aJsonList)
    return json.dumps(aJsonList)
