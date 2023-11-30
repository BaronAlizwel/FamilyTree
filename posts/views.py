from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            post_type = form.cleaned_data.get('post_type')

            if post_type == 'ST':
                post.status_field = form.cleaned_data.get('status_field')
            elif post_type == 'RV':
                post.review_field = form.cleaned_data.get('review_field')
            elif post_type == 'EV':
                post.event_field = form.cleaned_data.get('event_field')
            elif post_type == 'AN':
                post.announcement_field = form.cleaned_data.get('announcement_field')
            # Add conditions for other post types here, if necessary.

            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post_type = form.cleaned_data.get('post_type')

            if post_type == 'ST':
                post.status_field = form.cleaned_data.get('status_field')
            elif post_type == 'RV':
                post.review_field = form.cleaned_data.get('review_field')
            elif post_type == 'EV':
                post.event_field = form.cleaned_data.get('event_field')
            elif post_type == 'AN':
                post.announcement_field = form.cleaned_data.get('announcement_field')
            # Add conditions for other post types here, if necessary.

            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/update_post.html', {'form': form, 'post': post})

# The rest of your views go here...



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('posts:post_list')

# @login_required
# def post_list(request):
#     post_objects = Post.objects.all()
#     paginator = Paginator(post_objects, 7)  # Show 10 posts per page

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'posts/post_list.html', {'page_obj': page_obj})

from django.core.paginator import Paginator
from django.db.models import F

# @login_required
# def post_list(request):
#     post_objects = Post.objects.order_by(F('created_at').desc())  # Order posts by created_at in descending order
#     paginator = Paginator(post_objects, 6)  # Show 6 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'posts/post_list.html', {'page_obj': page_obj})


from django.shortcuts import render
from .models import Post

def post_list(request):
    sort_type = request.GET.get('sort', 'date')  # Get the sort type from the request parameters
    if sort_type == 'type':
        posts = Post.objects.order_by('type')
    else:
        posts = Post.objects.all()

    post_objects = Post.objects.order_by(F('created_at').desc())  # Order posts by created_at in descending order
    paginator = Paginator(post_objects, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        # Other context variables
    }
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})




@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('posts:post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'posts/update_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('posts:post_detail', post_id=comment.post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('posts:post_detail', post_id=post.id)

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes.remove(request.user)
    post.dislikes.add(request.user)
    return redirect('posts:post_detail', post_id=post.id)