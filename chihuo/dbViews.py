# coding:utf-8
from flask_admin.contrib.sqla import ModelView


class userView(ModelView):
    column_list = ('userId',
                   'userName',
                   'nickName',
                   # 'password',
                   # 'emailAddress',
                   # 'phoneNumber',
                   # 'followerCount',
                   # 'selfIntroduction',
                   # 'headIcon'
                   )
    column_labels = {
        'userId': u'用户ID',
        'userName': u'用户名',
        'password': u'用户密码',
        'nickName': u'用户昵称',
        'emailAddress': u'电子邮件',
        'phoneNumber': u'电话号码',
        'followerCount': u'粉丝数量',
        'selfIntroduction': u'自我介绍',
        'headIcon': u'用户头像'
    }

    def __init__(self, modelType, session, **kwargs):
        super(userView, self).__init__(modelType, session, **kwargs)


class foodView(ModelView):
    column_list = (
        'foodId',
        'foodName',
        'foodAuthorId',
        'foodTypeId'
    )
    column_labels = {
        'foodId': u'菜品ID',
        'foodName': u'菜品名称',
        'foodAuthorId': u'菜品作者的ID',
        'foodTypeId': u'所属菜系ID',
        'foodDetail': u'菜品详细信息',
        'starCount': u'点赞人数',
        'hotIndex': u'菜品热度'
    }

    def __init__(self, modelType, session, **kwargs):
        super(foodView, self).__init__(modelType, session, **kwargs)


class foodTypeView(ModelView):
    column_list = (
        'foodTypeId',
        'foodTypeName',
        'foodTypeDesc',
        'coverPath'
    )
    column_labels = {
        'foodTypeId': u'菜系ID',
        'foodTypeName': u'菜系名称',
        'foodTypeDesc': u'菜系介绍',
        'coverPath':u'封面路径'
    }

    def __init__(self, modelType, session, **kwargs):
        super(foodTypeView, self).__init__(modelType, session, **kwargs)


class foodStarView(ModelView):
    column_list = (
        'foodStarId',
        'foodId',
        'userId'
    )
    column_labels = {
        'foodStarId': u'点赞ID',
        'foodId': u'菜品ID',
        'userId': u'用户ID'
    }

    def __init__(self, modelType, session, **kwargs):
        super(foodStarView, self).__init__(modelType, session, **kwargs)


class shareView(ModelView):
    column_list = (
        'shareId',
        'shareTitle',
        'shareAuthorId',
        'shareDetail',
        'pubTime',
        'typeName',
    )
    column_labels = {
        'shareId': u'分享ID',
        'shareTitle': u'分享标题',
        'shareAuthorId': u'作者ID',
        'shareDetail': u'分享详情',
        'pubTime': u'发表时间',
        'hotIndex': u'分享热度',
        'typeName':u'分享类型名称',
    }

    def __init__(self, modelType, session, **kwargs):
        super(shareView, self).__init__(modelType, session, **kwargs)


class shareTypeView(ModelView):
    column_list = (
        'typeName',
    )
    column_labels = {
        'typeId': u"分享类型ID",
        'typeName': u'分享类型名称'
    }

    def __init__(self, modelType, session, **kwargs):
        super(shareTypeView, self).__init__(modelType, session, **kwargs)


class actionView(ModelView):
    column_list = (
        'actionId',
        'actionType',
        'subjectId',
        'objectId',
        'actionTime'
    )
    column_labels = {
        'actionId': '动态Id',
        'actionType': '动态类型',
        'subjectId': '主语Id',
        'objectId': '宾语Id',
        'actionTime': '动态时间'
    }

    def __init__(self, modelType, session, **kwargs):
        super(actionView, self).__init__(modelType, session, **kwargs)


class watchView(ModelView):
    column_list = {
        'watchId',
        'userId',
        'watchedId'
    }
    column_labels = {
        'watchId': '关注Id',
        'userId': '用户Id',
        'watchedId': '被关注者Id'
    }

    def __init__(self, modelType, session, **kwargs):
        super(watchView, self).__init__(modelType, session, **kwargs)
