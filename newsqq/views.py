from django.core.paginator import Paginator
from django.shortcuts import render
from newsqq.models import Article
from newsqq.models import Cate
from django.http import JsonResponse
from textrank4zh import TextRank4Sentence


# Create your views here.
# article.html：各类各页的新闻信息
def all_cate(request):
    limit = 10
    page = request.GET.get('page', 1)
    cate = request.GET.get('cate', 'politics')
    num = Article.objects(cate_en=cate).count()
    pipeline = [
        {'$match': {'cate_en': cate}},
        {'$sample': {'size': num}}
    ]
    article = Article.objects.aggregate(*pipeline)
    # article = Article.objects(cate_en=cate)
    paginator = Paginator(list(article), limit)
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
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=article, lower=True, source='all_filters')
    try:
        my_summary = tr4s.get_key_sentences(num=1)[0].sentence
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
