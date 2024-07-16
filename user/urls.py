from django.urls import path
from user import views
urlpatterns = [
    path('get-responsibility/', views.getresponsibilitys, name='get-responsibility'),
    path('add-responsibility/', views.addresponsibility, name='add-responsibility'),
    path('get-requiredskill/', views.getrequiredskills, name='get-requiredskill'),
    path('add-requiredskill/', views.addrequiredskill, name='add-requiredskill'),
    
    path('get-dsignation/', views.getdsignations, name='get-dsignation'),
    path('add-dsignation/', views.adddsignation, name='add-dsignation'),
    path('update-designation/<int:designationid>', views.updatedesignation, name='update-designation'),
    path('delete-designation/<int:designationid>', views.deletedesignation, name='delete-designation'),

    path('get-grade/', views.getgrades, name='get-grade'),
    path('add-grade/', views.addgrade, name='add-grade'),
    path('update-grade/<int:gradeid>', views.updategrade, name='update-grade'),
    path('delete-grade/<int:gradeid>', views.deletegrade, name='delete-grade'),

    path('get-shift/', views.getshifts, name='get-shift'),
    path('add-shift/', views.addshift, name='add-shift'),
    path('update-shift/<int:shiftid>', views.updateshift, name='update-shift'),
    path('delete-shift/<int:shiftid>', views.deleteshift, name='delete-shift'),

    path('get-shiftchangerequest/', views.getshiftchangerequest, name='get-shiftchangerequest'),
    path('add-shiftchangerequest/', views.addshiftchangerequest, name='add-shiftchangerequest'),
    path('update-shiftchangerequest/<int:shiftchangerequestid>', views.updateshiftchangerequest, name='update-shiftchangerequest'),
    path('approve-shiftchangerequest/<int:shiftchangerequestid>', views.approveshiftchangerequest, name='approve-shiftchangerequest'),
    path('reject-shiftchangerequest/<int:shiftchangerequestid>', views.rejectshiftchangerequest, name='reject-shiftchangerequest'),
    path('delete-shiftchangerequest/<int:shiftchangerequestid>', views.deleteshiftchangerequest, name='delete-shiftchangerequest'),

    path('get-shiftchangelog/', views.getshiftchangelog, name='get-shiftchangelog'),
    
    path('get-religion/', views.getreligions, name='get-religion'),
    path('add-religion/', views.addreligion, name='add-religion'),
    path('update-religion/<int:religionid>', views.updatereligion, name='update-religion'),
    path('delete-religion/<int:religionid>', views.deletereligion, name='delete-religion'),

    path('get-permission/', views.getpermissions, name='get-permission'),
    path('add-permission/', views.addpermission, name='add-permission'),
    path('get-rolepermission/', views.getrolepermissions, name='get-rolepermission'),
    path('add-rolepermission/', views.addrolepermission, name='add-rolepermission'),
    path('get-ethnicgroup/', views.getethnicgroups, name='get-ethnicgroup'),
    path('add-ethnicgroup/', views.addethnicgroup, name='add-ethnicgroup'),

    path('get-employee/', views.getemployee, name='get-employee'),
    path('add-employee/', views.addemployee, name='add-employee'),
    
    path('update-profilepic/<int:userid>', views.updateprofilepic, name='update-profilepic'),
    path('update-profile/<int:userid>', views.updateprofile, name='update-profile'),
    path('update-personal-details/<int:userid>', views.updatepersonaldetails, name='update-personal-details'),
    path('update-official-details/<int:userid>', views.updateofficialdetails, name='update-official-details'),
    path('update-salary-leaves/<int:userid>', views.updatesalaryleaves, name='update-salary-leaves'),
    
]
