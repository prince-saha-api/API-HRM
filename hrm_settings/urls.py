from django.urls import path
from hrm_settings import views

urlpatterns = [
    path('get-weekdays/', views.getweekdays, name='get-weekdays'),
    path('get-generalsettings/', views.getgeneralsettings, name='get-generalsettings'),
    # path('add-generalsettings/', views.addgeneralsettings, name='add-generalsettings'),
    path('update-generalsettings/<int:generalsettingsid>', views.updategeneralsettings, name='update-generalsettings')
]
