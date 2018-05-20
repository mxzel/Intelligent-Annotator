import os

from django.http import HttpResponse
from django.shortcuts import render
from django import template
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# from django.utils.translation import template
# from chi_annotator.webui.webuiapis.webuiapis.test.a import project_dir
from chi_annotator import project_dir


def index(request):
    # fp = open('/Users/seapatrol/Documents/PyCharmProjects/Intelligent-Annotator/chi_annotator/webui/webuiapis/web
    # /index.html')
    # project_dir = os.path.dirname(os.path.abspath(__file__))
    # fp = open()
    # print(project_dir)
    fp = open(project_dir + '/webui/webuiapis/web/index.html', encoding="utf-8")
    # fp = open('chi_annotator/webui/webuiapis/web/index.html')
    # fp = open('../web/index.html')
    t = template.Template(fp.read())
    fp.close()
    html = t.render(template.Context())
    return HttpResponse(html)
    # a_list = Article.objects.filter(pub_date__year=year)
    # context = {'year': '', 'article_list': ''}
    # return render(request, 'chi_annotator/webui/webuiapis/web/index.html', context)


