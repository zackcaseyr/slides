from django.urls import path
from . import views

urlpatterns = [
    # Class URLs
    path('', views.ClassListView.as_view(), name='class-list'),
    path('class/<int:pk>/', views.ClassDetailView.as_view(), name='class-detail'),
    path('class/create/', views.ClassCreateView.as_view(), name='class-create'),
    path('class/<int:pk>/update/', views.ClassUpdateView.as_view(), name='class-update'),
    path('class/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class-delete'),

    # Topic URLs
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('topic/create/', views.TopicCreateView.as_view(), name='topic-create'),
    path('topic/create-with-slides/', views.TopicWithSlidesCreateView.as_view(), name='topic-create-with-slides'),
    path('topic/<int:pk>/update/', views.TopicUpdateView.as_view(), name='topic-update'),
    path('topic/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic-delete'),
    path('topic/<int:pk>/present/', views.PresentationView.as_view(), name='topic-present'),
    path('topic/<int:pk>/pdf/', views.TopicPDFView.as_view(), name='topic-pdf'),

    # Slide URLs
    path('slides/', views.SlideListView.as_view(), name='slide-list'),
    path('slide/<int:pk>/', views.SlideDetailView.as_view(), name='slide-detail'),
    path('slide/create/', views.SlideCreateView.as_view(), name='slide-create'),
    path('slide/<int:pk>/update/', views.SlideUpdateView.as_view(), name='slide-update'),
    path('slide/<int:pk>/delete/', views.SlideDeleteView.as_view(), name='slide-delete'),
]
