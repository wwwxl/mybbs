from rest_framework import serializers
from .models import Article,Comment


# class ArticleSerializers(serializers.Serializer):
#     Article_title = serializers.CharField(max_length=50)
#     Article_text = serializers.CharField()
#     author = serializers.CharField(max_length=30)
#     pub_date = serializers.DateTimeField()

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = "__all__"
        fields = ['id','Article_title','Article_text','pub_date','author']

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # fields = "__all__"
        fields = ['article_id','comment_text','author','pub_date']



# class CommentSerializers(serializers.Serializer):
#     article = serializers.SlugRelatedField(read_only = 'True',slug_field='Article_title')
#     comment_text = serializers.CharField()
#     author = serializers.CharField(max_length=30)
#     pub_date = serializers.DateTimeField()


class CommentDetailSer(serializers.Serializer):
    comment_text = serializers.CharField()
    author = serializers.CharField(max_length=30)
    pub_date = serializers.DateTimeField()

