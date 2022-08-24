from django.views import generic
from .models import Post, Comment, About
from .forms import CommentForm, PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User as DjangoUser


# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3



class PostDetail(generic.DetailView):
    model = Post 
    template_name = 'post_details.html'    


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context


    def post(self, *args, **kwargs):   
        form = CommentForm(self.request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = self.get_object()

            # Save the comment to the database
            new_comment.save()

        print(form.is_valid())
        print(form.cleaned_data)
        
        return redirect('post_detail',self.get_object().slug)

class CreateBlog(generic.FormView):
    def get(self,request):
        form = PostForm()
        return render(request,'blog.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():          
            post = form.save(commit=False)
            post.author = request.user
            post.save()

        print(form.is_valid())
        print(form.cleaned_data)
        return redirect('home')


    