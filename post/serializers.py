
from rest_framework import serializers

from category.models import Category
from comment.serializers import ComentSerializer
from like.serializers import LikeSerializer
from post.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'
class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username',  'category', 'category_name',  'preview')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        comments = instance.comments.all()
        repr['comments_count'] = comments.count()
        repr['comments'] = ComentSerializer(comments, many=True).data
        repr['like_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
            repr['is_favorite'] = user.favorites.filter(post=instance).exists()
        return repr

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    owner = serializers.ReadOnlyField(source='owner.id')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        #print(self, '!!!!!!!!!!!!!!!!')
        #print(validated_data, '%%%%%%%%%%%%%%%%%')
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImage.objects.create(image=image, post=post)
        return post
class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)
    #comments = ComentSerializer(many=True)
    likes = LikeSerializer(many=True, read_only=True)



    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        like_count = instance.likes.all()
        repr['like_count'] = len(LikeSerializer(like_count, many=True).data)  # 2 способ
        return repr

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        comments = instance.comments.all()
        repr['comments_count'] = comments.count()
        repr['comments'] = ComentSerializer(comments, many=True).data
        repr['like_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
            repr['is_favorite'] = user.favorites.filter(post=instance).exists()
        return repr
