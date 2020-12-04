from django.urls import path
from . import views

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'SolarTumbler'
urlpatterns = [
    path('', views.LogEntryList.as_view(), name='all'),
    path('main/create/', views.LogEntryCreate.as_view(), name='logentry_create'),
    path('main/<int:pk>/update/', views.LogEntryUpdate.as_view(), name='logentry_update'),
    path('logentry/<int:pk>', views.LogEntryDetailView.as_view(), name='logentry_detail'),
    path('main/<int:pk>/delete/', views.LogEntryDelete.as_view(), name='logentry_delete'),
    path('lookup/', views.GroupView.as_view(), name='group_list'),
    path('lookup/create/', views.GroupCreate.as_view(), name='group_create'),
    path('lookup/<int:pk>/update/', views.GroupUpdate.as_view(), name='group_update'),
    path('lookup/<int:pk>/delete/', views.GroupDelete.as_view(), name='group_delete'),
    path('logentry/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='logentry_comment_create'),
    path('logentry/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='logentry_favorite'),
    path('logentry/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='logentry_unfavorite'),
]

# Note that logentry_ and logentry_ give us uniqueness within this applilogentryion