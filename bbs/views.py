from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.utils import timezone
from .models import Article,Comment
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

# 改写rest_framework
class IndexView(APIView):
    def get(self,request):
        articles = Article.objects.all()
        ser = serializers.ArticleSerializers(instance=articles , many = True)
        return Response(ser.data)

class DetailView(APIView):
    def get(self, request,pk):
        # 尝试用了两个序列化器进行解决，不知道有没有更简单的解决方式？
        articleinfo = Article.objects.get(id=pk)
        artser = serializers.ArticleSerializers(instance=articleinfo)

        comment = Comment.objects.filter(article_id = pk)  #可能有多条数据，单条用get
        ser = serializers.CommentSerializers(instance=comment , many=True)
        return_data = {
            'article_info' :artser.data,
            'comment_data' : ser.data
        }
        return Response(return_data)
    
    def post(self,request,pk):
        pass


    def delete(self,request,pk):
        pass

    def put(self,request,pk):
        pass





# 老版的views
# Create your views here.
# class IndexView(generic.ListView):
#     template_name = "bbs/index.html"
#     context_object_name = "latest_Article_list"

#     def get_queryset(self):
#         """Return the last five published comment."""
#         return Article.objects.order_by("-pub_date")
    
# class DetailView(generic.DetailView):
#     model = Article
#     template_name = "bbs/detail.html"
#     # context_object_name = 'latest_comment_list'  如果不定义context_object_name的话，html模板中用Object



def subart(request):
    if request.method == "POST":
        t = request.POST.get("title")
        b = request.POST.get("body")
        if request.user.is_authenticated:
            if t and b:
                Article.objects.create(Article_title = t,Article_text=b,pub_date=timezone.now(),author=request.user)
        
                return HttpResponseRedirect(reverse('bbs:index'))   # app名：url名
        else:
            return HttpResponseRedirect(reverse('bbs:login_page'))
        # return HttpResponseRedirect('/bbs/')



def register(request):
    if request.method == 'GET':
        return render(request,'bbs/register.html')
    if request.method == "POST":
        print(request.user.is_authenticated)
        u = request.POST.get("username")
        p = request.POST.get("password")
        print(u,p)
        if u and p:
            if not User.objects.filter(username = u).exists():
                new_user = User.objects.create_user(username=u,password=p)
                print(new_user)
                new_user.save()
                return HttpResponseRedirect(reverse('bbs:index'))   # app名：url名
            else:
                return render(
                request,
                "bbs/register.html",
                {
                    "error_message": "注册失败了老铁！用户名已经存在！",
                },)

        else:
            return render(
                request,
                "bbs/register.html",
                {
                    "error_message": "你好像什么都没填啊老铁",
                },)




def login_page(request):
    if request.method == 'GET':    
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return HttpResponse("你已经登陆了！")
        else:
            return render(request,'bbs/login_page.html')    

    if request.method == "POST":
        print(request.user.is_authenticated)
        u = request.POST.get("username")
        p = request.POST.get("password") 
        print(u,p)
        if u and p:
            user = authenticate(username=u,password=p)
            if user is not None:
                login(request,user)
                print(request.user.is_authenticated)
                return HttpResponseRedirect(reverse('bbs:index'))
                

            else:
                return render(
                request,
                "bbs/login_page.html",
                {
                    "error_message": "登录失败了老铁！用户名或者密码不对呀！",
                },)

        else:
            return render(
                request,
                "bbs/login_page.html",
                {
                    "error_message": "你好像什么都没填啊老铁",
                },)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('bbs:index'))


def subcomment(request,article_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            b = request.POST.get('comment')
            art = get_object_or_404(Article, pk=article_id)
            print(art)
            Comment.objects.create(article = art,comment_text=b,pub_date=timezone.now(),author=request.user)        
            return HttpResponseRedirect(reverse("bbs:detail", args=(article_id,)))
        else:
            return HttpResponseRedirect(reverse('bbs:login_page'))
   

