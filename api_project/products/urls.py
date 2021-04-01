from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'products'

router = routers.DefaultRouter()
router.register('category', views.CategoryView)
router.register('list', views.ProductsListView)
router.register('review', views.ProductReviewApi, basename='review-api')

urlpatterns = [
     path('', include(router.urls)),
]
