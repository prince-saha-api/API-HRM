from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user import models as MODELS_U
from contribution import models as MODELS_CON
from company import models as MODELS_COM
from branch import models as MODELS_BR
from leave import models as MODELS_LE
from department import models as MODELS_DE
from hrm_settings import models as MODELS_SE
from user.serializer import serializers as SRLZER_U
from rest_framework.response import Response
from rest_framework import status
from helps.common.generic import Generichelps as ghelp
# from helps.common.generic import Generichelps as ghelp
# from django.core.paginator import Paginator
import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getresponsibilitys(request):
    responsibilitys = MODELS_U.Responsibility.objects.all()
    responsibilityserializers = SRLZER_U.Responsibilityserializer(responsibilitys, many=True)
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
@permission_classes([IsAuthenticated])
def addresponsibility(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Responsibility, SRLZER_U.Responsibilityserializer, request.data, 'title')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getrequiredskills(request):
    requiredskills = MODELS_U.Requiredskill.objects.all()
    requiredskillserializers = SRLZER_U.Requiredskillserializer(requiredskills, many=True)
    return Response(requiredskillserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addrequiredskill(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Requiredskill, SRLZER_U.Requiredskillserializer, request.data, 'title')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getdsignations(request):
    dsignations = MODELS_U.Designation.objects.all()
    designationserializers = SRLZER_U.Designationserializer(dsignations, many=True)
    return Response(designationserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddsignation(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Designation, SRLZER_U.Designationserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getgrades(request):
    grades = MODELS_U.Grade.objects.all()
    gradeserializers = SRLZER_U.Gradeserializer(grades, many=True)
    return Response(gradeserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addgrade(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Grade, SRLZER_U.Gradeserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getshifts(request):
    shifts = MODELS_U.Shift.objects.all()
    shiftserializers = SRLZER_U.Shiftserializer(shifts, many=True)
    return Response(shiftserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addshift(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Shift, SRLZER_U.Shiftserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getreligions(request):
    religions = MODELS_U.Religion.objects.all()
    religionserializers = SRLZER_U.Religionserializer(religions, many=True)
    return Response(religionserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addreligion(request):
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(MODELS_U.Religion, SRLZER_U.Religionserializer, request.data, 'name')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getemployee(request):
    users = MODELS_U.User.objects.all()
    userserializers = SRLZER_U.Userserializer(users, many=True)
    return Response(userserializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def addemployee(request):
    personalDetails = request.data.get('personalDetails')
    officialDetails = request.data.get('officialDetails')
    salaryAndLeaves = request.data.get('salaryAndLeaves')
    emergencyContact = request.data.get('emergencyContact')
    academicRecord = request.data.get('academicRecord')
    previousExperience = request.data.get('previousExperience')
    uploadDocuments = request.data.get('uploadDocuments')

    if ghelp().ifallrecordsexistornot(MODELS_U.Ethnicgroup, officialDetails.get('ethnic_group')):
        if ghelp().ifallrecordsexistornot(MODELS_LE.Leavepolicy, salaryAndLeaves.get('leavepolicy')):

            fiscal_year_salaryAndLeaves = MODELS_SE.Fiscalyear.objects.all().order_by('id')
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
                    if not MODELS_U.User.objects.filter(username=official_id).exists():
                        classOBJpackage = {
                            'User': MODELS_U.User,
                            'Address': MODELS_CON.Address,
                            'Designation': MODELS_U.Designation,
                            'Shift': MODELS_U.Shift,
                            'Grade': MODELS_U.Grade,
                            'Bankaccount': MODELS_CON.Bankaccount,
                            'Bankaccounttype': MODELS_CON.Bankaccounttype,
                            'Religion': MODELS_U.Religion,

                        }
                        userinstance = ghelp().createuser(classOBJpackage, personalDetails, officialDetails, salaryAndLeaves)


                        if officialDetails.get('role_permission'):
                            for id in officialDetails.get('role_permission'):
                                object = ghelp().getobject(MODELS_U.Rolepermission, id)
                                if object:
                                    userinstance.role_permission.add(object)


                        # ইউজার ক্রিয়েটের পরে।
                        ethnic_group_officialDetails = officialDetails.get('ethnic_group')
                        if ethnic_group_officialDetails:
                            for id in ethnic_group_officialDetails:
                                object = ghelp().getobject(MODELS_U.Ethnicgroup, id)
                                if object:
                                    object.user.add(userinstance)

                        leavepolicy_salaryAndLeaves = salaryAndLeaves.get('leavepolicy')
                        if leavepolicy_salaryAndLeaves:
                            for id in leavepolicy_salaryAndLeaves:
                                leavepolicy = ghelp().getobject(MODELS_LE.Leavepolicy, id)
                                if not MODELS_LE.Leavepolicyassign.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                    MODELS_LE.Leavepolicyassign.objects.create(user=userinstance, leavepolicy=leavepolicy)
                                    if not MODELS_LE.Leavesummary.objects.filter(user=userinstance, leavepolicy=leavepolicy).exists():
                                        MODELS_LE.Leavesummary.objects.create(
                                            user=userinstance,
                                            leavepolicy=leavepolicy,
                                            fiscal_year=fiscal_year_salaryAndLeaves,
                                            total_allocation=leavepolicy.allocation_days,
                                            total_consumed=0,
                                            total_left=leavepolicy.allocation_days
                                        )
                        
                        ghelp().addemergencycontact(MODELS_U.Employeecontact, MODELS_CON.Address, userinstance, emergencyContact)
                        ghelp().addacademicrecord(MODELS_U.Employeeacademichistory, userinstance, academicRecord)
                        ghelp().addpreviousexperience(MODELS_U.Employeeexperiencehistory, userinstance, previousExperience)


                        department_officialDetails = ghelp().getobject(MODELS_DE.Department, officialDetails.get('department'))
                        department_officialDetails.user.add(userinstance)
                        # company_officialDetails = ghelp().getobject(MODELS_COM.Company, officialDetails.get('company'))
                        # branch_officialDetails = ghelp().getobject(MODELS_BR.Branch, officialDetails.get('branch'))
                        # department_officialDetails = ghelp().getobject('''MODELS_BR.Branch''', officialDetails.get('department'))



                        return Response({'data': {}, 'message': '', 'status': 'success'}, status=status.HTTP_200_OK)
                    else: return Response({'data': {}, 'message': 'employee id is already exist!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                else: return Response({'data': {}, 'message': 'employee id is missing!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            else: return Response({'data': {}, 'message': 'please add fiscalyear first!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'data': {}, 'message': 'please add valid Leavepolicy!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': 'please add valid Ethnicgroup!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)



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