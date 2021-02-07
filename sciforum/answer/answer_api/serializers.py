from rest_framework import serializers
from answer.models import Answer
from vote.models import AnswerVote


class AnswerSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username')
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'postBelong', 'owner', 'ownerDisplayName', 'ownerAvatar', 'answerContent', 'created_at', 'updated_at', 'likes', 'dislikes', 'vote_count']

    def get_likes(self, obj):
        return AnswerVote.objects.filter(answer_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return AnswerVote.objects.filter(answer_id=obj.id, voteType='DISLIKE').count()


class AnswerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['postBelong', 'owner', 'answerContent']


class AnswerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answerContent']


# Most voted answers
class TopAnswersSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username')
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'postBelong', 'owner', 'ownerDisplayName', 'ownerAvatar', 'answerContent', 'created_at', 'updated_at', 'vote_count']