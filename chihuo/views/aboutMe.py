#coding:utf-8
from threading import Thread

import time
from flask import Blueprint, request, json

from ..dbModels import  user
from ..dbConnect import db_session

aboutMe = Blueprint('aboutMe',__name__)

@aboutMe.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = db_session.query(user).filter(user.userName==username).all()
    if users==[]:
        #用户名不存在为-1
        return "-1"
    elif users[0].password != password:
        #密码不正确返回-2
        return "-2"
    else:
        return str(users[0].userId)

@aboutMe.route('/reg',methods=['POST'])
def reg():
    username = request.form['username']
    password = request.form['password']
    nickname = request.form['nickname']
    users_username = db_session.query(user).filter(user.userName==username).all()
    users_nickname = db_session.query(user).filter(user.nickName==nickname).all()
    if users_username == []:
        if users_nickname == []:
            try:
                newUser = user(username,password,nickname)
                db_session.add(newUser)
                db_session.commit()
                db_session.close()
                return "0"
            except(BaseException):
                return "-3"
        else:
            return "-1"
    else:
        return "-2"

@aboutMe.route('/getCurrentUserInfo',methods=['POST'])
def getCurrentUserInfo():
    getId = request.form['currentUserId']
    currentUserId = int(getId)
    users = db_session.query(user).filter(user.userId == currentUserId).all()
    if users ==[]:
        return "error"
    else:
        currentUser = users[0]
        return json.dumps(currentUser,default=user2json)

def user2json(u):
    return {
        "userId": u.userId,
        "username":u.userName,
        "password":u.password,
        "nickname":u.nickName,
        "emailAddress":u.emailAddress,
        "phoneNumber":u.phoneNumber,
        "selfIntroduction":u.selfIntroduction,
        "headIcon":u.headIcon
    }

@aboutMe.route('/modifyMyInfo',methods=['POST'])
def modifyMyInfo():
    currentId = int(request.form['currentUserId'])
    print currentId
    nickname = request.form['nickname']
    print nickname
    emailAddress = request.form['emailAddress']
    print emailAddress
    phoneNumber = request.form['phoneNumber']
    print phoneNumber
    selfIntro = request.form['selfIntro']
    print selfIntro
    try:
        db_session.query(user).filter(user.userId == currentId).update(
            {
                'userId':currentId,
                'nickName': nickname,
                'emailAddress': emailAddress,
                'phoneNumber': phoneNumber,
                'selfIntroduction': selfIntro
            }
        )
        db_session.commit()
        db_session.close()
        return "1"
    except Exception,ecp:
        print ecp
        return "-2"
