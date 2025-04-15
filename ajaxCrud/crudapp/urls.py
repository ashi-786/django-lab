from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('todo_data/', views.get_todo_data, name='get_todo_data'),
    path('add_data/', views.save_data, name='save_data'),
    path('del_data/', views.delete_data, name='delete_data'),
    path('edit_data/', views.get_edit_data, name='get_edit_data'),
    path('update_data/', views.update_data, name='update_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)