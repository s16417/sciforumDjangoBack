from post.models import Post, Visitors, PostImages
from user_profile.models import ProfileViewerInfo
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from vote.models import PostVote
from answer.models import Answer
# from user_profile.profile_api.serializers import ProfileSerializer
# from drf_writable_nested.serializers import WritableNestedModelSerializer


class VisitorSerializer(serializers.ModelSerializer):
    visitDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Visitors
        fields = ['post', 'visitorIp', 'visitDate']


class ProfileViewerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileViewerInfo
        fields = '__all__'


class PostImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = ['id', 'post', 'created_at', 'image']


class PostTempImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = ['id', 'created_at', 'image']


class PostSerializer(serializers.ModelSerializer, TaggitSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    tags = TagListSerializerField()
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    images = PostImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'body', 'viewCount', 'created_at', 'updated_at', 'tags', 'likes', 'dislikes',
                  'answers', 'images']

    def get_likes(self, obj):
        return PostVote.objects.filter(post_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return PostVote.objects.filter(post_id=obj.id, voteType='DISLIKE').count()

    def get_answers(self, obj):
        return Answer.objects.filter(postBelong=obj.id).count()


class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    images = PostImagesSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['owner', 'title', 'body', 'tags', 'images']


class PostUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    images = PostImagesSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'images']