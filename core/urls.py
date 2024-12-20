from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('todo', views.TaskViewSet, basename='todos')


urlpatterns = [

    path('api/v1/', include(router.urls)),
    path('', TemplateView.as_view(template_name='core/index.html')),

]
