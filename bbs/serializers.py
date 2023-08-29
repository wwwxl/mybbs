from rest_framework import serializers


class ArticleSerializers(serializers.Serializer):
    Article_title = serializers.CharField(max_length=50)
    Article_text = serializers.CharField()
    author = serializers.CharField(max_length=30)
    pub_date = serializers.DateTimeField()



class CommentSerializers(serializers.Serializer):
    article = serializers.SlugRelatedField(read_only = 'True',slug_field='Article_title')
    comment_text = serializers.CharField()
    author = serializers.CharField(max_length=30)
    pub_date = serializers.DateTimeField()
