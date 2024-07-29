from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def publish_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/publish_post.html', {'form': form})


@login_required
def home(request):
    print(request.GET.get('data'))
    print("GET HAPPEN")
    return render(request, 'homepage.html')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/single_post.html', {'post': post})
