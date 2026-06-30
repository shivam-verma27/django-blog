from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import CommentForm
from .models import Comment,Category

def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category') 

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = Post.objects.all()
    
    if category:
        posts = posts.filter(categories__name=category)

    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')

    posts = paginator.get_page(page_number)
    popular_posts = Post.objects.order_by('-views','-created_at')[:5]

    context = {
        'posts': posts,
        'categories':Category.objects.all(),
        'selected category':category,
        'popular_posts': popular_posts,
    }

    return render(
        request,
        'blog/home.html',
        context
    )

@login_required
def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    post.views+=1
    post.save()

    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.author = request.user

            comment.post = post

            comment.save()

            return redirect(
                'post_detail',
                post_id=post.id
            )

    else:

        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(
        request,
        'blog/post_detail.html',
        context
    )

@login_required
def create_post(request):
    print("METHOD:", request.method)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request,'Post created successfully!')
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('/')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('/')

    return render(request,'blog/delete_post.html',{'post': post})

@login_required
def update_post(request,post_id):
    post=get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('/')
    if request.method == 'POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Post updated successfully!')
            return redirect('/')
    else:
        form = PostForm(instance=post)
        context = {'form': form, 'post': post}
        return render(request, 'blog/update_post.html', context)
    
@login_required
def toggle_like(request,post_id):
    post=get_object_or_404(Post, id=post_id)
    if(request.user in post.likes.all()):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail',post_id=post.id)

# Create your views here.
