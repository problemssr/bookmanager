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


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    pub_data = serializers.DateField()
    reacount = serializers.IntegerField()
    pass
