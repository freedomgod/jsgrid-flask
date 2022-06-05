from flask import Flask, render_template, request, jsonify
# # from gevent import pywsgi
# # from api._util import *
# # from _util import *
# import os
# from flask_sqlalchemy import SQLAlchemy, sqlalchemy
# basedir = os.path.abspath(os.path.dirname(__file__))

# db = SQLAlchemy()


# class Bookmark(db.Model):
#     """
#     存储书签信息的关系/表
#     """
#     __tablename__ = 'bookmarks_table'
#     bookmark_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(64))
#     category = db.Column(db.String(64), db.ForeignKey('category_table.category'), nullable=False)
#     tags = db.Column(db.String(64))
#     url = db.Column(db.Text)
#     favicon_url = db.Column(db.Text)
#     description = db.Column(db.Text)

#     def __repr__(self):
#         return f'Bookmarks: {self.name}'
    
#     @staticmethod
#     def get_maxid():
#         """_summary_
#             获取表的最大ID值
#         Returns:
#             _type_: _description_ 返回整数
#         """
#         return db.session.query(sqlalchemy.sql.func.max(Bookmark.bookmark_id)).scalar()
    
#     def to_dict(self):
#         return {'bookmark_id': self.bookmark_id, 'category': self.category, 'tags': self.tags, 'url': self.url,
#                 'favicon_url': self.favicon_url, 'name': self.name, 'description': self.description}


# class Category(db.Model):
#     __tablename__ = 'category_table'
#     # category_id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(64), primary_key=True)   # 类别的变量名
#     # category_name = db.Column(db.String(64))  # 类别的中文名
#     favicon_code = db.Column(db.String(64))
#     category_bks = db.relationship('Bookmark', backref='category_table')


# def get_all_bookmark():
#     """_summary_返回所有书签内容
#     """
#     return [x.to_dict() for x in Bookmark.query.all()]
    

# def get_bk():
#     return jsonify(get_all_bookmark())


# def update_bk(bk_item):
#     Bookmark.query.filter(Bookmark.bookmark_id == bk_item['bookmark_id']).update(bk_item)
#     db.session.commit()
#     return jsonify(bk_item)


# def insert_bk(bk_item):
#     t_n = Bookmark.get_maxid() + 1
#     bk_item['bookmark_id'] = t_n
#     tem = Bookmark(**bk_item)
#     db.session.add(tem)
#     db.session.commit()
#     return jsonify(tem.to_dict())


# def delete_bk(bk_item):
#     tem = Bookmark.query.filter_by(bookmark_id=bk_item['bookmark_id']).first()
#     db.session.delete(tem)
#     db.session.commit()
#     return jsonify(bk_item)

# def get_test(ss):
#     return jsonify({'path': ss})


# class BaseConfig(object):
#     """配置参数"""
#     # 设置连接数据库的URL
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Bookmark.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False    # 设置每次请求结束后自动提交数据库中的改动
#     SQLALCHEMY_ECHO = True  # 查询时会显示原始的SQL语句
#     SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 禁止自动提交数据处理


# app = Flask(__name__)
# app.config.from_object(BaseConfig)
# db.init_app(app)


# @app.route('/')
# def index():
#     return get_test(basedir)
# #     return render_template('index.html')

# @app.route('/test')
# def test():
#     return get_test(basedir)


# @app.route('/api/db', methods=['GET'])
# def load_bookmark():
#     return get_bk()


# @app.route('/api/db', methods=['PUT'])
# def update_bookmark():
#     return update_bk(request.json)


# @app.route('/api/db', methods=['POST'])
# def insert_bookmark():
#     return insert_bk(request.json)


# @app.route('/api/db', methods=['DELETE'])
# def delete_bookmark():
#     return delete_bk(request.form.to_dict())



# if __name__ == "__main__":
# #     app.run(debug=True)  # 本地环境下以可调试的方式直接运行
# #     server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
# #     server.serve_forever()
#     app.run()
import random
import string
from flask import Flask, request, Response
import json
from gevent import pywsgi


def rand_digits(n: int) -> list:
    """
    生成随机数字列表
    :param n: 数字个数
    :return: 列表
    """
    return [random.choice('0123456789') for _ in range(n)]


def rand_alph(n: int) -> list:
    """
    生成随机字母列表
    :param n: 字母个数
    :return: 列表
    """
    return [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n)]


def rand_dots(n: int) -> list:
    """
    生成随机标点符号列表
    :param n: 符号个数
    :return: 列表
    """
    return [random.choice(',./?;:\'"[]{}\\|') for _ in range(n)]


def rand_op(n: int):
    """
    生成随机特殊字符列表
    :param n: 字符个数
    :return: 列表
    """
    return [random.choice('!@#$%^&*()_+=-~`') for _ in range(n)]


def rand_pin(para: dict) -> list:
    """
    依据参数生成随机字符串
    param length: 字符串长度
    param special: 是否包含特殊的字符串，可选值有0, 1, 2, 3，分别表示不包含、包含特殊字符、包含标点、包含特殊字符和标点，默认为0
    param capt: 字母大写的个数
    param key: 包含关键字
    param number: 生成密码的个数
    param mode: 使用固定的模式生成密码更方便
    :return: 字符串列表
    """
    digits = list('0123456789')  # 数字
    alph = list('abcdefghijklmnopqrstuvwxyz')  # 字母
    dots = list(',./?;:\'"[]{}\\|')  # 标点
    op = list('!@#$%^&*()_+=-~`')  # 特殊符号
    st_pool = digits + alph  # 基础字符池

    special = para.get('s')
    length = para.get('l')
    capt = para.get('c')
    key = para.get('k')
    n = para.get('n')

    if special == 0:  # 添加额外的字符
        pass
    elif special == 1:
        st_pool += op
    elif special == 2:
        st_pool += dots
    else:
        st_pool += dots + op

    pin = []
    for i in range(n):
        pin_lis = []
        if key is None:
            if capt >= length:
                pin_lis += [random.choice(st_pool).upper() for _ in range(length)]
            else:
                capt_st = [random.choice(string.ascii_uppercase) for _ in range(capt)]
                pin_lis += [random.choice(st_pool) for _ in range(length - capt)]
                pin_lis += capt_st
        else:
            if (len(''.join(list(key))) + capt) >= length:
                pin_lis += list(key)
            else:
                capt_st = [random.choice(string.ascii_uppercase) for _ in range(capt)]
                pin_lis += [random.choice(st_pool) for _ in range(length - len(''.join(key)) - capt)] + capt_st + key
        random.shuffle(pin_lis)
        tmp = ''.join(pin_lis)
        pin.append(tmp)
    return pin


# 实例化api，把当前这个python文件当作一个服务，__name__代表当前这个python文件
app = Flask(__name__)


# 'index'是接口路径，methods不写，默认get请求
# get方式访问
@app.route('/api', methods=['get', 'post'])
def rand_pwd():
    # url参数格式：? l=20 & s=1 & c=1 & k=free & n=5
    # l 表示随机数的长度
    # s 表示是否包括标点符号等其他字符
    # c 表示字母是否有大写
    # k 表示是否包含关键字
    # n 表示生成的个数

    l = request.args.get('l', 15)
    s = request.args.get('s', 0)
    c = request.args.get('c', 1)
    k = request.args.getlist('k')
    n = request.args.get('n', 1)
    para = {
        'l': int(l),
        's': int(s),
        'c': int(c),
        'k': k,
        'n': int(n)
    }
    res = {
        'pwd': rand_pin(para),
        'status': 200
    }
#     return Response(json.dumps(res), content_type='application/json')
    return render_template('index.html')

def get_test(ss):
    return jsonify({'path': ss})

@app.route('/api/test')
def index():
#     return get_test(basedir)
    return render_template('index.html')

# @app.route('/test')
# def test():
#     return get_test(basedir)



if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
#     app.run()
