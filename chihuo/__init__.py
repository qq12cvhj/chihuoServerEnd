from flask import Flask, Config
from views.aboutHome import aboutHome
from views.aboutCookbook import aboutCookbook
from views.aboutFriends import aboutFriends
from views.aboutMe import aboutMe
from views.aboutUser import  aboutUser

app = Flask(__name__)
app.config.from_object('chihuo.config')
app.config.from_object(Config())
app.register_blueprint(aboutHome)
app.register_blueprint(aboutCookbook)
app.register_blueprint(aboutFriends)
app.register_blueprint(aboutMe)
app.register_blueprint(aboutUser)





