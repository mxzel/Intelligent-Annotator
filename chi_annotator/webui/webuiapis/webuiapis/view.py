
from django.shortcuts import render


def index(request):
    # a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': '', 'article_list': ''}
    return render(request, '/Users/seapatrol/Documents/PyCharmProjects/Intelligent-Annotator/chi_annotator/webui/webuiapis/web/index.html', context)


