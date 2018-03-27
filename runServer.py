#coding:utf-8
from chihuo import app
from chihuo.dbConnect import init_db
from chihuo import models_import_admin
"""转换字符，确保中文参数可以传到前端页面,字符编码相关，否则会有中文编码错误。"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    init_db()
    models_import_admin()
    app.run('0.0.0.0',5000,debug = True,threaded=True)
