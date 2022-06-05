# jsgrid-flask

jsgrid是一个基于jQuery的轻型客户端数据表格控制的工具。它支持基本的网格操作，例如插入，过滤，编辑，删除，分页，分类和验证。

<p align="center">
  💟 <a href="http://js-grid.com/">jsgrid官网</a> | 🔯 <a href="https://github.com/tabalinas/jsgrid">GitHub地址</a>
<br>
</p>



需要注意的是jsgrid最近的更新也是在两年前，不知道是否是放弃维护了。

下面是使用`jsgrid+flask`做一个可由前端客户控制（增删改查），并将更改更新到数据库的应用。只实现了基础的用法，更为具体的需要参考官方文档。



## 数据库配置

用flask-sqlalchemy连接到数据库，数据库使用sqlite，具体其他数据库也是类似的。主要配置项在`settings.py`文件当中

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Bookmark.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False   # 设置每次请求结束后不要自动提交数据库中的改动
SQLALCHEMY_ECHO = True  # 查询时会显示原始的SQL语句
SQLALCHEMY_COMMIT_ON_TEARDOWN = False  # 禁止自动提交数据处理
```

只需要设置好正确的数据库连接路径即可。这里使用的sqlite数据库放置在根录下。

## 数据库接口

在`api.py`文件中实现对数据的请求接口，主要有增删改查几个方法。



## 模板文件

模板文件中只需要添加`<div id="jsGrid"></div>`元素，然后在后面添加配置的script。

```html
<div id="jsGrid"></div>

    <script>
        $(function() {

            $("#jsGrid").jsGrid({
                height: "70%",
                width: "100%",
                autoload: true,
                filtering: true,
                editing: true,
                inserting: true,
                sorting: true,
                paging: true,
                autoload: true,
                pageSize: 15,
                pageButtonCount: 5,
                deleteConfirm: "确认删除？",
                controller: {
                    loadData: function() {
                        var d = $.Deferred();
                        $.ajax({
                            url: "/api/db",
                            dataType: "json",
                            type: "GET"
                        }).done(function(response) {
                            d.resolve(response);
                        });

                        return d.promise();
                    },
                    updateItem: function(item) {
                        var d = $.Deferred();
                        console.log(item);
                        $.ajax({
                            url: "/api/db",
                            data: JSON.stringify(item),
                            type: "PUT",
                            dataType: "json",
                            contentType: "application/json",
                        }).done(function(response) {
                            d.resolve(response);
                        });
                        return d.promise();
                    },
                    deleteItem: function(item) {
                        var d = $.Deferred();
                        console.log(item);
                        $.ajax({
                            url: "/api/db",
                            data: item,
                            type: "DELETE",
                        }).done(function(response) {
                            d.resolve(response);
                        });
                        return d.promise();
                    },
                    insertItem: function(item) {
                        var d = $.Deferred();
                        $.ajax({
                            url: "/api/db",
                            data: JSON.stringify(item),
                            dataType: "json",
                            contentType: "application/json",
                            type: "POST",
                        }).done(function(response) {
                            d.resolve(response);
                        });
                        return d.promise();
                    },
                },
                fields: [
                    { name: "bookmark_id", type: "number", width: 50, editing: false, inserting: false, sorter: function(value1, value2) {
                        if(value1 < value2) return -1; // return negative value when first is less than second
                        if(value1 === value2) return 0; // return zero if values are equal
                        if(value1 > value2) return 1; // return positive value when first is greater than second
                    } },
                    { name: "name", type: "text", width: 150 },
                    { name: "category", type: "text", width: 70 },
                    { name: "tags", type: "text", width: 30 },
                    { name: "url", type: "text", width: 150 },
                    { name: "favicon_url", type: "text", width: 150 },
                    { name: "description", type: "text", width: 150 },
                    { type: "control" }
                ]
            });

        });
    </script>
```

具体的配置项可以在官方文档查看。这里需要理解的是`controller`项需要实现四个函数（加载、更新、删除、插入），不过这几个方法都是类似的，可以直接copy。要注意的是方法里面的url就是请求数据的接口，在flask当中需要在这个路径上实现接口的请求方法。

## 路由

```python
@app.route('/api/db', methods=['GET',])
def load_bookmark():
    return get_bk()


@app.route('/api/db', methods=['PUT',])
def update_bookmark():
    return update_bk(request.json)


@app.route('/api/db', methods=['POST',])
def insert_bookmark():
    return insert_bk(request.json)


@app.route('/api/db', methods=['DELETE',])
def delete_bookmark():
    return delete_bk(request.form.to_dict())
```

api请求的接口要返回更改后相应的数据，否则更改完数据后，更改能提交到数据库，但不能显示到前端页面上。