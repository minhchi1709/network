from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'followed')
    following = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'following')

    def __str__(self):
        return f'{self.following} followed {self.followed}'


class Post(models.Model):
    content = models.TextField(max_length = 512)
    datetime = models.DateTimeField(auto_now = False)
    poster = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')

    def __str__(self):
        return f'Post {self.id} by {self.poster}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.post}'

class Comment(models.Model):
    comment = models.TextField(max_length = 512)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')

    def __str__(self):
        return f'Comment {self.id} by {self.commenter}'

