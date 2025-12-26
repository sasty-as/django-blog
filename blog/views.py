# Create your views here.
# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm


def post_list(request):
    # Mengambil semua post yang sudah dipublish,
    # diurutkan berdasarkan tanggal publish
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_edit.html',
        {'form': form}
    )

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/post_edit.html',
        {'form': form}
    )

def custom_logout(request):
    logout(request)
    return redirect('/')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(
        request,
        'blog/add_comment_to_post.html',
        {'form': form}
    )

