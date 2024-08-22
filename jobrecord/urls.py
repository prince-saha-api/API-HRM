from django.urls import path
from jobrecord import views

urlpatterns = [
    path('get-jobhistory/', views.getjobhistorys, name='get-jobhistory'),
    path('add-jobhistory/', views.addjobhistory, name='add-jobhistory'),
    # path('update-jobhistory/<int:jobhistoryid>', views.updatejobhistory, name='update-jobhistory'),
    # path('delete-jobhistory/<int:jobhistoryid>', views.deletejobhistory, name='delete-jobhistory'),
]