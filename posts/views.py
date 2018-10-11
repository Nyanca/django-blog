from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

def get_posts(request):
    # returns posts published prior to 'now' & render to 'blogposts.html'
    
    posts = Post.objects.filter(published_date__lte=timezone.now
    ()).order_by('-published_date')
    return render(request, 'blogposts.html',{'posts':posts})
    
def post_detail(request, pk):
    # returns a post based on pk to postdetail.html or 404 and traces view count

    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    return render(request, 'postdetail.html', {'post':post})
    
def create_or_edit_post(request, pk=None):
    # enables create post or edit post depending on whether pk exists
    
     post = get_object_or_404(Post, pk=pk) if pk else None
     
     if request.method=="POST":
         form = BlogPostForm(request.POST, request.FILES, instance=post)
         if form.is_valid():
             post = form.save()
             return redirect(post_detail, post.pk)
     else:
        form = BlogPostForm(instance=post)
     return render(request, 'blogpostform.html', {'form':form})
     