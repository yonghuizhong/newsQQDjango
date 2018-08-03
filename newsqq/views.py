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

    cate_type = Cate.objects()
    context = {
        'article': load,
        'cate_type': cate_type
    }
    return render(request, 'article.html', context)




