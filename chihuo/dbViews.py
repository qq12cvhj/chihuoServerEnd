#coding:utf-8
from flask_admin.contrib.sqla import ModelView
class userView(ModelView):
    column_list = ('userId',
                   'userName',
                   'nickName',
                   #'password',
                   #'emailAddress',
                   #'phoneNumber',
                   #'followerCount',
                   #'selfIntroduction',
                   #'headIcon'
                   )
    column_labels = {
        'userId': u'用户ID',
        'userName': u'用户名',
        'password': u'用户密码',
        'nickName': u'用户昵称',
        'emailAddress': u'电子邮件',
        'phoneNumber':u'电话号码',
        'followerCount':u'粉丝数量',
        'selfIntroduction':u'自我介绍',
        'headIcon':u'用户头像'
    }

    def __init__(self, modelType,session, **kwargs):
        super(userView, self).__init__(modelType, session, **kwargs)