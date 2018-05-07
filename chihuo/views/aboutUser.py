# coding=utf-8
import os, re

import datetime
from chihuo.views import SERVER_IP
from flask import Blueprint, request, jsonify, render_template, json, Response
from aboutCookbook import getRandFilename
from ..dbConnect import db_session
from ..dbModels import share, user, action
from sqlalchemy import func

datetimeRegx = '%Y-%m-%d %H:%M:%S'

aboutUser = Blueprint('aboutUser', __name__)


@aboutUser.route("/uploadVideo", methods=['POST'])
def uploadVideo():
    try:
        file = request.files['video']
        fn = getRandFilename()
        tn = os.path.splitext(file.filename)[1]
        print tn
        fullFileName = fn + tn
        if not os.path.isdir('chihuo/static/videosUpload/'):
            os.mkdir('chihuo/static/videosUpload')
        if (tn == ".mp4") or (tn == ".mpeg") or (tn == ".ogg"):
            file.save(os.path.join('chihuo/static/videosUpload/', fullFileName))
            msg = SERVER_IP + "static/videosUpload/" + fullFileName
        else:
            msg = "err"
    except Exception, e:
        print e
        msg = "err"
    res = Response(msg)
    res.headers["Content-Type"] = "text/plain"
    res.headers["Charset"] = "utf-8"
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res


@aboutUser.route("/uploadImage", methods=['POST'])
def uploadImg():
    file = request.files['image']
    print file.filename
    print os.path.splitext(file.filename)[1]
    if file is None or \
            (os.path.splitext(file.filename)[1] != ".jpg"
             and os.path.splitext(file.filename)[1] != ".gif"
             and os.path.splitext(file.filename)[1] != ".png"):
        jsonInfo = {
            "status": 0,
            "msg": "上传失败,请确保你上传的是图片文件jpg/gif"
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
                "url": SERVER_IP + "static/imgsUpload/" + filename + ""
            }
            return jsonify(jsonInfo)
        except Exception, e:
            jsonInfo = {
                "status": 0,
                "msg": "error|" + str(e)
            }
            return jsonify(jsonInfo)


@aboutUser.route("/shareEdit", methods=['GET'])
def shareEdit():
    return render_template('shareEdit.html', serverip=SERVER_IP)


@aboutUser.route("/pubShare", methods=['POST'])
def pubShare():
    try:
        shareData = json.loads(request.form.get('data'))
        shareTitle = shareData['shareTitle']
        shareAuthorId = shareData['shareAuthorId']
        shareDetail = shareData['shareDetail']
        print shareTitle
        print shareAuthorId
        print shareDetail
        pubtime = datetime.datetime.now().strftime(datetimeRegx)
        newShare = share(int(shareAuthorId), shareDetail, pubtime, shareTitle)
        db_session.add(newShare)
        db_session.commit()
        try:
            newid = db_session.query(func.max(share.shareId)).first()[0]
            newaction = action(2, shareAuthorId, newid, pubtime)
            db_session.add(newaction)
            db_session.commit()
        except Exception, e1:
            print e1
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


def share2json(s):
    shareAuthor = db_session.query(user).filter(user.userId == s.shareAuthorId).first().nickName
    print s.shareDetail
    # 使用正则表达式获取内容中第一个图片的地址.如果没有图片,默认使用程序图标作为分享的缩略图
    imgSrcList = re.findall(r"<img src=\"(.*?)\.jpg", s.shareDetail)
    if imgSrcList == []:
        imgsrc = SERVER_IP + "static/imgsUpload/chihuo.png"
    else:
        imgsrc = imgSrcList[0] + ".jpg"
    return {
        "shareId": s.shareId,
        "shareTitle": s.shareTitle,
        "shareAuthor": shareAuthor,
        "pubTimeStr": str(s.pubTime),
        "shareTitleImg": imgsrc
    }


# 猜你喜欢部分的网络请求返回结果
@aboutUser.route('/getGuessList')
def getGuessList():
    try:
        shareInfoList = db_session.query(share).order_by(func.rand()).limit(10).all()
    except Exception, e:
        print e
        shareInfoList = []
    shareJsonList = []
    for s in shareInfoList:
        shareJsonList.append(share2json(s))
    print json.dumps(shareJsonList)
    return json.dumps(shareJsonList)


@aboutUser.route('/getShareInfoList<authorId>')
def getShareInfoList(authorId):
    shareInfoList = []
    try:
        shareInfoList = db_session.query(share).filter(share.shareAuthorId == authorId).all()
    except Exception, e:
        print e
        shareInfoList = []
    shareJsonList = []
    for s in shareInfoList:
        shareJsonList.append(share2json(s))
    print json.dumps(shareJsonList)
    return json.dumps(shareJsonList)


@aboutUser.route("/getShareInfo<shareId>")
def getShareInfo(shareId):
    shareInfo = db_session.query(share).filter(share.shareId == shareId).first()
    authorId = shareInfo.shareAuthorId
    authorName = db_session.query(user).filter(user.userId == authorId).first().nickName
    return render_template('shareInfoShow.html', shareInfo=shareInfo, authorName=authorName)
