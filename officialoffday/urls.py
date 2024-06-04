from django.urls import path
from officialoffday import views

urlpatterns = [
    path('get-offday/', views.getoffdays, name='get-offday'),
    path('add-offday/', views.addoffday, name='add-offday'),
    path('update-offday/<int:offdayid>', views.updateoffday, name='update-offday'),
]
