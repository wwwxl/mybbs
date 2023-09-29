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
from rest_framework.viewsets import ModelViewSet 
from rest_framework import status


class IndexView(ModelViewSet):
    queryset = Article.objects
    serializer_class = serializers.ArticleSerializers

    def create(self, request, *args, **kwargs):
        print(request.data)

        if request.user.is_authenticated:
            data = {'Article_title':request.data['Article_title'],
                        'Article_text':request.data['Article_text'],
                        'author':str(request.user),   #这里是为什么，上面的不写竟然也可以？？见鬼？？？
                        'pub_date':timezone.now()}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # print(instance.author,request.user)
        if request.user.is_authenticated:
            if str(instance.author) == str(request.user) or str(request.user) == 'admin':
                # print('可以修改了！')
                data = {'Article_title':request.data['Article_title'],
                        'Article_text':request.data['Article_text'],
                        'author':str(request.user),   #这里是为什么，上面的不写竟然也可以？？见鬼？？？
                        'pub_date':timezone.now()}
                serializer = self.get_serializer(instance, data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response({'error':'这不是你发表的文章，不能修改'})
        else:
            return Response({'error':'还没有登录！'})
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(instance.author) == str(request.user) or str(request.user) == 'admin':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'这不是你发表的文章，不能删除'})

    def retrieve(self, request,pk, *args, **kwargs):
        
        articleinfo = Article.objects.get(id=pk)
        artser = serializers.ArticleSerializers(instance=articleinfo)

        comment = Comment.objects.filter(article_id = pk)  #可能有多条数据，单条用get
        ser = serializers.CommentSerializers(instance=comment , many=True) #传入的是queryset都需要many = True
        return_data = {
            'article_info' :artser.data,
            'comment_data' : ser.data
        }
        return Response(return_data)
        

class CommentView(ModelViewSet):
    queryset = Comment.objects
    serializer_class = serializers.CommentSerializers

    def mylist(self, request,article_id, *args, **kwargs):
        # print(article_id)
        instance = self.queryset.filter(article_id = article_id)
        serializer = self.get_serializer(instance,many=True)
        return Response(serializer.data)
    
    def mycreate(self, request,article_id, *args, **kwargs):
        # print(request)
        if request.user.is_authenticated:
            # data = {    'article':article_id,
            #             'comment_text':request.data['comment_text'],
            #             'author':str(request.user),   #这里是为什么，上面的不写竟然也可以？？见鬼？？？
            #             'pub_date':timezone.now()}
            
            # serializer = self.get_serializer(data={**request.data,'pub_date':timezone.now(),'author':str(request.user)})
            serializer = self.get_serializer(data={'comment_text':request.data['comment_text'],'pub_date':timezone.now(),'author':str(request.user)})###这里又是为什么？？？成功了？？
            print(serializer)
            # serializer.is_valid(raise_exception=True)
            serializer.is_valid()
            print(serializer.validated_data)
            print(serializer.errors)
            
            
            serializer.save(article_id=article_id)  #这里还可以传入哪些参数？？？？
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



            # art = get_object_or_404(Article, pk=article_id)
            # data = {    'article':art,
            #             'comment_text':request.data['comment_text'],
            #             'author':str(request.user),   #这里是为什么，上面的不写竟然也可以？？见鬼？？？
            #             'pub_date':timezone.now()}
            # Comment.objects.create(**data)  
            # return HttpResponseRedirect(reverse("bbs:commentdetial", args=(article_id,)))
            # 上面这里如果直接用Response，会报Object of type Article is not JSON serializable，不明原因的错误。
        else:
            return Response({'error':'还没有登录！'})
        
    def retrieve(self, request, article_id, id, *args, **kwargs):
        instance = self.queryset.filter(article_id = article_id)
        serializer = self.get_serializer(instance[id],many=False)
        return Response(serializer.data)
    
    def destroy(self, request,article_id,id ,*args, **kwargs):
        instance = self.queryset.filter(article_id=article_id)[id]
        if str(instance.author) == str(request.user) or str(request.user) == 'admin':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'这不是你发表的文章，不能删除'})



# 改写rest_framework
# class IndexView(APIView):

#     def get(self,request):
#         articles = Article.objects.all()
#         ser = serializers.ArticleSerializers(instance=articles , many = True)
#         return Response(ser.data)
    
#     def post(self,request):
#         t = request.data.get("title")
#         b = request.data.get("body")
#         if request.user.is_authenticated:
#             if t and b:
#                 Article.objects.create(Article_title = t,Article_text=b,pub_date=timezone.now(),author=request.user)
#                 return Response({'msg':'发布成功'})
#             else:
#                 return Response({'msg':'空内容'})
#         else:
#             return HttpResponseRedirect(reverse('bbs:LoginView'))

         

# class DetailView(APIView):
#     def get(self, request,pk):
#         # 尝试用了两个序列化器进行解决，不知道有没有更简单的解决方式？
#         articleinfo = Article.objects.get(id=pk)
#         artser = serializers.ArticleSerializers(instance=articleinfo)

#         comment = Comment.objects.filter(article_id = pk)  #可能有多条数据，单条用get
#         ser = serializers.CommentSerializers(instance=comment , many=True) #传入的是queryset都需要many = True
#         return_data = {
#             'article_info' :artser.data,
#             'comment_data' : ser.data
#         }
#         return Response(return_data)
    
#     def post(self,request,pk):
#         pass


#     def delete(self,request,pk):
#         pass

#     def put(self,request,pk):
#         pass

class CommentDetailView(APIView):
    def get(self,request,pk,id):

        comment = Comment.objects.filter(article_id = pk)  #可能有多条数据，单条用get
        comment = comment.get(id = id)
        print(comment)
        ser = serializers.CommentDetailSer(instance=comment , many=False) #如果是filter，应该many=True

        return Response(ser.data)
    def put(self,request,pk,id):
        pass
    def delete(self,request,pk,id):
        pass


class LoginView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            login_info = "你已经登陆了,如果需要退出,get'http://127.0.0.1:8000/bbs/logout_view'"

        else:
            login_info = '''你还没有登录,可以发起post请求登录,
            数据格式：{"username": xxx,"password": xxx}
            如果没有账号到'http://127.0.0.1:8000/bbs/register'注册'''
        return_data = {
                'login_info':login_info
            }    
        return Response(return_data)


    def post(self,request):
        print(request.data)
        u = request.data.get('username')
        p = request.data.get('password')
        if u and p:
            user = authenticate(username = u, password = p)
            if user is not None:
                login(request,user)
                login_info = '登录成功！%s'%u
            else:
                login_info = '登录失败，用户不存在或用户名密码错误'
        else:
            login_info = '提交的数据不全啊'
        return_data = {'login_info':login_info}
        return Response(return_data)





class LogoutView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            logout_info = '%s退出成功'%request.user
            logout(request)
        else:
            logout_info = '还没有登录，无需退出'
        return_data = {'logout_info':logout_info}
        return Response(logout_info)




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




# def login_page(request):
#     if request.method == 'GET':    
#         print(request.user.is_authenticated)
#         if request.user.is_authenticated:
#             return HttpResponse("你已经登陆了！")
#         else:
#             return render(request,'bbs/login_page.html')    

#     if request.method == "POST":
#         print(request.user.is_authenticated)
#         u = request.POST.get("username")
#         p = request.POST.get("password") 
#         print(u,p)
#         if u and p:
#             user = authenticate(username=u,password=p)
#             if user is not None:
#                 login(request,user)
#                 print(request.user.is_authenticated)
#                 return HttpResponseRedirect(reverse('bbs:index'))
                

#             else:
#                 return render(
#                 request,
#                 "bbs/login_page.html",
#                 {
#                     "error_message": "登录失败了老铁！用户名或者密码不对呀！",
#                 },)

#         else:
#             return render(
#                 request,
#                 "bbs/login_page.html",
#                 {
#                     "error_message": "你好像什么都没填啊老铁",
#                 },)

# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('bbs:index'))


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
   

