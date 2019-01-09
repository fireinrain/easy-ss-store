import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

"""
easyss_store 自动生成shadowsocks，
shadowsocksR等相关配置好的压缩包
"""
# 数据库初始化
DB_INIT = True

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, 'ssdata.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置bootstrap
bootstrap = Bootstrap(app)
database = SQLAlchemy(app)


# 数据库模型
class User(database.Model):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True)
    password = database.Column(database.String(60))
    email = database.Column(database.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'User= username:{self.username},email:{self.email}'


def md5_password(raw_pass):
    pass


if DB_INIT:
    # database.create_all()
    admin = User.query.filter_by(username='admin').first()
    print(admin)
    if not admin:
        admin_user = User("admin", "123456", "admin@admin.com")
        database.session.add(admin_user)
        database.session.commit()


# 默认首页
@app.route('/')
def index():
    return render_template("index.html")


# 登录页
@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


# 注册页
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
