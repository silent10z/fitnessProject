from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'free'

urlpatterns = [
    path('', views.FreeListView.as_view(), name="list"),
    path('<int:pk>/', views.free_detail_view, name="detail"),
    path('write/', views.free_write_view, name="write"),
    path('<int:pk>/edit/', views.free_edit_view, name="edit"),
    path('<int:pk>/delete/', views.free_delete_view, name="delete"),
    path('download/<int:pk>', views.free_download_view, name="free_download"),
    path('<int:pk>/comment/writer/', views.comment_write_view, name="comment_write"),
    path('<int:pk>/comment/delete/', views.comment_delete_view, name="comment_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)