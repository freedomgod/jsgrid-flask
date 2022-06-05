# 从数据库获取相关数据的接口
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import sqlalchemy


db = SQLAlchemy()


class Bookmark(db.Model):
    """
    存储书签信息的关系/表
    """
    __tablename__ = 'bookmarks_table'
    bookmark_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64), db.ForeignKey('category_table.category'), nullable=False)
    tags = db.Column(db.String(64))
    url = db.Column(db.Text)
    favicon_url = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'Bookmarks: {self.name}'
    
    @staticmethod
    def get_maxid():
        """_summary_
            获取表的最大ID值
        Returns:
            _type_: _description_ 返回整数
        """
        return db.session.query(sqlalchemy.sql.func.max(Bookmark.bookmark_id)).scalar()
    
    def to_dict(self):
        return {'bookmark_id': self.bookmark_id, 'category': self.category, 'tags': self.tags, 'url': self.url,
                'favicon_url': self.favicon_url, 'name': self.name, 'description': self.description}


class Category(db.Model):
    __tablename__ = 'category_table'
    # category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), primary_key=True)   # 类别的变量名
    # category_name = db.Column(db.String(64))  # 类别的中文名
    favicon_code = db.Column(db.String(64))
    category_bks = db.relationship('Bookmark', backref='category_table')


def get_all_bookmark():
    """_summary_返回所有书签内容
    """
    return [x.to_dict() for x in Bookmark.query.all()]
    

def get_bk():
    return jsonify(get_all_bookmark())


def update_bk(bk_item):
    Bookmark.query.filter(Bookmark.bookmark_id == bk_item['bookmark_id']).update(bk_item)
    db.session.commit()
    return jsonify(bk_item)


def insert_bk(bk_item):
    t_n = Bookmark.get_maxid() + 1
    bk_item['bookmark_id'] = t_n
    tem = Bookmark(**bk_item)
    db.session.add(tem)
    db.session.commit()
    return jsonify(tem.to_dict())


def delete_bk(bk_item):
    tem = Bookmark.query.filter_by(bookmark_id=bk_item['bookmark_id']).first()
    db.session.delete(tem)
    db.session.commit()
    return jsonify(bk_item)

def get_test(ss):
    return jsonify({'path': ss})