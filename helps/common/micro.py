from rest_framework import status

from helps.common.nano import Nanohelps
import datetime

class Microhelps(Nanohelps):
    
    def isWorkingDayAccordingToOfficeOffDay(self, Offday, year, month, date):
        result = True
        objects = Offday.objects.filter(active=True).values('day')
        if objects:
            offdays = [object['day'] for object in objects]
            day = datetime.date(year, month, date).strftime("%A")
            if day in offdays: result = False
        return result
    
    # def getApplicableHolidayDates(self, Holiday, customuser):
    #     holidaydates = []

    #     holidays = Holiday.objects.filter(active=True, priority=True)
    #     for holiday in holidays:
    #         if customuser.religion:
    #             religion = customuser.religion.name
    #             if holiday.only_aplicable_for.all():
    #                 if holiday.only_aplicable_for.filter(name=religion): holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
    #             else: holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
    #         else:
    #             if not holiday.only_aplicable_for.all(): holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
                
    #     return holidaydates
    def getApplicableHolidayDates(self, customuser):
        holidaydates = []

        # holidays = Holiday.objects.filter(active=True, priority=True)
        # for holiday in holidays:
        #     if customuser.religion:
        #         religion = customuser.religion.name
        #         if holiday.only_aplicable_for.all():
        #             if holiday.only_aplicable_for.filter(name=religion): holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
        #         else: holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
        #     else:
        #         if not holiday.only_aplicable_for.all(): holidaydates.append(self.convertDateformat_STR_y_m_d(holiday.date))
                
        return holidaydates
    
    def getGrossSalary(self, customuser, Salary):
        salary = None
        salaryinfo = Salary.objects.filter(custom_user__id=customuser.id).order_by('-id')
        if salaryinfo:
            salaryinfo = salaryinfo.first()
            if salaryinfo != None:
                if salaryinfo.gross_salary != None:
                    salary = salaryinfo.gross_salary
        return salary   
    
    def getOnePortionOfSalaryAccordingToConfig(self, salary, BonusConfig):
        bonusconfig = BonusConfig.objects.all()
        OnePortionOfSalary = None
        if bonusconfig:
            bonusconfig = bonusconfig.first()
            if bonusconfig.calculation_based_on:
                percentage = bonusconfig.calculation_based_on.percentage
                if isinstance(percentage, float):
                    OnePortionOfSalary = (percentage*salary)/100
        return OnePortionOfSalary
    
    def addtocolass(self, classOBJ, classSrializer, data, unique): # New
        unique_value = data.get(unique)
        response_data = {}
        response_message = ''
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        if unique_value:
            if not classOBJ.objects.filter(**{unique:unique_value}).exists():
                classsrializer = classSrializer(data=data, many=False)
                if classsrializer.is_valid():
                    classsrializer.save()
                    response_data = classsrializer.data
                    response_successflag = 'success'
                    response_status = status.HTTP_201_CREATED
            else: response_message = f'this {unique_value} already exist!'
        else: response_message = f'{unique_value} is required!'

        return response_data, response_message, response_successflag, response_status
    
    def addemergencycontact(self, Employeecontact, Address, userinstance, emergencyContact): # New
        for details in emergencyContact:
            name = details.get('name')
            age = details.get('age')
            phone_no = details.get('phone_no')
            email = details.get('email')
            relation = details.get('relation')
            addressinstance = self.addaddress(Address, details['address'])

            employeecontactinstance = Employeecontact()
            employeecontactinstance.user=userinstance
            if name: employeecontactinstance.name=name
            if age: employeecontactinstance.age=age
            if phone_no: employeecontactinstance.phone_no=phone_no
            if email: employeecontactinstance.email=email
            if relation: employeecontactinstance.relation=relation
            if addressinstance: employeecontactinstance.address=addressinstance
            employeecontactinstance.save()

    def addbankaccount(self, classOBJpackage, data): # New
        print(classOBJpackage)
        bank_name = data.get('bank_name')
        branch_name = data.get('branch_name')
        account_type = self.getobject(classOBJpackage['Bankaccounttype'], data.get('account_type'))
        account_no = data.get('account_no')
        routing_no = data.get('routing_no')
        swift_bic = data.get('swift_bic')
        address = self.addaddress(classOBJpackage['Address'], data.get('address'))

        bankaccountinstance = classOBJpackage['Bankaccount']()
        if bank_name: bankaccountinstance.bank_name=bank_name
        if branch_name: bankaccountinstance.branch_name=branch_name
        if account_type: bankaccountinstance.account_type=account_type
        if account_no: bankaccountinstance.account_no=account_no
        if routing_no: bankaccountinstance.routing_no=routing_no
        if swift_bic: bankaccountinstance.swift_bic=swift_bic
        if address: bankaccountinstance.address=address
        bankaccountinstance.save()
        return bankaccountinstance