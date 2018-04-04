#coding: utf-8
from flask import Flask, Config

from chihuo.dbViews import userView,foodView,foodTypeView
from views.aboutHome import aboutHome
from views.aboutCookbook import aboutCookbook
from views.aboutFriends import aboutFriends
from views.aboutMe import aboutMe
from views.aboutUser import  aboutUser
from flask_admin import Admin
from dbConnect import db_session
from dbModels import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['UPLOAD_FOLDER'] = '/static/imgsUpload'
#app.config.from_object('chihuo.config')
#app.config.from_object(Config())
app.register_blueprint(aboutHome)
app.register_blueprint(aboutCookbook)
app.register_blueprint(aboutFriends)
app.register_blueprint(aboutMe)
app.register_blueprint(aboutUser)
admin = Admin(app, name='吃货APP后台数据库管理系统', template_mode='bootstrap3')
def models_import_admin():
    admin.add_view(userView(user,db_session,name='用户管理'))
    admin.add_view(foodView(food,db_session,name='菜品管理'))
    admin.add_view(foodTypeView(foodType,db_session,name='菜系管理'))




