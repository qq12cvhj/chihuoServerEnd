#coding=utf-8
import os

import datetime
import time
import random
from flask import Blueprint, render_template, request, Response
from ..dbModels import food,user,foodType
from ..dbConnect import db_session
aboutCookbook = Blueprint('aboutCookbook',__name__)

@aboutCookbook.route('/editCookbook',methods=['GET'])
def editCookbook():
    return render_template('cookbookEdit.html',title='编辑菜谱')

def getRandFilename():
    today = datetime.date.today()
    randomstr = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba987654321', 10))
    return str(today.year) + str(today.month) + str(today.day) + randomstr

@aboutCookbook.route("/upload",methods = ["POST"])
def GetImage():
        file = request.files['wangEditorMobileFile']
        if file == None:
            return "error|file is not exist"
        else:
                try:
                    filename = getRandFilename()+'.jpg'
                    print os.path.isdir('chihuo/static/imgsUpload/')
                    if not os.path.isdir('chihuo/static/imgsUpload/'):
                        os.mkdir('chihuo/static/imgsUpload')
                    file.save(os.path.join('chihuo/static/imgsUpload/',filename))
                    result = os.path.join('/static','imgsUpload/',filename)
                    res =  Response(result)
                    res.headers["ContentType"] = "text/html"
                    res.headers["Charset"] = "utf-8"
                    return res
                except Exception,e:
                    print(e)
                    return "error|"+str(e)

@aboutCookbook.route('/createNewFood',methods=['POST'])
def createNewFood():
    foodName = request.form['foodNameInput']
    foodDetail = request.form['foodDetailInput']
    foodAuthorId = int(request.form['foodAuthorIdInput'])
    foodTypeId = request.form['foodTypeIdInput']
    print foodName
    print foodDetail
    print type(foodAuthorId)
    print foodTypeId
    newfood = food(foodName,foodAuthorId,foodTypeId,foodDetail)
    try:
        db_session.add(newfood)
        db_session.commit()
        db_session.close()
        return render_template('cookbookEdit.html', title='编辑菜谱')
    except Exception,e:
        print e
        return "<script>alert('上传失败，菜品已存在,或菜系ID错误（菜系ID为整数）');</script>"

@aboutCookbook.route("/getFoodInfo<foodId>")
def getfoodInfo(foodId):
    foodInfos = db_session.query(food).filter(food.foodId == foodId).all()
    if foodInfos == []:
        return "<script>alert('请求失败,请重试');</script>"
    else:
        foodInfo = foodInfos[0]
        authorId = foodInfo.foodAuthorId
        authorName = db_session.query(user).filter(user.userId == authorId).all()[0].nickName
        return render_template('foodInfoShow.html',foodInfo = foodInfo,authorName = authorName)

@aboutCookbook.route("/addNewFoodType",methods=['POST'])
def addNewFoodType():
    foodTypeInput = request.form['foodTypeInput']
    foodDescInput = request.form['foodDescInput']
    print foodTypeInput
    print foodDescInput
    newFoodType = foodType(foodTypeInput,foodDescInput)
    try:
        db_session.add(newFoodType)
        db_session.commit()
        db_session.close()
        return "0"
    except Exception ,e:
        print e
        return "-1"