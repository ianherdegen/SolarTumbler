from django.urls import path
from . import views

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'SolarTumbler'
urlpatterns = [
    path('', views.LogEntryList.as_view(), name='all'),
    path('main/create/', views.LogEntryCreate.as_view(), name='logentry_create'),
    path('main/<int:pk>/update/', views.LogEntryUpdate.as_view(), name='logentry_update'),
    path('main/<int:pk>/delete/', views.LogEntryDelete.as_view(), name='logentry_delete'),
    path('lookup/', views.ItemView.as_view(), name='item_list'),
    path('lookup/create/', views.ItemCreate.as_view(), name='item_create'),
    path('lookup/<int:pk>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('lookup/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
]

# Note that logentry_ and logentry_ give us uniqueness within this applilogentryion