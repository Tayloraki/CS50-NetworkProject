import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
# from .models import PostForm, LikeForm, FollowForm


def index(request):
    user = request.user
    print("All posts:"+str(Post.objects.all()))
    all_posts = Post.objects.all()
    # if request.method == "POST":
    #     postform = PostForm(request.POST)
    #     if postform.is_valid:
    #         new_post = postform.save(commit=False)
    #         new_post.poster = user
    #         new_post.save()
    # else:
    #     postform = PostForm()
    
    return render(request, "network/index.html", {
        # 'postform': postform,
        # 'posts': posts
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

def profile(request, user):
    profile = User.objects.get(username=user)
    print(profile)
    user = request.user
    # followform = FollowForm()
    # likeform = LikeForm()

    try:
        followers = profile.follower.all()
        print(profile.follower.len())
        if user in followers:
            following = True
        else:
            following = False
    except ObjectDoesNotExist:
        print("profile has no followers")
        following = False

    # try:
    #     userslike = post.liked_by.all()
    #     print(post.liked_by.len())
    #     if user in liked:
    #         liked = True
    #     else:
    #         liked = False
    # except ObjectDoesNotExist:
    #     print("profile has no followers")
    #     liked = False


    # if following:
    #     if request.method == "POST":
    #         if 'followform' in request.method:
    #             unfollowform_submit = FollowForm(request.POST)
    #             if unfollowform_submit.is_valid:
    #                 profile.follower.clear()
    #                 profile.save()
    # else:
    #     if request.method == "POST":
    #         if 'followform' in request.method:
    #             followform_submit = FollowForm(request.POST)
    #             if followform_submit.is_valid:
    #                 profile.follower.add(user)
    #                 profile.save()


    # if liked:
    #     if request.method == "POST":
    #         if 'likeform' in request.method:
    #             unlikeform_submit = LikeForm(request.POST)
    #             if unlikeform_submit.is_valid:
    #                 post.liked_by.clear()
    #                 profile.save()
    # else:
    #     if request.method == "POST":
    #         if 'likeform' in request.method:
    #             likeform_submit = LikeForm(request.POST)
    #             if likeform_submit.is_valid:
    #                 post.liked_by.add(user)
    #                 post.save()


    all_posts = Post.objects.filter(
        poster=profile
    )
    posts = all_posts.order_by("-timestamp").all()
    print("Posts:"+str(posts))

    return render(request, "network/profile.html", {
        'user': profile,
        'posts': posts
    })

def following(request):
    user = request.user
    print(user)
    # if not user.following:
    #     print("not following")
    # else:
    #     following = user.following.all()
    #     print(following)
    print("All posts:"+str(Post.objects.all()))
    # following_post = 
    following_posts = Post.objects.all()
    # if request.method == "POST":
    #     postform = PostForm(request.POST)
    #     if postform.is_valid:
    #         new_post = postform.save(commit=False)
    #         new_post.poster = request.user
    #         new_post.save()
    # else:
    #     postform = PostForm()
    return render(request, "network/following.html", {
        # 'postform': postform,
    })


#           API Call Views

def all(request):
    user = request.user
    print("All posts:"+str(Post.objects.all()))
    all_posts = Post.objects.all()
    posts = all_posts.order_by("-timestamp").all()
    print("Posts:"+str(posts))

    return JsonResponse([post.serialize() for post in posts], safe=False)

def userposts(request, user):
    user = User.objects.get(username=user)
    print(user)
    all_posts = Post.objects.filter(
        poster=user
    )
    posts = all_posts.order_by("-timestamp").all()
    print("Posts:"+str(posts))

    return JsonResponse([post.serialize() for post in posts], safe=False)

# def followingposts(request):
#     user = request.user
#     print(user)
#     try:
#         follows = user.followering.all()
#         print(user.following.len())
#         for follow in follows:
#             followposts = follow.user_posts.all()
#             #   NEED TO GET EACH FOLLOWED USERS POSTS AND MERGE INTO ONE SET
#     except ObjectDoesNotExist:
#         print("user is not following anyone")
#     all_posts = Post.objects.filter(
#         poster=user
#     )
#     posts = all_posts.order_by("-timestamp").all()
#     print("Posts:"+str(posts))

#     return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
def posts(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # Get contents of post
    user = request.user
    body = data.get("body", "")
    print(body)

    post = Post(
        poster=user,
        body=body,
    )
    post.save()
    print(post)

    return JsonResponse({"message": "Post successful."}, status=201)




# def post(request, post_id):

#     # Query for requested email
#     try:
#         post = Post.objects.get(user=request.user, pk=email_id)
#     except Email.DoesNotExist:
#         return JsonResponse({"error": "Email not found."}, status=404)

#     # Return email contents
#     if request.method == "GET":
#         return JsonResponse(email.serialize())

#     # Update whether email is read or should be archived
#     elif request.method == "PUT":
#         data = json.loads(request.body)
#         if data.get("read") is not None:
#             email.read = data["read"]
#         if data.get("archived") is not None:
#             email.archived = data["archived"]
#         email.save()
#         return HttpResponse(status=204)

#     # Email must be via GET or PUT
#     else:
#         return JsonResponse({
#             "error": "GET or PUT request required."
#         }, status=400)