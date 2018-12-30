from django.db import models
from mongoengine import *

# Create your models here.
connect('newsQQDB', host='127.0.0.1', port=27017)


class Article(Document):
    cate_en = StringField()
    category = StringField()
    title = StringField()
    href = StringField()
    image = StringField()
    article = StringField()
    introduce = StringField()
    keywords = ListField()
    time = DateTimeField()
    source = StringField()
    summary = StringField()
    my_summary = StringField()
    second_article = StringField()
    second_href = StringField()
    _id = ObjectIdField()
    meta = {'collection': 'links'}  # 服务器上改为links_web，因为是每天更新


class Cate(Document):
    type_name = StringField()
    type_link = StringField()
    type_en = StringField()
    meta = {'collection': 'cate'}


for i in Article.objects[:9]:  # 测试是否连接成功
    print(i.keywords)
    print(i.time)

for i in Cate.objects:
    print(i.type_link)
