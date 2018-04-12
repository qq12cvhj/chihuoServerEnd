# coding=utf-8
import os, re

import datetime
from flask import Blueprint, request, jsonify, render_template, json, Response
from aboutCookbook import getRandFilename
from ..dbConnect import db_session
from ..dbModels import share, user, action
from sqlalchemy import func

datetimeRegx = '%Y-%m-%d %H:%M:%S'

aboutUser = Blueprint('aboutUser', __name__)


@aboutUser.route("/uploadImage", methods=['POST'])
def uploadImg():
    file = request.files['image']
    if file == None:
        jsonInfo = {
            "status": 0,
            "msg": "上传失败"
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
                "url": "http://192.168.1.101:5000/static/imgsUpload/" + filename + ""
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
    return render_template('shareEdit.html')


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
    imgSrcList = re.findall(r"src=\"(.*?)\.jpg", s.shareDetail)
    if imgSrcList == []:
        imgsrc = "http://192.168.1.101:5000/static/imgsUpload/chihuo.png"
    else:
        imgsrc = imgSrcList[0] + ".jpg"
    return {
        "shareId": s.shareId,
        "shareTitle": s.shareTitle,
        "shareAuthor": shareAuthor,
        "pubTimeStr": str(s.pubTime),
        "shareTitleImg": imgsrc
    }


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
