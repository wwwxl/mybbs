from django.db import models

# Create your models here.

class Article(models.Model):
    Article_title = models.CharField(max_length=50)
    Article_text = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField('data published')

    def __str__(self) -> str:
        return self.Article_title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=300)
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField('data published')

    def __str__(self) -> str:
        return self.comment_text
