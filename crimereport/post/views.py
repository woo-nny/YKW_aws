from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import ListView,TemplateView
from .models import Post, Comment
from crime.models import Congressperson
from accounts.models import User
from django.core.paginator import Paginator
import json
from django.forms.models import model_to_dict
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .forms import CommentForm, writeForm, PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def fn_pagination(request, model, paginate_by = 10):
    paginator = Paginator(model, paginate_by)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_numbers_range = 5
    max_index = len(paginator.page_range)
    current_page = int(page_number) if page_number else 1
    start_index = int((current_page - 1)/page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index
    page_list = paginator.page_range[start_index:end_index]
    return (page_obj, page_list)

def get_author_congperson(model):
    result = []
    for m in model:
        user = User.objects.get(username = m.author)
        c = Congressperson.objects.get(district = user.city + user.district)
        result.append([m,c.name])
    return result

def postlist(request):
    if 'search_text' in request.GET:
        search = request.GET['search_text']
        orders = request.GET['search_order']
        if orders == 'text':
            model = Post.objects.filter(text__contains=search)
        elif orders == 'title':
            model = Post.objects.filter(title__contains=search)
        else:
            model = Post.objects.filter(text__contains=search, title__contains=search)
        result = get_author_congperson(model)
        page_obj, page_list = fn_pagination(request, result)
    elif 'party' in request.GET:
        search = request.GET['party']
        # models = Post.objects.all()
        partys_of_congressperson = Congressperson.objects.filter(party = search)
        user_model = User.objects.all()
        final_user = []
        for cong_person in partys_of_congressperson:
            for user in user_model:
                if user.city+user.district in cong_person.district:
                    final_user.append(user)
        model = Post.objects.none()
        for user in final_user:
            model |= Post.objects.filter(author = user)
        result = get_author_congperson(model)
        page_obj, page_list = fn_pagination(request, result)
    else:
        model = Post.objects.all()
        result = get_author_congperson(model)
        page_obj, page_list = fn_pagination(request, result)
    return render(request, 'post/postList.html', {'page_obj':page_obj,'page_list':page_list})


def detailpost(request, post_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_form.instance.post= Post.objects.get(id = post_id)
            comment_form.instance.author = auth.get_user(request)
            comment_form.save()
            return redirect(detailpost, post_id)
    else:
        detail_post = Post.objects.get(id = post_id)
        # comments = Comment.objects.select_related('post').filter(id = post_id).order_by('created')
        comments = detail_post.comments.all()
        context = {'detail_post':detail_post, 'comments':comments}
        return render(request, 'post/detailPost.html', context)

def ajaxcreatecomment(request, post_id):
    if HttpRequest.is_ajax():
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_form.instance.post= Post.objects.get(id = post_id)
            comment_form.instance.author = auth.get_user(request)
            comment_form.save()
            senddata = model_to_dict(comment_form.instance)
            to_json = {**senddata}
            return JsonResponse(to_json)

def updatepost(request, post_id):
    model = Post.objects.get(id=post_id)
    if request.method == 'POST':
        writeform = writeForm(request.POST, request.FILES, instance = model) #수정시에는 instance와 files를 불러와야함
        if writeform.is_valid():
            model.title = writeform.cleaned_data['title']
            model.text = writeform.cleaned_data['text']
            model.updated = timezone.now()
            model.save()
            return redirect(postlist)
    else:
        context = {'model':model}
        return render(request, 'post/updatepost.html', context)

def writepost(request):
    if request.method == 'POST':
        writeform = writeForm(request.POST, request.FILES)
        if writeform.is_valid():
            writeform.instance.author = auth.get_user(request) #생성시에는 instance, files를 안불러와도됨
            writeform.save()
            return redirect(postlist)
    else:
        return render(request, 'post/updatepost.html', {})
