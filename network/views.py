from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Comment, Follow, Like
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json

@csrf_exempt
@login_required
def comment(request, id):
    if request.method == "PUT":
        body = json.loads(request.body)
        comment = body['comment']
        post = Post.objects.all().get(pk = id)
        Comment.objects.create(commenter = request.user, post = post, comment = comment)
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def like(request, id):
    if request.method == "PUT":
        body = json.loads(request.body)
        liked = body['liked']
        post = Post.objects.all().get(pk = id)
        if liked:
            Like.objects.create(user = request.user, post = post)
        else:
            Like.objects.all().get(user = request.user, post = post).delete()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def edit(request, id):
    if request.method == "PUT":
        body = json.loads(request.body)
        if body.get('content'):
            content = body['content']
            post = Post.objects.all().get(pk = id)
            post.content = content
            post.save()
    return HttpResponse(status=204)

def following(request):
    # Find all follows by current user
    followings = Follow.objects.all().filter(following = request.user)
    
    # Find all users who the current user follows
    followings = [following.followed for following in followings] 

    # Create list of dicts
    posts = [post for following in followings for post in following.posts.all()]

    posts = [{'post': post, 'liked': len(Like.objects.all().filter(user = request.user, post = post)), 
              'likes': len(Like.objects.all().filter(post = post)),
              'comments': reversed(list(Comment.objects.all().filter(post = post)))} for post in posts]
    # Number of pages
    end = len(posts) // 10
    # Reverse chronological order
    posts.reverse()
    pages = []
    # Devide posts into sublist of posts with length of 10
    for i in range(end):
        pages.append({'page': i, 'posts': posts[i : i + 10]}) 
    if 10 * end < len(posts):
        pages.append({'page': end, 'posts': posts[10 * end:]})
    
    return render(request, 'network/following.html', {
        'pages': pages,
        'end' : end,
    })

def follow(request, id):
    user = User.objects.all().get(pk = id)
    if request.method == "POST":
        # If the user click follow, then add following relation
        if request.POST['follow'] == 'Follow':
            Follow.objects.create(following = request.user, followed = user)
        # Otherwise delete the relation between them
        else:
            Follow.objects.all().get(following = request.user, followed = user).delete()
    return HttpResponseRedirect(reverse('user', args=(id,)))

def user(request, id):
    user = User.objects.all().get(pk = id)
    posts = list(Post.objects.all().filter(poster = user))
    posts = [{'post': post, 'liked': len(Like.objects.all().filter(user = request.user, post = post)), 
              'likes': len(Like.objects.all().filter(post = post)),
              'comments': reversed(list(Comment.objects.all().filter(post = post)))} for post in posts]
    # Number of pages
    end = len(posts) // 10
    # Reverse chronological order
    posts.reverse()
    pages = []
    # Devide posts into sublist of posts with length of 10
    for i in range(end):
        pages.append({'page': i, 'posts': posts[i : i + 10]}) 
    if 10 * end < len(posts):
        pages.append({'page': end, 'posts': posts[10 * end:]}) 

    return render(request, 'network/user.html', {
        'user_searching': user,
        'followed': len(Follow.objects.all().filter(followed = user, following = request.user)) == 1,
        'followers': len(Follow.objects.all().filter(followed = user)),
        'samePerson': user == request.user,
        'pages': pages,
        'end' : end,
    })

def post(request):
    if request.method == "POST":
        content = request.POST['content']
        # Check if the content of the post is valid
        if not content or len(content) == 0:
            return render(request, 'network/failure.html', {
                'msg': 'Invalid Content'
            })
        # Create a post
        Post.objects.create(poster = request.user, content = content, datetime = datetime.now())
    return HttpResponseRedirect(reverse('index'))

def index(request):
    posts = list(Post.objects.all())
    posts = [{'post': post, 'liked': len(Like.objects.all().filter(user = request.user, post = post)), 
              'likes': len(Like.objects.all().filter(post = post)),
              'comments': reversed(list(Comment.objects.all().filter(post = post)))} for post in posts]
    # Number of pages
    end = len(posts) // 10
    # Reverse chronological order
    posts.reverse()
    pages = []
    # Devide posts into sublist of posts with length of 10
    for i in range(end):
        pages.append({'page': i, 'posts': posts[i : i + 10]}) 
    if 10 * end < len(posts):
        pages.append({'page': end, 'posts': posts[10 * end:]}) 
    return render(request, "network/index.html", {
        'pages': pages,
        'end' : end,
        'user': request.user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
