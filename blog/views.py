from django.shortcuts import render, get_list_or_404, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from verify_email.email_handler import send_verification_email

from .decorators import *
import datetime
import json

from .forms import *
from .models import *
# Create your views here.

date = datetime.datetime.now()
date = date.strftime("%Y/%m/%d")

def index(request):
    posts = get_list_or_404(Post)
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories
    }
    return render(request, 'blog/index.html', context)

def article(request, slang):
    post = get_object_or_404(Post, slang=slang)
    post_id=post.id
    date_created = post.date_created
    comments = Comment.objects.filter(post=post_id)[0:5]

    context = {
        'date_created': date_created,
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/content.html', context)

def category(request, slang):
    categories = Category.objects.all()
    category_id = Category.objects.filter(name__contains=slang)[0].id
    posts = Post.objects.filter(category=category_id)
    context = {
        'slang':slang,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/category.html', context)

def search(request):
    search = request.GET.get('search')
    search_result = Post.objects.filter(body__contains=search)
    print(search_result)
    context = {
        'search_keyword':search,
        'search_result':search_result,
    }
    return render(request, 'blog/search_result.html', context)

@login_required(login_url='blog:login')
def create_post(request):
    user = request.user
    form = PostCreationForm()
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
           article = form.save()
           article.author = request.user
           article.save()
           return HttpResponseRedirect(reverse('blog:index'))
        else:
            print("invalid")
    context = {
        'form': form,
        'user': user,
        'date': date
    }
    return render(request, 'blog/create_post.html', context)

@login_required(login_url='blog:login')
def update_post(request, slang):
    post = Post.objects.get(slang=slang)
    form = PostCreationForm(instance=post)
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('blog:dashboard'))
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/update_post.html', context)

@login_required(login_url='blog:login')
def delete_post(request, slang):
    user = request.user
    post = Post.objects.get(slang=slang)
    groups = []
    for group in user.groups.all():
        groups.append(group.name)

    if 'admin' in groups:
        return HttpResponseRedirect(reverse("blog:admin_dashboard"))
    else:
        return HttpResponseRedirect(reverse('blog:dashboard'))

@login_required(login_url='blog:login')
@allowed_user(allowed_roles=['author'])
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    total_posts = len(posts)
    categories = Category.objects.all()
    author = user.author
    form = UserProfilePicForm(instance=author)
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'categories': categories,
        'form':form,
    }
    return render(request, 'blog/dashboard.html', context)

@login_required(login_url='blog:login')
@allowed_user(allowed_roles=['admin'])
def admin_dashboard(request):
    posts = Post.objects.all()
    total_posts = len(posts)
    categories = Category.objects.all()
    context = {
        'posts':posts,
        'total_posts': total_posts,
        'categories':categories,
    }
    return render(request, 'blog/admin_dashboard.html', context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Authenticated")
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            messages.error(request, "Invalid Credentials!!")
            return HttpResponseRedirect(reverse('blog:login'))
    return render(request, 'blog/login.html')

@unauthenticated_user
def register_view(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        # username = request.POST['username']
        # email = request.POST['email']
        # if User.objects.filter(username=username).exists():
        #     messages.error(request,"Username already taken!!")
        # elif User.objects.filter(email=email).exists():
        #     messages.error(request,"Email already taken!!")
        # else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = send_verification_email(request, form)
            user.first_name = form.clean_first_name()
            user.last_name = form.clean_last_name()
            user.save()
            user.groups.add(Group.objects.get(id=2))
            author = Author.objects.create(user=user)
            author.save()
            return HttpResponseRedirect(reverse('blog:email_verification_sent'))

    context = {
        'form': form
    }
    return render(request, 'blog/register.html', context)

def email_verification_sent(request):
    return render(request, 'blog/registration_email_sent.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

# comment Views

def add_comment(request, pk):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.filter(username=username)[0]
        post = Post.objects.get(id=pk)
        comment_text = request.POST['comment']
        print(user, post, comment_text)
        comment = Comment.objects.create(author=user, post=post, comment_text=comment_text)

        return HttpResponseRedirect(f'/article/{post.slang}')
    else:
        return HttpResponseRedirect(reverse('blog:login'))

def hit_like(request, pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=pk)
        post_slug = Post.objects.filter(comment=pk)[0].slang
        if Likes.objects.filter(author=request.user, comment=comment).exists():
            Likes.objects.filter(author=request.user, comment=comment)[0].delete()
            return redirect(f'/article/{post_slug}')
        else:
            like = Likes.objects.create(author=request.user, comment=comment)
            like.save()
    else:
        return redirect('blog:login')

    return redirect(f'/article/{post_slug}')

def update_profile_pic(request):
    if request.method == 'POST':
        author = request.user.author
        form = UserProfilePicForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:dashboard'))

    return redirect(reverse('blog:dashboard'))

def like(request):
    data = json.loads(request.body)
    commentId = data['commentId']
    comment = Comment.objects.get(id=commentId)
    if Likes.objects.filter(author=request.user, comment=comment).exists():
        Likes.objects.filter(author=request.user, comment=comment)[0].delete()
        total_likes = comment.total_likes()
        return JsonResponse(total_likes, safe=False)
    else:
        like = Likes.objects.create(author=request.user, comment=comment)
        like.save()
        total_likes = comment.total_likes()
        return JsonResponse(total_likes, safe=False)

