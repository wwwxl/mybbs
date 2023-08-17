from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from .models import Article,Comment
from django.http import HttpResponse,Http404,HttpResponseRedirect
# Create your views here.
class IndexView(generic.ListView):
    template_name = "bbs/index.html"
    context_object_name = "latest_Article_list"

    def get_queryset(self):
        """Return the last five published comment."""
        return Article.objects.order_by("pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Article
    template_name = "bbs/detail.html"
    # context_object_name = 'latest_comment_list'  如果不定义context_object_name的话，html模板中用Object



def subart(request):
    if request.method == "POST":
        print(request.POST.getlist())

    #     # 获得表单
    #     article_post_form = ArticlePostForm(data=request.POST)
    #     if article_post_form.is_valid():
    #         cd = article_post_form.cleaned_data
    #         try:
    #             # 将表单数据放入到article_post_form关联的模型ArticlePost
    #             new_article = article_post_form.save(commit=False)
    #             # 文章关联的作者
    #             new_article.author = request.user
    #             # 文章关联的类型
    #             new_article.column = request.user.article_column.get(id=request.POST['column_id'])
    #             # 保存到数据库
    #             new_article.save()
    #             return HttpResponse("1")
    #         except:
    #             return HttpResponse("2")
    #     else:
    #         return HttpResponse("3")
    # else:
    #     article_post_form = ArticlePostForm()
    #     # 查得该用户的所有栏目
    #     article_columns = request.user.article_column.all()
    #     # 入参包括表单和栏目
    #     return render(request, "article/column/article_post.html",
    #                   {"article_post_form": article_post_form, "article_columns": article_columns,})


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.

#     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
