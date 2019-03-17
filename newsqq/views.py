from django.core.paginator import Paginator
from django.shortcuts import render
from newsqq.models import Article
from newsqq.models import Cate
from django.http import JsonResponse
from Summary import TextRankSentence
import datetime


# Create your views here.
# article.html：各类各页的新闻信息
def all_cate(request):
    limit = 10
    article_list = []
    page = request.GET.get('page', str(1))
    cate = request.GET.get('cate', 'politics')
    # 获取当前日期
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')
    if page == str(1):
        # num = Article.objects(cate_en=cate).count()
        pipeline1 = [
            {'$match': {'$and': [{'cate_en': cate}, {'time': {'$regex': today_str}}]}},  # 日期为今天
            {'$sample': {'size': limit+1}}  # size需大于limit，否则不会出现下一页按钮
        ]
        article = Article.objects.aggregate(*pipeline1)
        article_list = list(article)
        if(len(article_list)) < limit + 1:  # 当天新闻数量不够的情况下，避免没有下一页按钮的情况
            limit = len(article_list) - 1
        if not article_list:  # 当数据不更新时，避免首页出现空白
            print('数据未更新////////////////////////////////')
            limit = 10
            pipeline2 = [
                {'$match': {'cate_en': cate}},
                {'$sample': {'size': limit + 1}}
            ]
            article = Article.objects.aggregate(*pipeline2)
            article_list = list(article)
    else:
        article = Article.objects(cate_en=cate)
        article_list = list(article)
    paginator = Paginator(article_list, limit)
    load = paginator.page(page)

    if load.number <= 6:
        page_array = [i for i in range(1, 11)]
    elif load.number <= load.paginator.num_pages - 4:
        page_array = [i for i in range(load.number - 5, load.number + 5)]
    else:
        page_array = [i for i in range(load.number - 5, load.paginator.num_pages + 1)]

    cate_type = Cate.objects()

    context = {
        'article': load,
        'cate_type': cate_type,
        'page_array': page_array,
    }
    return render(request, 'article.html', context)


# genSummary.html: 生成摘要页面
def summary(request):
    cate_type = Cate.objects()
    context = {
        'cate_type': cate_type
    }
    return render(request, 'genSummary.html', context)


# ajax
def summaryAjax(request):
    article = request.POST.get('article', '默认字段')
    # 暂时使用textRank生成摘要
    tr = TextRankSentence.TextRankSentence()
    tr.analyze(text=article)
    try:
        my_summary = tr.get_key_sentences(num=2)
    except:
        my_summary = '生成新闻摘要错误'
    context = {
        'summary': my_summary
    }
    return JsonResponse(context)


# details.html：新闻正文阅读页面
def details(request):
    id = request.GET.get('t')
    text = Article.objects(_id=id)[0]
    print(text)
    context = {
        'text': text
    }
    print(text)
    return render(request, 'details.html', context)
