#coding=utf-8
import os

import datetime
from flask import Blueprint, request, jsonify, render_template, json, Response
from aboutCookbook import getRandFilename
from ..dbConnect import db_session
from ..dbModels import share
datetimeRegx = '%Y-%m-%d %H:%M:%S'

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
    msg = ""
    try:
        shareData = json.loads(request.form.get('data'))
        shareTitle = shareData['shareTitle']
        shareAuthorId = shareData['shareAuthorId']
        shareDetail = shareData['shareDetail']
        print shareTitle
        print shareAuthorId
        print shareDetail
        pubtime = datetime.datetime.now().strftime(datetimeRegx)
        newShare = share(int(shareAuthorId), shareDetail, pubtime)
        db_session.add(newShare)
        db_session.commit()
        db_session.close()
        msg = "0"
        res = Response(msg)
        res.headers["Content-Type"] = "text/plain"
        res.headers["Charset"] = "utf-8"
        return res
    except Exception, e:
        print e
        msg = "-1"
        res = Response(msg)
        res.headers["Content-Type"] = "text/plain"
        res.headers["Charset"] = "utf-8"
        return res
