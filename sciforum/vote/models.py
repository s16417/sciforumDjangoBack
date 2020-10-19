from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from answer.models import Answer

class VoteType(models.TextChoices):
    EMPTY = 'EMPTY'
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'

class PostVote(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    '''Make post, voteType and owner unique together inorder to avoid 
    same user putting likes on same answer again and again'''
    class Meta:
        unique_together = ('post', 'owner', 'voteType', )

class AnswerVote(models.Model):

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('answer', 'owner', 'voteType', )