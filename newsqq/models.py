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


num = Article.objects(cate_en='politics').count()
print(num)
pipeline = [
    {'$match': {'cate_en': 'politics'}},
    {'$sample': {'size': 5}}
]
for i in Article.objects.aggregate(*pipeline):  # 测试是否连接成功
    print(i['title'], i['cate_en'])

for i in Cate.objects:
    print(i.type_link)
