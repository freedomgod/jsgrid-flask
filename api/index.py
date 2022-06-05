from flask import Flask, render_template, request
from gevent import pywsgi
from api.util import *
# from util import *
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """配置参数"""
    # 设置连接数据库的URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Bookmark.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # 设置每次请求结束后自动提交数据库中的改动
    SQLALCHEMY_ECHO = True  # 查询时会显示原始的SQL语句
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 禁止自动提交数据处理


app = Flask(__name__)
app.config.from_object(BaseConfig)
db.init_app(app)


@app.route('/')
def index():
    return get_test(basedir)
#     return render_template('index.html')

@app.route('/test')
def test():
    return get_test(basedir)


@app.route('/api/db', methods=['GET'])
def load_bookmark():
    return get_bk()


@app.route('/api/db', methods=['PUT'])
def update_bookmark():
    return update_bk(request.json)


@app.route('/api/db', methods=['POST'])
def insert_bookmark():
    return insert_bk(request.json)


@app.route('/api/db', methods=['DELETE'])
def delete_bookmark():
    return delete_bk(request.form.to_dict())



if __name__ == "__main__":
    # app.run(debug=True)  # 本地环境下以可调试的方式直接运行
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    app.run()
