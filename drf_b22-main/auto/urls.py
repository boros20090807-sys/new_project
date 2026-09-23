from django.urls import path, include
from .views import (
    register,
    login,
    logout,
    GamesReviewDetailView,
    GamesViewSet,
    PublisherViewSet,
    SystemViewSet,
    GamesReviewViewSet,
    SystemDetailView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'publisher',PublisherViewSet)
router.register(r'system',SystemViewSet)
router.register(r'games',GamesViewSet)
router.register(r'review',GamesReviewViewSet)

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('games_review/<int:pk>/', GamesReviewDetailView.as_view()),
    path('sistem/<int:pk>/', SystemDetailView.as_view()),
    # path('sistem', SystemListCreateView.as_view()),
    # path('sistem/<int:pk>/', SystemDetailView.as_view()),
    # path('games/', AutoLisCreateView.as_view()),
    # path('games/<int:pk>/', AutoDetailView.as_view()),
    path('', include(router.urls))
]

