from chihuo import app


"""转换字符，确保中文参数可以传到前端页面,字符编码相关，否则会有中文编码错误。"""
import sys
reload(sys)

if __name__ == '__main__':
    app.run()
