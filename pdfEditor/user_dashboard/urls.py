from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("history", views.history, name="history"),
    path('files_data', views.get_files, name='get_files'),
    path('history_data', views.get_history, name='get_history'),
    path('upload_pdf', views.upload_pdf_file, name='upload_pdf_file'),
    path('del_data', views.delete_data, name='delete_data'),
    path('editor', views.file_editor, name='file_editor'),
    path('update_data', views.update_data, name='update_data'),
    path('download_pdf', views.download_pdf_file, name='download_pdf_file'),
    path('rename_pdf', views.rename_file, name='rename_file'),
]