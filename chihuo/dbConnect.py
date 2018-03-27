#coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
dbEngine = create_engine('mysql://root:123456@localhost:3306/chihuo?charset=utf8')
dbSession = sessionmaker(bind = dbEngine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=dbEngine))
Base.query = db_session.query_property()

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。否则你就必须在调用 init_db() 之前导入它们????
    import chihuo.dbModels
    Base.metadata.create_all(bind=dbEngine)