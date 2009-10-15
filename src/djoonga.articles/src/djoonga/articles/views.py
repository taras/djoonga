from models import Article, Section, Category, Rating, FrontpageContent
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def move(request, ct):
    return render_to_response('admin/move_article.html', {'article' : ct},)
#report = staff_member_required(report)
