from rest_framework import serializers

"""
drf 框架 能够帮助我们实现  序列化和反序列化的功能  (对象和字典的相互转换)


BookInfo(对象)        ---序列化器类--->             字典

豆子                  ---豆浆机--->              豆浆


序列化器类
    ① 将对象转换为字典
    ② 将字典转换为对象  -- 反序列化


序列化器类的定义
    ① 参考模型来定义就可以了


class 序列化器名字(serializers.Serializer):
    字段名=serializer.类型(选项)


    字段名和模型字段名一致
    字段的类型和模型的类型一致

"""


class PeopleRelatedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    pub_date = serializers.DateField()
    readcount = serializers.IntegerField()

    people = PeopleRelatedSerializer(many=True)
    """
    {
     'id': 1, 'name': '射雕英雄传', 'pub_date': '1980-05-01', 'readcount': 12,
     'people': [
                    OrderedDict([('id', 1), ('name', '郭靖'), ('passwor3456abc')]), 
                    OrderedDict([('id', 2), ('name', '黄蓉'), ('password', '123456abc')]),
                    OrderedDict([('id', 3), ('name', '黄药师'), ('passwor123456abc')]), 
                    OrderedDict([('id', 4), ('name', '欧阳锋'), ('password', '123456abc')]), 
                    OrderedDict([('id', 5), ('name', '梅超风'), ('pas, '123456abc')])
                ]
    }

    """


################定义人物模型对应的序列化器#####################

from book.models import BookInfo


class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    book_id = serializers.IntegerField()

    ###对外键进行学习
    # ①  如果我们定义的序列化器外键字段类型为 IntegerField
    # 那么,我们定义的序列化器字段名 必须和数据库中的外键字段名一致
    # book_id=serializers.IntegerField()

    # ② 如果我们期望的外键数据的key就是模型字段的名字,那么 PrimaryKeyRelatedField 就可以获取到关联的模型id值
    # queryset 在验证数据的时候,我们要告诉系统,在哪里匹配外键数据
    # book=serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())
    # 或者
    # read_only=True 意思就是 我不验证数据了
    # book=serializers.PrimaryKeyRelatedField(read_only=True)

    # ③ 如果我们期望获取外键关联的 字符串的信息, 这个时候 我们可以使用 StringRelationField
    # book=serializers.StringRelatedField()

    # ④ 如果我们期望获取, book 所关联的模型的 所有数据,这个时候我们就定义 book=BookInfoSerializer()
    # book=关联的BookInfo的一个关联对象数据
    # book=BookInfo.objects.get(id=xxx)

    # book=BookInfoSerializer(instance=book).data
    # 等号右边的 book 是模型对象
    # 等号左边的book 是字典数据
    # book=BookInfoSerializer()
    """
    {
    'id': 1, 'name': '郭靖', 'password': '123456abc', 'description': '降龙十八掌', 'is_delete': False, 
    'book': OrderedDict([('id', 1), ('name','射雕英雄传'), ('pub_date', '1980-05-01'), ('readcount', 12)])
    }

    """


"""

①book:1                             PrimaryKeyRelationField                                                       

②book_id:1                          IntergerField

③book:射雕英雄传                      StringRelationField

④book: {id:1,name:射雕英雄传,readcount:10}   BookInfoSerializer


"""
