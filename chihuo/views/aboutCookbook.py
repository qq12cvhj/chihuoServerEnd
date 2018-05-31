# coding=utf-8
import os

import datetime
import random

import re
from flask import Blueprint, render_template, request, Response, json, jsonify

from chihuo.views import SERVER_IP
from ..dbModels import food, user, foodType, foodStar, action
from ..dbConnect import db_session
from sqlalchemy import func

datetimeRegx = '%Y-%m-%d %H:%M:%S'
aboutCookbook = Blueprint('aboutCookbook', __name__)


@aboutCookbook.route('/editCookbook', methods=['GET'])
def editCookbook():
    foodTypeList = getFoodTypeLIst()
    return render_template('cookbookEdit.html', title='编辑菜谱', foodTypeList=foodTypeList, serverip=SERVER_IP)


def getRandFilename():
    today = datetime.date.today()
    randomstr = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba987654321', 10))
    return str(today.year) + str(today.month) + str(today.day) + randomstr


@aboutCookbook.route("/upload", methods=["POST"])
def GetImage():
    file = request.files['wangEditorMobileFile']
    if file == None:
        return "error|file is not exist"
    else:
        try:
            filename = getRandFilename() + '.jpg'
            print os.path.isdir('chihuo/static/imgsUpload/')
            if not os.path.isdir('chihuo/static/imgsUpload/'):
                os.mkdir('chihuo/static/imgsUpload')
            file.save(os.path.join('chihuo/static/imgsUpload/', filename))
            result = os.path.join('/static', 'imgsUpload/', filename)
            res = Response(result)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res
        except Exception, e:
            print(e)
            return "error|" + str(e)


def getFoodTypeLIst():
    foodTypeList = db_session.query(foodType).all()
    return foodTypeList


@aboutCookbook.route('/createNewFood', methods=['POST'])
def createNewFood():
    foodName = request.form['foodNameInput']
    foodDetail = request.form['foodDetailInput']
    foodAuthorId = int(request.form['foodAuthorIdInput'])
    foodTypeId = request.form['foodTypeIdInput']
    print foodName
    print foodDetail
    print type(foodAuthorId)
    print foodTypeId
    newfood = food(foodName, foodAuthorId, foodTypeId, foodDetail)
    actiontime = datetime.datetime.now().strftime(datetimeRegx)
    try:
        db_session.add(newfood)
        db_session.commit()
        try:
            newid = db_session.query(func.max(food.foodId)).first()[0]
            print newid
            newAction = action(1, foodAuthorId, newid, actiontime)
            db_session.add(newAction)
            db_session.commit()
        except Exception, e1:
            print e1
        db_session.close()
        # foodTypeList = getFoodTypeLIst()
        # return render_template('cookbookEdit.html', title='编辑菜谱',foodTypeList = foodTypeList)
        return "<script>alert('创建成功，请返回上一层');</script>"
    except Exception, e:
        print e
        return "<script>alert(" + e + ");</script>"



@aboutCookbook.route("/getFoodInfo<foodId>")
def getfoodInfo(foodId):
    foodInfo = db_session.query(food).filter(food.foodId == foodId).first()
    if foodInfo == None:
        return "<script>alert('请求失败,请重试');</script>"
    else:
        authorId = foodInfo.foodAuthorId
        authorName = db_session.query(user).filter(user.userId == authorId).first().nickName
        foodInfo.hotIndex += 10
        db_session.commit()
        return render_template('foodInfoShow.html', foodInfo=foodInfo, authorName=authorName)


@aboutCookbook.route("/addNewFoodType", methods=['POST'])
def addNewFoodType():
    foodTypeInput = request.form['foodTypeInput']
    foodDescInput = request.form['foodDescInput']
    print foodTypeInput
    print foodDescInput
    newFoodType = foodType(foodTypeInput, foodDescInput)
    try:
        db_session.add(newFoodType)
        db_session.commit()
        db_session.close()
        return "0"
    except Exception, e:
        print e
        return "-1"


def getfoodCoverimg(f):
    imgList = re.findall(r"/imgsUpload/(.*?)\.jpg", f.foodDetail)
    if imgList == []:
        return SERVER_IP + "static/imgsUpload/chihuo.png"
    else:
        return SERVER_IP + "static/imgsUpload/" + imgList[0] + ".jpg"


def foodtype2json(ft):
    return {
        "foodTypeId": ft.foodTypeId,
        "foodTypeName": ft.foodTypeName,
        "foodTypeDesc": ft.foodTypeDesc
    }


def food2json(f):
    foodAuthor = db_session.query(user).filter(user.userId == f.foodAuthorId).first().nickName
    return {
        "foodId": f.foodId,
        "foodAuthor": foodAuthor,
        "foodName": f.foodName,
        "foodAuthorId": f.foodAuthorId,
        "foodImgSrc": getfoodCoverimg(f),
        "starCount": f.starCount
    }


@aboutCookbook.route("/getNewFoodList")
def getNewFoodList():
    foodlist = db_session.query(food).limit(10).all()
    foodlist.sort(key=lambda x: x.foodId, reverse=True)
    foodJsonList = []
    for f in foodlist:
        foodJsonList.append(food2json(f))
    print json.dumps(foodJsonList)
    return json.dumps(foodJsonList)


@aboutCookbook.route("/getHotFoodList")
def getHotFoodList():
    foodlist = db_session.query(food).limit(10).all()
    foodlist.sort(key=lambda x: x.starCount, reverse=True)
    foodJsonList = []
    for f in foodlist:
        foodJsonList.append(food2json(f))
    print json.dumps(foodJsonList)
    return json.dumps(foodJsonList)


@aboutCookbook.route("/getDesignList<authorId>")
def getDesignList(authorId):
    foodList = db_session.query(food).filter(food.foodAuthorId == authorId).all()
    foodJsonList = []
    for f in foodList:
        foodJsonList.append(food2json(f))
    print json.dumps(foodJsonList)
    return json.dumps(foodJsonList)


@aboutCookbook.route("/getFavoList<authorId>")
def getFavoList(authorId):
    foodList = db_session.query(food).filter(foodStar.foodId == food.foodId, foodStar.userId == authorId).all()
    foodJsonList = []
    for f in foodList:
        foodJsonList.append(food2json(f))
    print json.dumps(foodJsonList)
    return json.dumps(foodJsonList)


@aboutCookbook.route("/getFoodList<typeId>")
def getFoodList(typeId):
    foodList = db_session.query(food).filter(food.foodTypeId == typeId).all()
    foodJsonList = []
    for f in foodList:
        foodJsonList.append(food2json(f))
    print json.dumps(foodJsonList)
    return json.dumps(foodJsonList)


@aboutCookbook.route("/getFoodTypeList")
def foodTypeList():
    foodTypeList = getFoodTypeLIst()
    typeJsonList = []
    for type in foodTypeList:
        typeJsonList.append(foodtype2json(type))
    print json.dumps(typeJsonList)
    print typeJsonList
    return json.dumps(typeJsonList)


aboutCookbook.route("/getStarCount<foodId>", methods=['GET'])


def getStarCount(foodId):
    return None


@aboutCookbook.route("/starStatus<foodId>/<userId>", methods=['GET'])
def starStatus(foodId, userId):
    try:
        status = db_session.query(foodStar).filter(foodStar.userId == userId, foodStar.foodId == foodId).first()
        if status == None:
            print 0
            return "0"
        else:
            print 1
            return "1"
    except Exception, e:
        print e
        return "0"


@aboutCookbook.route("/starOrCancel<foodId>/<userId>")
def starOrCancel(foodId, userId):
    try:
        status = db_session.query(foodStar).filter(foodStar.userId == userId, foodStar.foodId == foodId).first()
        if status == None:
            fs = foodStar(userId, foodId)
            actiontime = datetime.datetime.now().strftime(datetimeRegx)
            newaction = action(3, userId, foodId, actiontime)
            db_session.query(food).filter(food.foodId == foodId).update({food.starCount: food.starCount + 1})
            db_session.add(fs)
            db_session.add(newaction)
            db_session.commit()
            db_session.close()
            print 1
            return "1"
        else:
            try:
                db_session.query(food).filter(food.foodId == foodId).update({food.starCount: food.starCount - 1})
                delaction = db_session.query(action) \
                    .filter(action.subjectId == userId, action.objectId == foodId, action.actionType == 3) \
                    .first()
                db_session.delete(delaction)
            except Exception, e1:
                print e1
            db_session.delete(status)
            db_session.commit()
            db_session.close()
            print 0
            return "0"
    except Exception, e:
        print e
        return "-1"
