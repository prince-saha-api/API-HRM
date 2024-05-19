from django.shortcuts import render
# from helps.decorators.decorator import CommonDecorator as deco
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from company.models import *
# from company.serializer.serializers import *
# from rest_framework.response import Response
# from rest_framework import status
# from customuser.models import CustomUser, Paymentrecord, Salary, SalaryAllocation, PerdaySalary, Bonus
# from costcalculation.models import Costtitle 
# from helps.choice.common import CALCULATION_TYPE
# from attendance.models import Attendance
# from officialoffday.models import Offday
# # from holidaymanagement.models import Holiday
# from hrm_settings.models import FixedWorkingdaysinamonth, Workingminutesperday, Latefineforfewdays
# from helps.common.generic import Generichelps as ghelp


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['Get Companies Details', 'all'])
# def getSalary(request, id, year, month):
#     if CustomUser.objects.filter(id=id).exists():
#         customuser = CustomUser.objects.get(id=id)
#         salaryinfo = Salary.objects.filter(custom_user__id=customuser.id).order_by('-id')
#         if salaryinfo:
#             salaryinfo = salaryinfo.first()
#             if salaryinfo != None:
#                 response = ghelp().generateOBJSalaryCalculation(salaryinfo)
#                 ghelp().partitionSalary(SalaryAllocation, response, salaryinfo)

#                 # if ghelp().calculateAttendanceCost(Attendance, Holiday, Offday, PerdaySalary, FixedWorkingdaysinamonth, Workingminutesperday, Latefineforfewdays, response, customuser, year, month, id):
#                 if ghelp().calculateAttendanceCost(Attendance, Offday, PerdaySalary, FixedWorkingdaysinamonth, Workingminutesperday, Latefineforfewdays, response, customuser, year, month, id):
#                     # # Calculate Leave Cost
#                     # ghelp().calculateLeaveCost(Leave, LeaveConfig, FixedWorkingdaysinamonth, salaryinfo, response, CALCULATION_TYPE, id)

#                     applicable_deduction = customuser.applicable_deduction
#                     if applicable_deduction:
#                         # Costtitle, Subcosttitle
#                         ghelp().calculateDynamicCost(Costtitle, applicable_deduction, response, salaryinfo)
                    
#                     # Calculate Bonus
#                     ghelp().calculateBonus(Bonus, id, response, year, month)

#                     flag = ghelp().storepaymentrecord(Paymentrecord, User, request.user.username, response, customuser, year, ghelp().convert_y_m_d_STR_month(year, month, 1))
#                     if flag: return Response({'message': response}, status=status.HTTP_200_OK)
#                     else: return Response({'message': 'This Employee has got his salary in this month already!'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'message': 'This employee\'s attendance record is empty!'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'message': 'salary hasn\'t set yet!'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'salary hasn\'t set yet!'}, status=status.HTTP_200_OK)
        
#     else:
#         return Response({'message': 'user couldn\'t find!'}, status=status.HTTP_404_NOT_FOUND)