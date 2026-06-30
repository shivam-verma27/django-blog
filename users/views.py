from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,update_session_auth_hash
from blog.models import Post
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserUpdateForm
from django.contrib import messages
from .forms import (UserUpdateForm,ProfileUpdateForm)
from django.contrib.auth.forms import PasswordChangeForm


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/')

    else:

        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'users/register.html',
        context
    )

def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(request,data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('/')

    else:

        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'users/login.html',
        context
    )
def user_logout(request):

    logout(request)

    return redirect('/')

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    total_posts = posts.count()
    total_comments = Comment.objects.filter(author=request.user).count()
    total_likes = sum(post.likes.count() for post in posts)
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_likes': total_likes
    }

    return render(request,'users/profile.html',context)

def public_profile(request,username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request,'users/public_profile.html',context)

@login_required
def edit_profile(request):

    if request.method == 'POST':

        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()

            messages.success(
                request,
                'Profile updated successfully!'
            )

            return redirect('profile')

    else:

        u_form = UserUpdateForm(
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(
        request,
        'users/edit_profile.html',
        context
    )

@login_required
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            user=form.save();
            update_session_auth_hash(request, user)
            messages.success(request,"password change successfully")
            return redirect('profile')
        
    else:
        form=form=PasswordChangeForm(user=request.user)
    
    context={
                'form':form
            }
    return render(request,'users/change_password.html',context)