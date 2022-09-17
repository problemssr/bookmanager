from django.urls import path
from book import views

urlpatterns = [
    path('books/', views.BookListView.as_view()),
    path('books/<int:pk>/', views.BookDetailView.as_view()),

    path('apibooks/', views.BookListAPIView.as_view()),
    # #二级视图 GenericAPIView
    path('genericbooks/', views.BookInfoGenericAPIView.as_view()),
    path('genericbooks/<id>/', views.BookInfoDetailGenericAPIView.as_view()),
    # #二级视图 GenericAPIView与mixin配合使用
    path('mixinbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    # #三级视图
    path('thressbooks/', views.BookInfoListCreaetAPIView.as_view()),
    #
    # #视图集
    path('viewsetbooks/', views.BookViewSet.as_view({'get': 'list'})),
    path('viewsetbooks/<pk>/', views.BookViewSet.as_view({'get': 'retrieve'})),
]
