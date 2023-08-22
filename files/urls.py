from django.urls import path

from files.views import file_detail, FileAdd, file_delete, FileUpdate

app_name = 'files'

urlpatterns = [
    path('add/', FileAdd.as_view(), name='file_add'),
    path('<int:file_id>/', file_detail, name='file_detail'),
    path('<int:file_id>/delete/', file_delete, name='file_delete'),
    path('<int:pk>/update/', FileUpdate.as_view(), name='file_update'),
]
