from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from book.models import BookInfo
from django.http import JsonResponse
import json

"""
通过REST来实现 对于书籍的 增删改查操作

增加一本书籍
删除一本书籍
修改一本书籍
查询一本书籍
查询所有书籍

###########列表视图#################################    
查询所有书籍
GET             books/
    1.查询所有数据
    2.将查询结果集进行遍历,转换为字典列表
    3.返回响应

增加一本书籍
POST            books/
    1.接收参数,获取参数
    2.验证参数
    3.保存数据
    4.返回响应

###########详情视图#################################
删除一本书籍
DELETE          books/id/
    1. 接收参数,查询数据
    2. 操作数据库(删除)
    3. 返回响应

修改一本书籍
PUT             books/id/
    1.查询指定的数据
    2.接收参数,获取参数
    3.验证参数
    4.更新数据
    5.返回响应
查询一本书籍
GET             books/id/
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应

pip install djangorestframework
###########列表视图#################################    
查询所有书籍
GET             books/
    1.查询所有数据                                    查询数据库
    2.将查询结果集进行遍历,转换为字典列表                 序列化操作
    3.返回响应                                        返回响应

增加一本书籍
POST            books/
    1.接收参数,获取参数                                 JSON/dict
    2.验证参数
    3.保存数据                                        反序列化操作
    4.返回响应                                        序列化操作

###########详情视图#################################
删除一本书籍
DELETE          books/id/
    1. 接收参数,查询数据                              查询
    2. 操作数据库(删除)                              删除
    3. 返回响应

修改一本书籍
PUT             books/id/   
    1.查询指定的数据                               对象
    2.接收参数,获取参数                         JSON/dict
    3.验证参数
    4.更新数据                                  反序列化
    5.返回响应                                  序列化
查询一本书籍
GET             books/id/
    1.查询指定数据
    2.将对象数据转换为字典数据                      序列化
    3.返回响应

"""


# Create your views here.
class BookListView(View):
    """
    查询所有图书、增加图书
    """

    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            name=book_dict.get('name'),
            pub_date=book_dict.get('pub_date')
        )

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        }, safe=False)


class BookDetailView(View):
    """
    获取单个图书信息
    修改图书信息
    删除图书
    """

    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.name = book_dict.get('name')
        book.pub_date = book_dict.get('pub_date')
        book.save()

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        book.delete()

        return JsonResponse({}, status=204)


from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 模拟对象数据
book = BookInfo.objects.get(id=1)
# 2. 创建序列化器,将对象数据给序列化器
serializer = BookInfoSerializer(instance=book)
# 3. 获取序列化器的字典数据
print(serializer.data)

# 1.获取所有书籍
books = BookInfo.objects.all()
# 2.实例化序列化，将对象数据传递给序列化器
serializer = BookInfoSerializer(books, many=True)
# 3.获取序列化（将对象转为json）数据
print(serializer.data)

from book import serializers
from book.models import PeopleInfo

people = PeopleInfo.objects.get(id=1)
serializer = serializers.PeopleInfoSerializer(instance=people)
print(serializer.data)

from book.serializers import BookInfoSerializer
from book.models import BookInfo

book = BookInfo.objects.get(id=1)
s = BookInfoSerializer(book)
print(s.data)

"""
序列化器验证数据的第一种形式:

1.  我们定义的数据类型,可以帮助我们 在反序列化(字典转模型)的时候 验证传入的数据的类型
    例如:
        DateField 需要满足 YYYY-MM-DD
        IntegerField 满足整形类型

2.  通过字段的选项来验证数据
    例如: 
        CharField(max_length=10,min_length=5)
        IntegerField(max_value=10,min_value=1)
        required=True 默认是True

        read_only: 只用于序列化使用. 反序列化的时候 忽略该字段
        write_only: 只是用于反序列化使用. 序列化的时候 忽略该字段
"""

# 将字典转换为对象
from book.serializers import BookInfoSerializer

# 1. 模拟字典数据
# data = {
#     'name': 'django',
#     'pub_date': '2018-1-1',
#     'readcount': 666
# }
# 2. 创建序列化器,将字典数据给序列化器
# BookInfoSerializer(instance,data)
# instance 用于序列化(对象转换为字典)
# data 用于反序列化(字典转换为对象)
# serializer = BookInfoSerializer(data=data)

# 3. 验证数据
# 如果我们的数据 正确(满足需求) 返回True
# 如果我们的数据 不正确(不满足需求) 返回False
# serializer.is_valid(raise_exception=True)
# 4. 保存,获取对象


######################反序列化数据验证##########################
# from book.serializers import BookInfoSerializer
#
# # 1. 模拟字典数据
# data = {
#     'name': 'django',
#     'pub_date': '2020-1-1',
#     'readcount': 100,
#     'commentcount': 10
# }
# # 2. 创建序列化器,将字典数据传递给序列化器
# serializer = BookInfoSerializer(data=data)
# # 3. 验证数据
# serializer.is_valid(raise_exception=True)
# # 4.验证数据没有问题之后,就可以调用保存方法了
# serializer.save()

#######################################################################
from book.serializers import BookInfoSerializer
from book.models import BookInfo

# # 1. 模拟一个对象数据
# book = BookInfo.objects.get(id=1)
# # 2. 模拟一个字典数据
# data = {
#     'name': '射雕英雄后传',
#     'pub_date': '2000-1-1',
#     'readcount': 999,
#     'commentcount': 666
# }
# # 3. 把对象和字典都传递给序列化器的创建
# serializer = BookInfoSerializer(instance=book, data=data)
#
# # 4. 验证数据
# serializer.is_valid(raise_exception=True)
# # 5. 数据的更新操作
# serializer.save()
# # 6.会获取新字典数据
# serializer.data

#####################################
# from book.serializers import BookInfoModelSerializer
#
# data = {
#     'name': '射雕英雄~~~~',
#     'pub_date': '2000-1-1',
#     'readcount': 999,
#     'commentcount': 666
# }
#
# serializer = BookInfoModelSerializer(data=data)
# serializer.is_valid(raise_exception=True)
# serializer.save()

from book.serializers import BookInfoModelSerializer

BookInfoModelSerializer()

#################################################
# 这个data 就类似于 我们在讲解 序列化的时候
# 定义了一个 PeopleInfoSerializer
# 定义了一个 BookInfoSerialzier
# 在BookInfoSerialzier 有一个字段是 peopleinfo=PeopleInfoSerializer(many=True)
"""
class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')

class BookInfoSerializer(serializers.Serializer):
    name = serializers.CharField(label='名称')

    #一本书籍关联多个人物
    people=PeopleInfoSerializer(many=True)

"""
from book.serializers import BookInfoModelSerializer

# # 1. 模拟数据
# data = {
#     'name': '离离原上草',
#     'people': [
#         {
#             'name': '靖妹妹111',
#             'password': '123456abc'
#         },
#         {
#             'name': '靖表哥222',
#             'password': '123456abc'
#         }
#     ]
# }
#
# # 2. 将字典数据传递给序列化器,创建序列化器对象
# serializer = BookInfoModelSerializer(data=data)
# # 3. 验证数据
# serializer.is_valid(raise_exception=True)
# # 4. 保存数据
# serializer.save()

########################apiView#########3
"""
通过REST来实现 对于书籍的 增删改查操作

增加一本书籍
删除一本书籍
修改一本书籍
查询一本书籍
查询所有书籍

###########列表视图#################################    
查询所有书籍
GET             books/
    1.查询所有数据
    2.将查询结果集进行遍历,转换为字典列表
    3.返回响应

增加一本书籍
POST            books/
    1.接收参数,获取参数
    2.验证参数
    3.保存数据
    4.返回响应

###########详情视图#################################
删除一本书籍
DELETE          books/id/
    1. 接收参数,查询数据
    2. 操作数据库(删除)
    3. 返回响应

修改一本书籍
PUT             books/id/
    1.查询指定的数据
    2.接收参数,获取参数
    3.验证参数
    4.更新数据
    5.返回响应
查询一本书籍
GET             books/id/
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应

"""
from rest_framework.views import APIView
from book.models import BookInfo
from book.serializers import BookInfoModelSerializer
from django.http import HttpRequest  # django
from django.http import HttpResponse  # django

from rest_framework.request import Request  # drf
from rest_framework.response import Response  # drf


class BookListAPIView(APIView):

    def get(self, request):
        # django -- request.GET
        # drf -- request.query_params
        query_params = request.query_params

        # 1.查询所有数据
        books = BookInfo.objects.all()
        # 2.将查询结果集进行遍历,转换为字典列表
        serializer = BookInfoModelSerializer(instance=books, many=True)
        # 3.返回响应
        from rest_framework import status
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return JsonResponse({'code':'get','books':serializer.data})

    def post(self, request):
        # django  --  request.POST, request.body

        # drf -- request.data
        # data = request.data

        # 1.接收参数,获取参数
        data = request.data
        # 2.验证参数
        serializer = BookInfoModelSerializer(data=data)
        serializer.is_valid()
        # 3.保存数据
        serializer.save()
        # 4.返回响应
        return Response(serializer.data)

        # return JsonResponse({'code':'post'})


###############二级视图#################################################################
from rest_framework.generics import GenericAPIView

"""
GenericAPIView 比 APIView 扩展了一些属性和方法


属性
    queryset                设置查询结果集
    serializer_class        设置序列化器
    lookup_field            设置查询指定数据的关键字参数
方法
    get_queryset()          获取查询结果集
    get_serializer()        获取序列化器实例
    get_object()            获取到指定的数据
"""


# 列表视图
class BookInfoGenericAPIView(GenericAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

    def get(self, request):
        # 1.查询所有数据
        # books=BookInfo.objects.all()
        # books=self.queryset
        books = self.get_queryset()

        # 2.将查询结果集进行遍历,转换为字典列表
        # serializer=BookInfoModelSerializer(books,many=True)
        # serializer=self.serializer_class(books,many=True)
        serializer = self.get_serializer(books, many=True)

        # 3.返回响应
        return Response(serializer.data)

    def post(self, request):
        # 1.接收参数,获取参数
        data = request.data
        # 2.验证参数
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        # 3.保存数据
        serializer.save()
        # 4.返回响应
        return Response(serializer.data)


# 详情视图
class BookInfoDetailGenericAPIView(GenericAPIView):
    # 查询所有数据.因为查询结果集有惰性 以及后续的代码可以采用 self.queryset.filter(id=pk) 属性.
    # 所以 我们就直接设置 所有查询结果就可以
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

    # 设置关键字参数的名字
    lookup_field = 'id'

    def get(self, request, id):
        # 1.查询指定数据
        # book=BookInfo.objects.get(id=pk)
        # book=self.queryset.get(id=pk)
        # book=self.get_queryset().get(id=pk)
        book = self.get_object()
        # 2.将对象数据转换为字典数据
        serializer = self.get_serializer(instance=book)
        # 3.返回响应
        return Response(serializer.data)

    def put(self, request, id):
        # 1.查询指定的数据
        book = self.get_object()
        # 2.接收参数,获取参数
        data = request.data
        # 3.验证参数
        serializer = self.get_serializer(instance=book, data=data)
        serializer.is_valid(raise_exception=True)
        # 4.更新数据
        serializer.save()
        # 5.返回响应
        return Response(serializer.data)

    def delete(self, request, id):
        # 1. 接收参数,查询数据
        book = self.get_object()
        # 2. 操作数据库(删除)
        book.delete()
        # 3. 返回响应
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)


##############二级视图与Mixin配合使用###########################################################
from rest_framework.mixins import ListModelMixin, CreateModelMixin


# GenericAPIView 一般和mixin配合使用
# 列表视图
class BookInfoGenericMixinAPIView(ListModelMixin,
                                  CreateModelMixin,
                                  GenericAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 详情视图
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class BookInfoDetailGenericMixinAPIVIiew(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()

    serializer_class = BookInfoModelSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)


##################三级视图#####################################################
from rest_framework.generics import ListCreateAPIView


class BookInfoListCreaetAPIView(ListCreateAPIView):
    # 查询结果集
    queryset = BookInfo.objects.all()
    # 序列化器
    serializer_class = BookInfoModelSerializer


############################视图集##########################################################

from rest_framework.viewsets import ViewSet, ModelViewSet

"""
视图集 继承自 APIView --> APIView 继承自 View
如果我们想把 增删改查 都放到一个视图集里,原则上还是不行!!!
为什么???
因为 一个类视图 的http方法 不能重复
获取数据 有2个get  get所有数据  get某一个数据

"""
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from book.serializers import BookInfoModelSerializer


class BookViewSet(ViewSet):

    # 获取所有书籍   GET       books/
    def list(self, request):
        queryset = BookInfo.objects.all()
        serializer = BookInfoModelSerializer(queryset, many=True)
        return Response(serializer.data)

    # 获取指定书籍 GET         books/pk/
    def retrieve(self, request, pk=None):
        queryset = BookInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BookInfoModelSerializer(user)
        return Response(serializer.data)


#############################################################################
from rest_framework.viewsets import ModelViewSet


# ModelViewSet 基本使用
class BookInfoModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()

    serializer_class = BookInfoModelSerializer


##########################高级功能################################################
"""
1. 概念
2. 配置
3. 效果
"""

# 定义一个 视图集
from book.models import PeopleInfo
from book.serializers import PeopleInfoModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

# 系统为我们提供了2个分页类
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView


class PageNum(PageNumberPagination):
    # 开启分页的开关
    page_size = 5
    # 设置查询字符串的key 相当于 开关.只有设置了这个值.一页多少条记录才生效
    page_size_query_param = 'ps'

    # 一页最多多少条记录
    max_page_size = 20


class PeopleInfoModelViewSet(ModelViewSet):
    # 给视图 单独设置权限
    # permission_classes = [AllowAny]

    # 单独设置分页类
    pagination_class = PageNum

    # queryset = PeopleInfo.objects.all()
    # 或者
    def get_queryset(self):
        return PeopleInfo.objects.all()

    # serializer_class = PeopleInfoModelSerializer
    # 或者
    def get_serializer_class(self):
        return PeopleInfoModelSerializer
