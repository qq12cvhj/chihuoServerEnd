#coding:utf-8
from threading import Thread

import time
from flask import Blueprint, request

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