# coding:utf-8
from sqlalchemy import Column, String, Integer, DateTime, SmallInteger, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from chihuo.dbConnect import Base

"""这个类定义了用户类型，之后会在数据库创建相应的表"""


class user(Base):
    __tablename__ = 'user'

    userId = Column(Integer(), primary_key=True)
    userName = Column(String(16), unique=True, nullable=False)
    password = Column(String(16), nullable=False)
    nickName = Column(String(30), nullable=False, unique=True)
    emailAddress = Column(String(20), unique=True, default=None)
    phoneNumber = Column(String(11), unique=True, default=None)
    followerCount = Column(Integer, default=0)
    selfIntroduction = Column(String(255), nullable=True, default=None)
    headIcon = Column(String(127), nullable=True, default=None)

    # 初始化
    def __init__(self, username=None, psw=None, nn=None):
        self.userName = username
        self.password = psw
        self.nickName = nn


class food(Base):
    __tablename__ = 'food'

    foodId = Column(Integer, primary_key=True)
    foodName = Column(String(16), unique=True, nullable=False)
    foodAuthorId = Column(Integer, nullable=False)
    foodTypeId = Column(Integer)
    foodDetail = Column(LONGTEXT)
    starCount = Column(Integer, default=0)
    hotIndex = Column(Integer, default=0)

    def __init__(self, name=None, authorId=None, typeId=None, detail=None, hotindex=None):
        self.foodName = name
        self.foodAuthorId = authorId
        self.foodTypeId = typeId
        self.foodDetail = detail
        self.hotIndex = hotindex


class foodType(Base):
    __tablename__ = 'foodType'

    foodTypeId = Column(Integer, primary_key=True)
    foodTypeName = Column(String(16), unique=True, nullable=False)
    foodTypeDesc = Column(LONGTEXT)

    def __init__(self, name=None, desc=None):
        self.foodTypeName = name
        self.foodTypeDesc = desc


class foodStar(Base):
    __tablename__ = 'foodStar'

    foodStarId = Column(Integer, primary_key=True)
    foodId = Column(Integer)
    userId = Column(Integer)

    def __init__(self, userid=None, foodid=None):
        self.foodId = foodid
        self.userId = userid


class share(Base):
    __tablename__ = 'share'

    shareId = Column(Integer, primary_key=True)
    shareTitle = Column(String(16), nullable=False)
    shareAuthorId = Column(Integer, nullable=False)
    shareDetail = Column(LONGTEXT)
    pubTime = Column(DateTime, nullable=False)
    hotIndex = Column(Integer, default=0)
    typeName = Column(String(16),  nullable=True)

    def __init__(self, authotid=None, detail=None, pubtime=None, title=None, hotindex=None, type=None):
        self.shareAuthorId = authotid
        self.shareDetail = detail
        self.pubTime = pubtime
        self.shareTitle = title
        self.hotIndex = hotindex
        self.typeName = type


class shareType(Base):
    __tablename__ = 'shareType'

    typeId = Column(Integer, primary_key=True)
    typeName = Column(String(16), nullable=False, unique=True)

    def __init__(self, id=None, name=None):
        self.typeId = id
        self.typeName = name


class action(Base):
    __tablename__ = 'action'

    actionId = Column(Integer, primary_key=True)
    """
    Type不同的数字表示:
            1:创建菜品
            2:发表分享
            3:收藏菜品
            4:....
    """
    actionType = Column(SmallInteger, nullable=False)
    # 主语
    subjectId = Column(Integer, nullable=False)
    # 宾语
    objectId = Column(Integer, nullable=False)
    # 时间
    actionTime = Column(DateTime, nullable=False)

    def __init__(self, type=None, sid=None, oid=None, atime=None):
        self.actionType = type
        self.subjectId = sid
        self.objectId = oid
        self.actionTime = atime


class watch(Base):
    __tablename__ = "watch"

    watchId = Column(Integer, primary_key=True)
    userId = Column(Integer, nullable=False)
    watchedId = Column(Integer, nullable=False)

    def __init__(self, wid=None, uid=None):
        self.userId = uid
        self.watchedId = wid
