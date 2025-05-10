# urls.py

from django.urls import path
from .views import GradeListView, BoardListView

urlpatterns = [
    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('boards/', BoardListView.as_view(), name='board-list'),
]
