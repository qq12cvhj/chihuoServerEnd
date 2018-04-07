#coding=utf-8
import os
from flask import Blueprint, request, jsonify, render_template, json
from aboutCookbook import getRandFilename, getFoodTypeLIst

aboutUser = Blueprint('aboutUser',__name__)

@aboutUser.route("/uploadImage",methods=['POST'])
def uploadImg():
    file = request.files['image']
    if file == None:
        jsonInfo = {
            "status":0,
            "msg":"上传失败"
        }
        return jsonify(jsonInfo)
    else:
        try:
            filename = getRandFilename() + '.jpg'
            if not os.path.isdir('chihuo/static/imgsUpload/'):
                os.mkdir('chihuo/static/imgsUpload')
            file.save(os.path.join('chihuo/static/imgsUpload/', filename))
            jsonInfo = {
                "status": 1,
                "url": "http://192.168.1.101:5000/static/imgsUpload/"+filename+""
            }
            return jsonify(jsonInfo)
        except Exception, e:
            jsonInfo = {
                "status": 0,
                "msg": "error|" + str(e)
            }
            return jsonify(jsonInfo)

@aboutUser.route("/shareEdit",methods = ['GET'])
def cbEdit():
    return render_template('shareEdit.html')

@aboutUser.route("/pubShare",methods=['POST'])
def pubShare():
    try:
        shareData = json.loads(request.form.get('data'))
        shareTitle = shareData['shareTitle']
        shareAuthorId = shareData['shareAuthorId']
        shareDetail = shareData['shareDetail']
        print shareTitle
        print shareAuthorId
        print shareDetail
        return str('0')
    except Exception,e:
        print e
        return str('-1')
