from django.shortcuts import render,HttpResponseRedirect
from blog.forms import SignupForm, LoginForm, AddPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import Group
from django.core.cache import cache
# Create your views here.
# home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'post':posts})
# About
def about(request):
    return render(request, 'blog/about.html')
# Contant page
def contact(request):
    return render(request, 'blog/contact.html')
# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gsp = user.groups.all()
        ip = request.session.get('ip', 0) 
        ct = cache.get('count', version = user.pk)
    return render(request, 'blog/dashboard.html', {'post':posts, 'full_name':full_name, 'gsps':gsp, 'ip':ip, 'ct':ct})
# Sign Up
def signup(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request,"Congratulation! Your registration successfully completed!!!")
            user=fm.save()
            group=Group.objects.get(name='Auther')
            user.groups.add(group)

    else:
        fm = SignupForm()
    return render(request, 'blog/signup.html', {'form':fm})
# user_login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            lgform = LoginForm(request=request, data=request.POST)
            if lgform.is_valid():
                un = lgform.cleaned_data['username']
                upass = lgform.cleaned_data['password']
                user = authenticate(username=un, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Congratulation! Your registration successfully login!!!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            lgform = LoginForm()
        return render(request, 'blog/login.html', {'lg':lgform})
    else:
        return HttpResponseRedirect('/dashboard/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
# Add post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            aform=AddPostForm(request.POST)
            if aform.is_valid():
                af=aform.cleaned_data['title']
                ap=aform.cleaned_data['desc']
                apf=Post(title=af, desc=ap)
                apf.save()
        else:
            aform = AddPostForm()
        return render(request, 'blog/addpost.html',{'addform':aform})
    else:
        return HttpResponseRedirect('/login/')
# Update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            uform = AddPostForm(request.POST,instance=pi)
            if uform.is_valid():
                uform.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi=Post.objects.get(pk=id)
            uform = AddPostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'updateform':uform})

    else:
        return HttpResponseRedirect('/login/')
# Delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')