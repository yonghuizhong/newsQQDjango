from django.core.paginator import Paginator
from django.shortcuts import render
from newsqq.models import Article
from newsqq.models import Cate


# Create your views here.
# article.html：各类各页的新闻信息
def all_cate(request):
    limit = 10
    page = request.GET.get('page', 1)
    cate = request.GET.get('cate', 'politics')
    article = Article.objects(cate_en=cate)
    paginator = Paginator(article, limit)
    load = paginator.page(page)

    if load.number <= 6:
        left_array = [i for i in range(1, 7)]
        right_array = [i for i in range(7, 11)]
    elif load.number <= load.paginator.num_pages - 4:
        left_array = [i for i in range(load.number - 5, load.number)]
        right_array = [i for i in range(load.number, load.number + 5)]
    else:
        left_array = [i for i in range(load.number - 5, load.number)]
        right_array = [i for i in range(load.number, load.paginator.num_pages + 1)]

    cate_type = Cate.objects()

    context = {
        'article': load,
        'cate_type': cate_type,
        'left_array': left_array,
        'right_array': right_array
    }
    return render(request, 'article.html', context)


# genSummary.html: 生成摘要页面
def summary(request):
    cate_type = Cate.objects()
    context = {
        'cate_type': cate_type
    }
    return render(request, 'genSummary.html', context)
