from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.generic import TemplateView

# router = DefaultRouter()
# router.register('crime', views.CongressViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('', TemplateView.as_view(template_name = 'crime/index.html'), name='congresslist'),
    path('<str:district>/', views.search, name="search"),
]
