# coding=utf-8
import os

import datetime
import time
import random
from flask import Blueprint, render_template, request, Response, json, jsonify
from ..dbModels import food, user, foodType,foodStar
from ..dbConnect import db_session

aboutCookbook = Blueprint('aboutCookbook', __name__)


@aboutCookbook.route('/editCookbook', methods=['GET'])
def editCookbook():
    foodTypeList = getFoodTypeLIst()
    return render_template('cookbookEdit.html', title='编辑菜谱', foodTypeList=foodTypeList)



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
    try:
        db_session.add(newfood)
        db_session.commit()
        db_session.close()
        # foodTypeList = getFoodTypeLIst()
        # return render_template('cookbookEdit.html', title='编辑菜谱',foodTypeList = foodTypeList)
        return "<script>alert('创建成功，请返回上一层');</script>"
    except Exception, e:
        print e
        return "<script>alert('创建失败，菜品已存在。请退出重试');</script>"


@aboutCookbook.route("/getFoodInfo<foodId>")
def getfoodInfo(foodId):
    foodInfos = db_session.query(food).filter(food.foodId == foodId).all()
    if foodInfos == []:
        return "<script>alert('请求失败,请重试');</script>"
    else:
        foodInfo = foodInfos[0]
        authorId = foodInfo.foodAuthorId
        authorName = db_session.query(user).filter(user.userId == authorId).all()[0].nickName
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


def foodtype2json(ft):
    return {
        "foodTypeId": ft.foodTypeId,
        "foodTypeName": ft.foodTypeName,
        "foodTypeDesc": ft.foodTypeDesc
    }
def food2json(f):
    foodAuthor = db_session.query(user).filter(user.userId == f.foodAuthorId).first().nickName
    return {
        "foodId":f.foodId,
        "foodAuthor":foodAuthor,
        "foodName":f.foodName
    }
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

aboutCookbook.route("/getStarCount<foodId>", methods = ['GET'])
def getStarCount(foodId):
    return None

@aboutCookbook.route("/starStatus<foodId>/<userId>",methods=['GET'])
def starStatus(foodId,userId):
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
def starOrCancel(foodId,userId):
    try:
        status = db_session.query(foodStar).filter(foodStar.userId == userId, foodStar.foodId == foodId).first()
        if status == None:
            fs = foodStar(userId,foodId)
            db_session.add(fs)
            db_session.commit()
            db_session.close()
            print 1
            return "1"
        else:
            db_session.delete(status)
            db_session.commit()

            db_session.close()
            print 0
            return "0"
    except Exception,e:
        print e
        return "-1"
