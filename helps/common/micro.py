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
        