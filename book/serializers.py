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

from rest_framework import serializers
from book.models import BookInfo

class BookInfoSerializer(serializers.Serializer):

    id =serializers.IntegerField(read_only=True)
    name =serializers.CharField(write_only=True,max_length=10,min_length=5)
    pub_date =serializers.DateField(required=True)
    readcount =serializers.IntegerField(required=False)
    commentcount=serializers.IntegerField(required=False)

    #单个字段验证
    def validate_readcount(self,value):

        # 写 额外的检测代码
        if value<0:
            #raise Exception('阅读量不能为负数')

            # rest_framework.exceptions.ValidationError:
            raise serializers.ValidationError('阅读量不能为负数')

        return value

    # 多个字段验证
    # attrs = data
    # def validate(self, attrs):
    def validate(self, data):

        readcount=data.get('readcount')
        commentcount=data.get('commentcount')

        # if readcount<0:
        #     raise serializers.ValidationError('')

        if commentcount>readcount:
            raise serializers.ValidationError('评论量不能大于阅读量')

        return data

    """
    如果我们的序列化器是继承自Serialzier
    当调用序列化器的save方法的时候,会触发调用 序列化器的create方法
    """
    def create(self, validated_data):
        # validated_data  验证没有问题的数据
        # 如果我们的data 经过我们的层层验证,没有问题,则
        # validated_data = data

        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance,         序列化器创建的时候 传递的对象
        # validated_data    序列化器创建的时候 验证没有问题的数据

        # get(key,default_value)
        # 如果 get的key是一个None,则使用 默认值
        instance.name=validated_data.get('name',instance.name)
        instance.pub_date=validated_data.get('pub_date',instance.pub_date)
        instance.readcount=validated_data.get('readcount',instance.readcount)
        instance.commentcount=validated_data.get('commentcount',instance.commentcount)
        instance.save()  #调用保存方法,数据才会入库
        return instance

###################################################################
class BookInfoModelSerializer(serializers.ModelSerializer):
    # name=serializers.CharField(max_length=10,min_length=5,required=True)
    class Meta:
        model=BookInfo          # ModelSerializer 必须设置 model
        fields='__all__'        # 设置自动生成的字段列表  __all__ 表示所有
        # fields=['id','name']        # 列表或者元组
        # exclude=['id','name']                    # 除去列表中的字段,其他的字段都生成

        # 只读字段列表
        read_only_fields=['id','name','pub_date']

        # 选项设置
        extra_kwargs = {
            # '字段名': { '选项名':value, },
            'name': {
                'max_length':40,
                'min_length':10
            }
        }


from rest_framework import serializers
from book.models import PeopleInfo, BookInfo

"""
1. 将对象转换为字典 -- 序列化
2. 验证我们的字典数据 -- 反序列化的一部分
3. 能够将我们的字典数据保存 -- 反序列化的一部分
"""
"""
 'book':1,
'name': '靖哥哥',
'password': '123456abc',
"""


class PeopleInfoModelSerializer(serializers.ModelSerializer):
    # password=serializers.CharField(write_only=True,max_length=20)
    book_id = serializers.IntegerField(required=False)

    class Meta:
        model = PeopleInfo
        fields = ['id', 'book_id', 'name', 'password', 'is_delete', 'description']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'is_delete': {
                'read_only': True
            }
        }


class BookInfoModelSerializer(serializers.ModelSerializer):
    people = PeopleInfoModelSerializer(many=True)

    class Meta:
        model = BookInfo
        fields = '__all__'

    """
    序列化器嵌套序列化器写入数据的时候.默认系统是不支持写入的
    我们需要自己实现create方法 来实现数据的写入

    validate:
    data={
        'name':'离离原上草',

    }

    people 
    'people':[
            {
                'name': '靖妹妹111',
                'password': '123456abc'
            },
            {
                'name': '靖表哥222',
                'password': '123456abc'
            }
        ]

    写入数据的思想是:  因为 当前 书籍和人物的关系是 1对多  应该先写入 1的模型数据,再写入 多的模型数据

    data.pop('people')  'name':'离离原上草',

    people 再写入 people列表数据

    """

    def create(self, validated_data):
        # 1. 先把 validated_data 的嵌套数据 分解开
        people = validated_data.pop('people')

        # validated_data
        # 2. 写入书籍信息
        book = BookInfo.objects.create(**validated_data)

        # 3. 对字典列表进行遍历
        for item in people:
            """
            item 
            {
                'name': '靖表哥222',
                'password': '123456abc'
            }
            """
            PeopleInfo.objects.create(book=book, **item)

        return book