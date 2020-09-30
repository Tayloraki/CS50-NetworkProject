from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

class User(AbstractUser):
    follower = models.ForeignKey(
        'self',
        blank=True,
        on_delete=models.CASCADE,
        related_name="followed"
    )
    following = models.ForeignKey(
        'self',
        blank=True,
        on_delete=models.CASCADE,
        related_name="followers"
    )

class Post(models.Model):
    poster = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_posts"
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # liked = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     related_name="liked_by"
    # )

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            # "liked": self.liked,
        }

# class PostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['body']
#         exclude = ['poster', 'time', 'liked']

# # class LikeForm(ModelForm):
# #     class Meta:
# #         model = Post
# #         exclude = [
# #             'poster', 'body', 'timestamp', 'like'
# #         ]

# class FollowForm(ModelForm):
#     class Meta:
#         model = User
#         exclude = ['user']