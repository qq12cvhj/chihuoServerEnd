#coding:utf-8
from sqlalchemy import Column, String,Integer,Date,Boolean,DateTime,Text,Float
from chihuo.dbConnect import Base

"""这个类定义了用户类型，之后会在数据库创建相应的表"""
class user(Base):
    __tablename__ = 'user'

    userId = Column(Integer(),primary_key = True)
    userName = Column(String(16),unique=True,nullable=False)
    password = Column(String(16),nullable=False)
    nickName = Column(String(30),nullable=False)
    emailAddress = Column(String(20),unique=True,default=None)
    phoneNumber = Column(String(11),unique=True,default=None)
    followerCount = Column(Integer,default=0)
    selfIntroduction = Column(String(255),nullable=True,default=None)
    headIcon = Column(String(127),nullable=True,default=None)
    #初始化
    def __init__(self,username=None,psw=None,nn=None):
        self.userName = username
        self.password = psw
        self.nickName = nn

