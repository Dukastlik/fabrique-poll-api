from django.contrib import admin
from django.urls import path, include

from polls import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register(r'polls', views.PollViewSet)
router.register(r'answers', views.ChoiceViewSet, basename='keygen')
router.register(r'keygen', views.KeyGen, basename='keygen')


polls_router = routers.NestedSimpleRouter(router, r'polls', lookup='poll')
polls_router.register(r'questions', views.QuestionViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(polls_router.urls)),
]
