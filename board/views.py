from django.shortcuts import render, redirect
from .models import Content, Comment, Tag
from django.utils import timezone
from .forms import ContentForm, CommentForm, TagForm
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    posts = Content.objects.all()
    return render(request, 'board/home.html', {'posts':posts})

def new(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = ContentForm()

    return render(request, 'board/new.html', {'form': form})

def detail(request, pk):
    post = get_object_or_404(Content, pk=pk)
    comments = Comment.objects.filter(post=post) 
    if request.method == "POST":
        comment_form = CommentForm(request.POST) 
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) 
            comment.published_date = timezone.now() 
            comment.author = request.user #추가
            comment.post = post
            comment.save()
            return redirect('detail', pk=pk)
    else:
        comment_form = CommentForm()
        tag_form = TagForm()

    return render(request, 'board/detail.html', {'post': post, 
    'comments':comments, 'comment_form':comment_form, 'tag_form':tag_form})

def edit(request, pk):
    post = get_object_or_404(Content, pk=pk)
    if request.method == "POST":
        form = ContentForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = ContentForm(instance=post)
    return render(request, 'board/edit.html', {'form': form})

def delete(request, pk):
    post = get_object_or_404(Content, pk=pk)
    post.delete()
    return redirect('home')

def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment,pk=comment_pk)
    comment.delete()
    return redirect('detail', pk=pk)

def tag_add(request, pk):
    post = get_object_or_404(Content, pk=pk)
    tag_form = TagForm(request.POST)
    if tag_form.is_valid():
        tag = tag_form.save(commit=False)
        tag, created = Tag.objects.get_or_create(name=tag.name)
        post.tag_set.add(tag)
        return redirect('detail',pk=pk)

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'board/tag.html', {'tags':tags})

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag_posts = tag.content_set.all() #Content.objects.filter(tag_set__in=[tag])
    return render(request, 'board/tag_detail.html',{'tag':tag, 'tag_posts':tag_posts})

def tag_delete(request, pk, tag_pk):
    post = get_object_or_404(Content, pk=pk)
    tag = get_object_or_404(Tag, pk=tag_pk)
    post.tag_set.remove(tag)
    if tag.content_set.count()==0:
        tag.delete()
    return redirect('detail', pk=pk)

