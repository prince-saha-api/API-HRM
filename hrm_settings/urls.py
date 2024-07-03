from django.urls import path
from hrm_settings import views

urlpatterns = [
    path('get-weekdays/', views.getweekdays, name='get-weekdays'),
    # path('add-weekdays/', views.addweekdays, name='add-weekdays'),
    # path('update-weekdays/<int:weekdaysid>', views.updateweekdays, name='update-weekdays'),
    # path('delete-weekdays/<int:weekdaysid>', views.deleteweekdays, name='delete-weekdays'),

    path('get-generalsettings/', views.getgeneralsettings, name='get-generalsettings'),
    path('add-generalsettings/', views.addgeneralsettings, name='add-generalsettings'),
    path('update-generalsettings/<int:generalsettingsid>', views.updategeneralsettings, name='update-generalsettings'),
    # path('add-fiscalyear/', views.addfiscalyear, name='add-fiscalyear'),
    # path('update-fiscalyear/<int:fiscalyearid>', views.updatefiscalyear, name='update-fiscalyear'),
    # path('delete-fiscalyear/<int:fiscalyearid>', views.deletefiscalyear, name='delete-fiscalyear'),
]
