from operator import or_

import re
from flask import Blueprint, json,render_template

from chihuo.views import SERVER_IP
from ..dbModels import user, action, food, share
from ..dbConnect import db_session

aboutHome = Blueprint('aboutHome', __name__)


@aboutHome.route("/")
def index():
    return render_template('index.html')

@aboutHome.route("/getHotUserList", methods=['GET'])
def getHotUserList():
    uJsonList = []
    try:
        userList = db_session.query(user).all()
        for u in userList:
            uJsonList.append(hotUser2Json(u))
    except Exception, e:
        print e
        uJsonList = []
    print json.dumps(uJsonList)
    return json.dumps(uJsonList)


def hotUser2Json(u):
    return {
        "userid": u.userId,
        "nickname": u.nickName,
        "imgList": getUserImgs(u.userId)
    }


def getUserImgs(id):
    imgList = []
    try:
        actions = db_session.query(action).filter(action.subjectId == id,
                                                  or_(action.actionType == 1, action.actionType == 2)).all()
        print len(actions)
        if len(actions) > 3:
            print "???"
            actions = actions[1:3]
        for a in actions:
            if a.actionType == 1:
                actionob = db_session.query(food).filter(food.foodId == a.objectId).first()
                jpglist = re.findall(r"/imgsUpload/(.*?)\.jpg", actionob.foodDetail)
                if jpglist == []:
                    imgList.append(SERVER_IP + "static/imgsUpload/chihuo.png")
                else:
                    imgList.append(SERVER_IP + "static/imgsUpload/" + jpglist[0] + ".jpg")
            elif a.actionType == 2:
                actionob = db_session.query(share).filter(share.shareId == a.objectId).first()
                jpglist = re.findall(r"src=\"(.*?)\.jpg", actionob.shareDetail)
                if jpglist == []:
                    imgList.append(SERVER_IP + "static/imgsUpload/chihuo.png")
                else:
                    imgList.append(jpglist[0] + ".jpg")
    except Exception, e:
        print e
        imgList = []
    return imgList
