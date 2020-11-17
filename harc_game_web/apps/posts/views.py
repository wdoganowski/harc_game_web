from django.shortcuts import render, redirect, get_object_or_404, reverse
from django import forms
from .models import Post
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import F

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['pub_date_time', 'title', 'content', 'link1', 'link2', 'link3']
  
def list_active_posts(request):
	"""
	Function to list all posts on home screen
	"""
	# Exclude future posts
	posts = Post.objects.exclude(pub_date_time__gte = timezone.now())
	return render(request, 'posts/list_active.html', {'posts': posts})
	
def list_all_posts(request):
	"""
	Function to list all posts
	"""
	posts = Post.objects.all().order_by(F('pub_date_time').desc(nulls_last=True))
	return render(request, 'posts/list.html', {'posts': posts})

def view_post(request, slug):
	"""
	Function to list a single post
	"""
	post = Post.objects.get(slug=slug)
	return render(request, 'posts/view.html', {'post': post})
	
def new_post(request):
    """
    Function create a post
    """

    # If request is POST, create a bound form (form with data)
    if request.method == "POST":
        form = PostForm(request.POST)
        
        # check whether form is valid or not
		# if the form is valid, save the data to the database
		# and redirect the user back to the add post form
		
        # If form is invalid show form with errors again
        if form.is_valid():
			#  save data
            post = form.save()
            post.user = request.user
            post.save()
            return redirect('view_post', slug=post.slug)
	# if request is GET the show unbound form to the user
    else:
        form = PostForm()
    return render(request, 'posts/edit.html', {'form': form})

def edit_post(request, slug):
    """
    Function edit a post
    """
    post = get_object_or_404(Post, slug=slug)
    
    # If request is POST, create a bound form(form with data)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        # check whether form is valid or not
        # if the form is valid, save the data to the database
        # and redirect the user back to the update post form

        # If form is invalid show form with errors again
        if form.is_valid():
            form.save()
            return redirect(reverse('view_post', args=[post.slug]))

    # if request is GET the show unbound form to the user, along with data
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit.html', {'form': form, 'post': post})

def delete_post(request, slug):
	"""
	Function to delete a post
	"""
	post = get_object_or_404(Post, slug=slug)
	post.delete()

	return HttpResponseRedirect('/posts/list')
