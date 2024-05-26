from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from contribution import models as MODELS_CONT
from leave import models as MODELS_LEAV
from department import models as MODELS_DEPA
from hrm_settings import models as MODELS_SETT
from user import models as MODELS_USER
from user.serializer import serializers as SRLZER_USER
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp
# from helps.common.generic import Generichelps as ghelp
# from django.core.paginator import Paginator
from drf_nested_forms.utils import NestedForm
import json

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getresponsibilitys(request):
    responsibilitys = MODELS_USER.Responsibility.objects.all()
    responsibilityserializers = SRLZER_USER.Responsibilityserializer(responsibilitys, many=True)
    return Response(responsibilityserializers.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addresponsibility(request):
#     title = request.data.get('title')
#     if title:
#         if not MODELS_U.Responsibility.objects.filter(title=title).exists():
#             responsibilityserializers = SRLZER_U.Responsibilityserializer(data=request.data, many=False)
#             if responsibilityserializers.is_valid():
#                 responsibilityserializers.save()
#                 return Response({'data': responsibilityserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_201_CREATED)
#         else: return Response({'data': {}, 'message': 'this title already exist!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
#     else: return Response({'data': {}, 'message': 'title is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addresponsibility(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Responsibility, SRLZER_USER.Responsibilityserializer, request.data, 'title')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getrequiredskills(request):
    requiredskills = MODELS_USER.Requiredskill.objects.all()
    requiredskillserializers = SRLZER_USER.Requiredskillserializer(requiredskills, many=True)
    return Response(requiredskillserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addrequiredskill(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Requiredskill, SRLZER_USER.Requiredskillserializer, request.data, 'title')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getdsignations(request):
    dsignations = MODELS_USER.Designation.objects.all()
    designationserializers = SRLZER_USER.Designationserializer(dsignations, many=True)
    return Response(designationserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def adddsignation(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Designation, SRLZER_USER.Designationserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgrades(request):
    grades = MODELS_USER.Grade.objects.all()
    gradeserializers = SRLZER_USER.Gradeserializer(grades, many=True)
    return Response(gradeserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addgrade(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Grade, SRLZER_USER.Gradeserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getshifts(request):
    shifts = MODELS_USER.Shift.objects.all()
    shiftserializers = SRLZER_USER.Shiftserializer(shifts, many=True)
    return Response(shiftserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addshift(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Shift, SRLZER_USER.Shiftserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getreligions(request):
    religions = MODELS_USER.Religion.objects.all()
    religionserializers = SRLZER_USER.Religionserializer(religions, many=True)
    return Response(religionserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addreligion(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Religion, SRLZER_USER.Religionserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getpermissions(request):
    permissions = MODELS_USER.Permission.objects.all()
    permissionserializers = SRLZER_USER.Permissionserializer(permissions, many=True)
    return Response(permissionserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addpermission(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Permission, SRLZER_USER.Permissionserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getrolepermissions(request):
    rolepermissions = MODELS_USER.Rolepermission.objects.all()
    rolepermissionserializers = SRLZER_USER.Rolepermissionserializer(rolepermissions, many=True)
    return Response(rolepermissionserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addrolepermission(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Rolepermission, SRLZER_USER.Rolepermissionserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getethnicgroups(request):
    ethnicgroups = MODELS_USER.Ethnicgroup.objects.all()
    ethnicgroupserializers = SRLZER_USER.Ethnicgroupserializer(ethnicgroups, many=True)
    return Response(ethnicgroupserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addethnicgroup(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_USER.Ethnicgroup, SRLZER_USER.Ethnicgroupserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getemployee(request):
    users = MODELS_USER.User.objects.all()
    userserializers = SRLZER_USER.Userserializer(users, many=True)
    return Response(userserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addemployee(request):
    # requestdata = dict(request.data)
    requestdata = ghelp().requestdata()
    options = {
        'allow_blank': True,
        'allow_empty': False
    }
    

    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)

    personalDetails = form.data.get('personalDetails')
    ghelp().preparepersonalDetails(personalDetails)
    officialDetails = form.data.get('officialDetails')
    ghelp().prepareofficialDetails(officialDetails)
    if 'official_id' not in officialDetails: return Response({'data': {}, 'message': 'official_id is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    if 'ethnic_group' not in officialDetails: return Response({'data': {}, 'message': 'ethnic_group is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
    salaryAndLeaves = form.data.get('salaryAndLeaves')
    ghelp().preparesalaryAndLeaves(salaryAndLeaves)
    emergencyContact = form.data.get('emergencyContact')
    ghelp().prepareemergencyContact(emergencyContact)
    academicRecord = form.data.get('academicRecord')
    ghelp().prepareacademicRecord(academicRecord)
    previousExperience = form.data.get('previousExperience')
    ghelp().preparepreviousExperience(previousExperience)

    # uploadDocuments = form.data.get('uploadDocuments')

    leavepolicy_salaryAndLeaves = salaryAndLeaves.get('leavepolicy')
    if leavepolicy_salaryAndLeaves:
        if not ghelp().ifallrecordsexistornot(MODELS_USER.Ethnicgroup, officialDetails.get('ethnic_group')):
            return Response({'data': {}, 'message': 'please add valid Ethnicgroup!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    if ghelp().ifallrecordsexistornot(MODELS_LEAV.Leavepolicy, salaryAndLeaves.get('leavepolicy')):

        fiscal_year_salaryAndLeaves = MODELS_SETT.Fiscalyear.objects.all().order_by('id')
        if fiscal_year_salaryAndLeaves.exists():
            fiscal_year_salaryAndLeaves = fiscal_year_salaryAndLeaves.last()

            # religion exist or not 
            # department exist or not
            # designation exist or not
            # shift exist or not
            # grade exist or not
            # role_permission exist or not
            # leavepolicy exist or not

            official_id = officialDetails.get('official_id')
            if official_id:
                classOBJpackage = {
                    'User': MODELS_USER.User,
                    'Address': MODELS_CONT.Address,
                    'Designation': MODELS_USER.Designation,
                    'Shift': MODELS_USER.Shift,
                    'Grade': MODELS_USER.Grade,
                    'Bankaccount': MODELS_CONT.Bankaccount,
                    'Bankaccounttype': MODELS_CONT.Bankaccounttype,
                    'Religion': MODELS_USER.Religion,
                }
                
                modelsuniquefields = ['personal_phone', 'nid_passport_no', 'tin_no', 'official_id', 'official_phone', 'rfid']
                response = ghelp().createuser(classOBJpackage, personalDetails, officialDetails, salaryAndLeaves, modelsuniquefields)
                if not response['flag']: return Response({'data': {}, 'message': response['message'], 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                userinstance = response['userinstance']

                role_permission_officialDetails = officialDetails.get('role_permission')
                if role_permission_officialDetails:
                    for id in role_permission_officialDetails:
                        object = ghelp().getobject(MODELS_USER.Rolepermission, id)
                        if object: userinstance.role_permission.add(object)


                # ইউজার ক্রিয়েটের পরে।
                ethnic_group_officialDetails = officialDetails.get('ethnic_group')
                if ethnic_group_officialDetails:
                    for id in ethnic_group_officialDetails:
                        object = ghelp().getobject(MODELS_USER.Ethnicgroup, id)
                        if object:
                            if object.name != 'all': object.user.add(userinstance)

                leavepolicy_salaryAndLeaves = salaryAndLeaves.get('leavepolicy')
                if leavepolicy_salaryAndLeaves:
                    for id in leavepolicy_salaryAndLeaves:
                        leavepolicy = ghelp().getobject(MODELS_LEAV.Leavepolicy, id)
                        if userinstance in leavepolicy.applicable_for.user.all() or leavepolicy.applicable_for.name == 'all':
                            if not MODELS_LEAV.Leavepolicyassign.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                MODELS_LEAV.Leavepolicyassign.objects.create(user=userinstance, leavepolicy=leavepolicy)
                                if not MODELS_LEAV.Leavesummary.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                    MODELS_LEAV.Leavesummary.objects.create(
                                        user=userinstance,
                                        leavepolicy=leavepolicy,
                                        fiscal_year=fiscal_year_salaryAndLeaves,
                                        total_allocation=leavepolicy.allocation_days,
                                        total_consumed=0,
                                        total_left=leavepolicy.allocation_days
                                    )
                
                emergencycontact = ghelp().addemergencycontact(MODELS_USER.Employeecontact, MODELS_CONT.Address, userinstance, emergencyContact)
                academicrecord = ghelp().addacademicrecord(MODELS_USER.Employeeacademichistory, userinstance, academicRecord)
                previousexperience = ghelp().addpreviousexperience(MODELS_USER.Employeeexperiencehistory, userinstance, previousExperience)


                department_officialDetails = ghelp().getobject(MODELS_DEPA.Department, officialDetails.get('department'))
                if department_officialDetails: department_officialDetails.user.add(userinstance)
                # company_officialDetails = ghelp().getobject(MODELS_COM.Company, officialDetails.get('company'))
                # branch_officialDetails = ghelp().getobject(MODELS_BR.Branch, officialDetails.get('branch'))
                # department_officialDetails = ghelp().getobject('''MODELS_BR.Branch''', officialDetails.get('department'))



                return Response({'data': {}, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)
            else: return Response({'data': {}, 'message': 'employee id is missing!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': 'please add fiscalyear first!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': 'please add valid Leavepolicy!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
# def getPermission(request, id):
#     if Permission.objects.filter(id=id).exists():
#         permission = Permission.objects.get(id=id)
#         permissionserializer=PermissionSerializer(permission, many=False)
#         return Response(permissionserializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'not found!'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Active Permissions', 'all'])
# def getActivePermissions(request):
#     permissions = Permission.objects.filter(active=True)
#     permissionserializer=PermissionSerializer(permissions, many=True)
#     return Response(permissionserializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Active Permissions', 'all'])
# def getInactivePermissions(request):
#     permissions = Permission.objects.filter(active=False)
#     permissionserializer=PermissionSerializer(permissions, many=True)
#     return Response(permissionserializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Permissions', 'all'])
# def getLoggedinUserPermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#            ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, all=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Active Permissions', 'all'])
# def getLoggedinUserActivePermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#             ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, active=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Loggedin User Inactive Permissions', 'all'])
# def getLoggedinUserInactivePermissions(request):
#     permissions = []
#     if request.user.username:
#         if User.objects.filter(username=request.user.username).exists():
#             ghelp().getPermissionsList(User=User, username=request.user.username, permissions=permissions, inactive=True)
#     return Response({'permissions': permissions}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Add Permission', 'all'])
# def addPermission(request):
#     permissionserializer=PermissionSerializer(data=request.data)
#     if permissionserializer.is_valid(raise_exception=True):
#         permissionserializer.save()
#         return Response(permissionserializer.data, status=status.HTTP_201_CREATED)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Update Permission', 'all'])
# def updatePermission(request, id):
#     if Permission.objects.filter(id=id).exists():
#         permission = Permission.objects.get(id=id)
#         permissionserializer=PermissionSerializer(permission, data=request.data, partial=True)
#         if permissionserializer.is_valid(raise_exception=True):
#             permissionserializer.save()
#             return Response(permissionserializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'validation failed!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#     else:
#         return Response({'message': 'not found!'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Update Permission', 'all'])
# def getUsersInfo(request):
#     customusers = CustomUser.objects.all()
#     customUserserializer = CustomUserSerializer(customusers, many=True)
#     return Response(customUserserializer.data, status=status.HTTP_200_OK)