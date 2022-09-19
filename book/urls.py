from django.urls import path
from book import views

urlpatterns = [
    # path('books/', views.BookListView.as_view()),
    # path('books/<int:pk>/', views.BookDetailView.as_view()),
    #
    # path('apibooks/', views.BookListAPIView.as_view()),
    # # #二级视图 GenericAPIView
    # path('genericbooks/', views.BookInfoGenericAPIView.as_view()),
    # path('genericbooks/<id>/', views.BookInfoDetailGenericAPIView.as_view()),
    # # #二级视图 GenericAPIView与mixin配合使用
    # path('mixinbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    # # #三级视图
    # path('thressbooks/', views.BookInfoListCreaetAPIView.as_view()),
    # #
    # # #视图集
    # path('viewsetbooks/', views.BookViewSet.as_view({'get': 'list'})),
    # path('viewsetbooks/<pk>/', views.BookViewSet.as_view({'get': 'retrieve'})),
]

# 视图集的路由比较特殊.我们可以借助于 drf 的 router 帮实现
from rest_framework.routers import DefaultRouter, SimpleRouter

"""
DefaultRouter,SimpleRouter
共同点: 都可以帮助 视图集自动生成路由
不同点:
    DefaultRouter:  http://127.0.0.1:8000/ 根路由可以访问
    SimpleRouter    http://127.0.0.1:8000/ 根路由不可以访问
"""

# 1. 创建router实例
router = SimpleRouter()
# 2. 设置列表视图和详情视图的公共部分(不包括/部分)
# prefix,              路由. 列表视图和详情视图的公共部分(不包括最后的/部分)
#                       router会生成2个路由,一个是列表视图的路由 prefix.另外一个是详情视图的路由 prefix/pk/
# viewset,              视图集
# basename=None         给列表视图和详情视图的路由设置别名.
#                       别名的规范是 列表视图是: basename-list   详情视图是: basename-detail
#                       因为 别名的原因.所以 basename 不要重复.一般我们都是以 prefix 作为basename.因为prefix不会重复

router.register('abc', views.BookInfoModelViewSet, basename='abc')

# 3.将router生成的路由,追加到 urlpatterns
# urlpatterns += router.urls


#######################################
router.register('people', views.PeopleInfoModelViewSet, basename='people')

urlpatterns += router.urls
