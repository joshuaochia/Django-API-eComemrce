from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('user-list', views.UserList, basename='user-list')
router.register('addresses', views.AddressView)
router.register('create', views.CreateUser, basename='create')
router.register('product-cart', views.CartViewSet, basename='cart')
router.register(
     'blog-comment',
     views.UserBlogCommentViewSet,
     basename='comment'
     )


urlpatterns = [
     path('', include(router.urls)),
     path('token/', views.UserToken.as_view(), name='token'),
     path('', views.ManagerUserView.as_view(), name='me')
]
