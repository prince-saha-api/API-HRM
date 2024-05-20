from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user import models as MODELS_U
from contribution import models as MODELS_CON
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addresponsibility(request):
    title = request.data.get('title')
    if title:
        if not MODELS_U.Responsibility.objects.filter(title=title).exists():
            responsibilityserializers = SRLZER_U.Responsibilityserializer(data=request.data, many=False)
            if responsibilityserializers.is_valid():
                responsibilityserializers.save()
                return Response({'data': responsibilityserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_201_CREATED)
        else: return Response({'data': {}, 'message': 'this title already exist!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': 'title is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    title = request.data.get('title')
    if title:
        if not MODELS_U.Requiredskill.objects.filter(title=title).exists():
            requiredskillserializers = SRLZER_U.Requiredskillserializer(data=request.data, many=False)
            if requiredskillserializers.is_valid():
                requiredskillserializers.save()
                return Response({'data': requiredskillserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_201_CREATED)
        else: return Response({'data': {}, 'message': 'this title already exist!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': 'title is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

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
    name = request.data.get('name')
    if name:
        if not MODELS_U.Designation.objects.filter(name=name).exists():
            designationserializers = SRLZER_U.Designationserializer(data=request.data, many=False)
            if designationserializers.is_valid():
                designationserializers.save()
                return Response({'data': designationserializers.data, 'message': '', 'status': 'success'}, status=status.HTTP_201_CREATED)
        else: return Response({'data': {}, 'message': 'this title already exist!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    else: return Response({'data': {}, 'message': 'title is required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    
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
    gradeserializers = SRLZER_U.Gradeserializer(data=request.data, many=False)
    if gradeserializers.is_valid():
        gradeserializers.save()
        return Response({'data': gradeserializers.data}, status=status.HTTP_201_CREATED)
    
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
    shiftserializers = SRLZER_U.Shiftserializer(data=request.data, many=False)
    if shiftserializers.is_valid():
        shiftserializers.save()
        return Response({'data': shiftserializers.data}, status=status.HTTP_201_CREATED)



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
    errors = []

    personalDetails = request.data.get('personalDetails')
    officialDetails = request.data.get('officialDetails')
    salaryAndLeaves = request.data.get('salaryAndLeaves')
    emergencyContact = request.data.get('emergencyContact')
    academicRecord = request.data.get('academicRecord')
    previousExperience = request.data.get('previousExperience')
    uploadDocuments = request.data.get('uploadDocuments')

    employeeId_officialDetails = officialDetails.get('employeeId')
    if employeeId_officialDetails:
        if not MODELS_U.User.objects.filter(username=employeeId_officialDetails).exists():
            # personalDetails
            firstName_personalDetails = personalDetails.get('firstName')
            lastName_personalDetails = personalDetails.get('lastName')
            email_personalDetails = personalDetails.get('email')

            designation_officialDetails = officialDetails.get('designation')
            try: designation_officialDetails = MODELS_U.Designation.objects.get(id=designation_officialDetails)
            except: designation_officialDetails = None

            grade_academicRecord = academicRecord.get('grade')
            try: grade_academicRecord = MODELS_U.Grade.objects.get(id=grade_academicRecord)
            except: grade_academicRecord = None

            shift_officialDetails = officialDetails.get('defaultShift')
            try: shift_officialDetails = MODELS_U.Shift.objects.get(id=shift_officialDetails)
            except: shift_officialDetails = None

            dob_personalDetails = personalDetails.get('dateOfBirth')
            bloodGroup_personalDetails = personalDetails.get('bloodGroup')
            fathersName_personalDetails = personalDetails.get('fathersName')
            mothersName_personalDetails = personalDetails.get('mothersName')
            maritalStatus_personalDetails = personalDetails.get('maritalStatus')
            gender_personalDetails = personalDetails.get('gender')
            spouseName_personalDetails = personalDetails.get('spouseName')


            # permanentAddress
            presentAddress_personalDetails = personalDetails.get('presentAddress')
            city_presentAddress_personalDetails = presentAddress_personalDetails.get('city')
            state_presentAddress_personalDetails = presentAddress_personalDetails.get('state')
            zipCode_presentAddress_personalDetails = presentAddress_personalDetails.get('zipCode')
            country_presentAddress_personalDetails = presentAddress_personalDetails.get('country')
            address_presentAddress_personalDetails = presentAddress_personalDetails.get('address')
            presentaddressinstance = MODELS_CON.Address()
            if city_presentAddress_personalDetails: presentaddressinstance.city=city_presentAddress_personalDetails
            if state_presentAddress_personalDetails: presentaddressinstance.state_division=state_presentAddress_personalDetails
            if zipCode_presentAddress_personalDetails: presentaddressinstance.post_zip_code=zipCode_presentAddress_personalDetails
            if country_presentAddress_personalDetails: presentaddressinstance.country=country_presentAddress_personalDetails
            if address_presentAddress_personalDetails: presentaddressinstance.address=address_presentAddress_personalDetails
            presentaddressinstance.save()


            # permanentAddress
            permanentAddress_personalDetails = personalDetails.get('permanentAddress')
            city_permanentAddress_personalDetails = permanentAddress_personalDetails.get('city')
            state_permanentAddress_personalDetails = permanentAddress_personalDetails.get('state')
            zipCode_permanentAddress_personalDetails = permanentAddress_personalDetails.get('zipCode')
            country_permanentAddress_personalDetails = permanentAddress_personalDetails.get('country')
            address_permanentAddress_personalDetails = permanentAddress_personalDetails.get('address')
            permanentaddressinstance = MODELS_CON.Address()
            if city_permanentAddress_personalDetails: permanentaddressinstance.city=city_permanentAddress_personalDetails
            if state_permanentAddress_personalDetails: permanentaddressinstance.state_division=state_permanentAddress_personalDetails
            if zipCode_permanentAddress_personalDetails: permanentaddressinstance.post_zip_code=zipCode_permanentAddress_personalDetails
            if country_permanentAddress_personalDetails: permanentaddressinstance.country=country_permanentAddress_personalDetails
            if address_permanentAddress_personalDetails: permanentaddressinstance.address=address_permanentAddress_personalDetails
            permanentaddressinstance.save()

            religion_personalDetails = personalDetails.get('religion')
            try: religion_personalDetails = MODELS_U.Religion.objects.get(id=religion_personalDetails)
            except: religion_personalDetails = None

            nationality_personalDetails = personalDetails.get('nationality')
            contactNo_personalDetails = personalDetails.get('contactNo')
            nidPassport_personalDetails = personalDetails.get('nidPassport')
            tinNo_personalDetails = personalDetails.get('tinNo')

            # bankAccount
            bankAccount_salaryAndLeaves = salaryAndLeaves.get('bankAccount')
            bankName_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('bankName')
            branch_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('branch')

            accountType_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('accountType')
            try: accountType_bankAccount_salaryAndLeaves=MODELS_CON.Bankaccounttype.objects.get(id=accountType_bankAccount_salaryAndLeaves)
            except: accountType_bankAccount_salaryAndLeaves=None

            accountingNo_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('accountingNo')
            routingNo_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('routingNo')
            swiftBIC_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('swiftBIC')

            address_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('address')
            city_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('city')
            state_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('state')
            zipCode_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('zipCode')
            country_bankAccount_salaryAndLeaves = bankAccount_salaryAndLeaves.get('country')
            bankAccountaddressinstance = MODELS_CON.Address()
            if address_bankAccount_salaryAndLeaves: bankAccountaddressinstance.address=address_bankAccount_salaryAndLeaves
            if city_bankAccount_salaryAndLeaves: bankAccountaddressinstance.city=city_bankAccount_salaryAndLeaves
            if state_bankAccount_salaryAndLeaves: bankAccountaddressinstance.state_division=state_bankAccount_salaryAndLeaves
            if zipCode_bankAccount_salaryAndLeaves: bankAccountaddressinstance.post_zip_code=zipCode_bankAccount_salaryAndLeaves
            if country_bankAccount_salaryAndLeaves: bankAccountaddressinstance.country=country_bankAccount_salaryAndLeaves
            bankAccountaddressinstance.save()

            bankAccountinstance = MODELS_CON.Bankaccount()
            if bankName_bankAccount_salaryAndLeaves: bankAccountinstance.bank_name=bankName_bankAccount_salaryAndLeaves
            if branch_bankAccount_salaryAndLeaves: bankAccountinstance.branch_name=branch_bankAccount_salaryAndLeaves
            if accountType_bankAccount_salaryAndLeaves: bankAccountinstance.account_type=accountType_bankAccount_salaryAndLeaves
            if accountingNo_bankAccount_salaryAndLeaves: bankAccountinstance.account_no=accountingNo_bankAccount_salaryAndLeaves
            if routingNo_bankAccount_salaryAndLeaves: bankAccountinstance.routing_no=routingNo_bankAccount_salaryAndLeaves
            if swiftBIC_bankAccount_salaryAndLeaves: bankAccountinstance.swift_bic=swiftBIC_bankAccount_salaryAndLeaves
            if bankAccountaddressinstance: bankAccountinstance.address=bankAccountaddressinstance
            bankAccountinstance.save()

            joiningDate_officialDetails = officialDetails.get('joiningDate')
            employeeId_officialDetails = officialDetails.get('employeeId')
            officialEmail_officialDetails = officialDetails.get('officialEmail')
            officialPhone_officialDetails = officialDetails.get('officialPhone')
            employeeType_officialDetails = officialDetails.get('employeeType')
            photo_uploadDocuments = uploadDocuments.request.FILES.get('photo')

            expenseApprover_officialDetails = officialDetails.get('expenseApprover')
            try: expenseApprover_officialDetails = MODELS_U.User.objects.get(id=expenseApprover_officialDetails)
            except: expenseApprover_officialDetails = None

            leaveApprover_officialDetails = officialDetails.get('leaveApprover')
            try: leaveApprover_officialDetails = MODELS_U.User.objects.get(id=leaveApprover_officialDetails)
            except: leaveApprover_officialDetails = None

            shiftApprover_officialDetails = officialDetails.get('shiftApprover')
            try: shiftApprover_officialDetails = MODELS_U.User.objects.get(id=shiftApprover_officialDetails)
            except: shiftApprover_officialDetails = None


            userinstance = MODELS_U.User()
            userinstance.username=employeeId_officialDetails
            if firstName_personalDetails: userinstance.first_name=firstName_personalDetails
            if lastName_personalDetails: userinstance.last_name=lastName_personalDetails
            if email_personalDetails: userinstance.email=email_personalDetails
            if designation_officialDetails: userinstance.designation=designation_officialDetails
            if grade_academicRecord: userinstance.grade=grade_academicRecord
            if shift_officialDetails: userinstance.shift=shift_officialDetails
            if dob_personalDetails: userinstance.dob=dob_personalDetails #########
            if bloodGroup_personalDetails: userinstance.blood_group=bloodGroup_personalDetails
            if fathersName_personalDetails: userinstance.fathers_name=fathersName_personalDetails
            if mothersName_personalDetails: userinstance.mothers_name=mothersName_personalDetails
            if maritalStatus_personalDetails: userinstance.marital_status=maritalStatus_personalDetails
            if gender_personalDetails: userinstance.gender=gender_personalDetails
            if spouseName_personalDetails: userinstance.spouse_name=spouseName_personalDetails
            if presentaddressinstance: userinstance.present_address=presentaddressinstance
            if permanentaddressinstance: userinstance.permanent_address=permanentaddressinstance
            if religion_personalDetails: userinstance.religion=religion_personalDetails
            if nationality_personalDetails: userinstance.nationality=nationality_personalDetails
            if contactNo_personalDetails: userinstance.personal_phone=contactNo_personalDetails
            if nidPassport_personalDetails: userinstance.nid_passport_no=nidPassport_personalDetails
            if tinNo_personalDetails: userinstance.tin_no=tinNo_personalDetails
            if joiningDate_officialDetails: userinstance.joining_date=joiningDate_officialDetails #########
            if employeeId_officialDetails: userinstance.official_id=employeeId_officialDetails
            if officialEmail_officialDetails: userinstance.official_email=officialEmail_officialDetails
            if officialPhone_officialDetails: userinstance.official_phone=officialPhone_officialDetails
            if employeeType_officialDetails: userinstance.employee_type=employeeType_officialDetails
            if photo_uploadDocuments: userinstance.photo=photo_uploadDocuments
            if expenseApprover_officialDetails: userinstance.expense_approver=expenseApprover_officialDetails
            if leaveApprover_officialDetails: userinstance.leave_approver=leaveApprover_officialDetails
            if shiftApprover_officialDetails: userinstance.shift_request_approver=shiftApprover_officialDetails




        else: 'employee id is already exist!'
    else: 'employee id is missing!'



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