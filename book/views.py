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
data = {
    'name': 'django',
    'pub_date': '2018-1-1',
    'readcount': 666
}
# 2. 创建序列化器,将字典数据给序列化器
# BookInfoSerializer(instance,data)
# instance 用于序列化(对象转换为字典)
# data 用于反序列化(字典转换为对象)
serializer = BookInfoSerializer(data=data)

# 3. 验证数据
# 如果我们的数据 正确(满足需求) 返回True
# 如果我们的数据 不正确(不满足需求) 返回False
serializer.is_valid(raise_exception=True)
# 4. 保存,获取对象


######################反序列化数据验证##########################
from book.serializers import BookInfoSerializer

# 1. 模拟字典数据
data = {
    'name':'django',
    'pub_date':'2020-1-1',
    'readcount':100,
    'commentcount':10
}
# 2. 创建序列化器,将字典数据传递给序列化器
serializer=BookInfoSerializer(data=data)
# 3. 验证数据
serializer.is_valid(raise_exception=True)
# 4.验证数据没有问题之后,就可以调用保存方法了
serializer.save()


#######################################################################
from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 模拟一个对象数据
book=BookInfo.objects.get(id=1)
# 2. 模拟一个字典数据
data={
    'name':'射雕英雄后传',
    'pub_date':'2000-1-1',
    'readcount':999,
    'commentcount':666
}
# 3. 把对象和字典都传递给序列化器的创建
serializer=BookInfoSerializer(instance=book,data=data)

# 4. 验证数据
serializer.is_valid(raise_exception=True)
# 5. 数据的更新操作
serializer.save()
# 6.会获取新字典数据
serializer.data


#####################################
from book.serializers import BookInfoModelSerializer

data={
    'name':'射雕英雄~~~~',
    'pub_date':'2000-1-1',
    'readcount':999,
    'commentcount':666
}

serializer=BookInfoModelSerializer(data=data)
serializer.is_valid(raise_exception=True)
serializer.save()


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

# 1. 模拟数据
data = {
    'name': '离离原上草',
    'people': [
        {
            'name': '靖妹妹111',
            'password': '123456abc'
        },
        {
            'name': '靖表哥222',
            'password': '123456abc'
        }
    ]
}

# 2. 将字典数据传递给序列化器,创建序列化器对象
serializer = BookInfoModelSerializer(data=data)
# 3. 验证数据
serializer.is_valid(raise_exception=True)
# 4. 保存数据
serializer.save()

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
        data = request.data

        return JsonResponse({'code': 'post'})