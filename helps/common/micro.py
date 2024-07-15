from rest_framework import status

from helps.common.nano import Nanohelps
import datetime
import re

class Microhelps(Nanohelps):

    
    def addtocolass(self, classOBJ=None, Serializer=None, data=None, allowed_fields='__all__', unique_fields=[], required_fields=[], extra_fields={}, choice_fields=[], fields_regex=[]): # New
        response_data = None
        response_message = []
        response_data = {}
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        if classOBJ:
            if Serializer:
                if data:
                    preparedata = {}
                    self.filterAllowedFields(allowed_fields, data, preparedata)
                    self.filterUniqueFields(classOBJ, unique_fields, preparedata, response_message)
                    preparedata.update(extra_fields)
                    self.filterChoiceFields(choice_fields, preparedata, response_message)
                    self.filterRequiredFields(required_fields, preparedata, response_message)
                    self.filterRegexFields(fields_regex, preparedata, response_message)

                    if not response_message:
                        serializer = Serializer(data=preparedata, many=False)
                        if serializer.is_valid():
                            try:    
                                serializer.save()
                                response_data = serializer
                                response_successflag = 'success'
                                response_status = status.HTTP_201_CREATED
                            except:
                                print(serializer)
                                response_message.append('unique combination is already exist!')
                        else:
                            print(serializer.errors)
                            response_message.append('something went wrong!')
                else: response_message.append('please provide data!')
            else: response_message.append('provide serializer!')
        else: response_message.append('please provide a Model!')
        return response_data, response_message, response_successflag, response_status
    
    def updaterecord(self, classOBJ=None, Serializer=None, id=None, data={}, allowed_fields='__all__', unique_fields=[], freez_update=[], continue_update=[], extra_fields={}, choice_fields=[], fields_regex=[], static_fields=[]): # New
        response_data = {}
        response_message = []
        response_successflag = 'error'
        response_status = status.HTTP_400_BAD_REQUEST
        if classOBJ:
            if Serializer:
                if id:
                    if data:
                        classobj = classOBJ.objects.filter(id=id)
                        if classobj.exists():
                            preparedata = {}
                            self.filterAllowedFields(allowed_fields, data, preparedata)
                            self.filterUniqueFields(classOBJ, unique_fields, preparedata, response_message, recordid=classobj.first().id)
                            if extra_fields: preparedata.update(extra_fields)
                            self.filterFreezFields(classobj, freez_update, response_message)
                            self.filterContinueFields(classobj, continue_update, response_message)
                            self.filterChoiceFields(choice_fields, preparedata, response_message)
                            self.filterRegexFields(fields_regex, preparedata, response_message)
                            if not response_message:
                                serializer = Serializer(instance=classobj.first(), data=preparedata, partial=True)
                                if serializer.is_valid():
                                    try:
                                        for static_field in static_fields:
                                            self.removeFile(classobj.first(), static_field)
                                        serializer.save()

                                        response_data = serializer.data
                                        response_successflag = 'success'
                                        response_status = status.HTTP_200_OK
                                    except: response_message.append('unique combination is already exist!')
                                else:
                                    print(serializer.errors)
                                    response_message.append('Something Went wrong!')
                        else: response_message.append('doesn\'t exist!')
                    else: response_message.append('please provide data!')
                else: response_message.append('please provide an id!')
            else: response_message.append('provide serializer!')
        else: response_message.append('please provide a Model!')
        return response_data, response_message, response_successflag, response_status
    
    def deleterecord(self, classOBJ=None, id=None, classOBJpackage_tocheck_assciaativity=[], freez_delete=[], continue_delete=[]): # New
        response_data = {}
        response_message = []
        response_successflag = 'error'
        response_status = status.HTTP_409_CONFLICT
        
        if classOBJ:
            if id:
                classobj = classOBJ.objects.filter(id=id)
                if classobj.exists():
                    for classOBJpackage in classOBJpackage_tocheck_assciaativity:
                        for field in classOBJpackage['fields']:
                            if field['relation'] == 'onetoonefield':
                                if classOBJpackage['model'].objects.filter(**{field['field']: classobj.first()}).exists():
                                    response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                            if field['relation'] == 'foreignkey':
                                if classOBJpackage['model'].objects.filter(**{field['field']: classobj.first()}).exists():
                                    response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                            if field['relation'] == 'manytomanyfield':
                                if field['records']: response_message.append(f"can\'t delete, associated to {classOBJpackage['model'].__name__} class and exist record!")
                    
                    self.filterFreezFields(classobj, freez_delete, response_message)
                    self.filterContinueFields(classobj, continue_delete, response_message)
                    if not response_message:
                        try:
                            classobj.delete()
                            response_successflag = 'success'
                            response_status = status.HTTP_202_ACCEPTED
                        except: response_message.append('something went wrong!')
                else: response_message.append('doesn\'t exist!')
            else: response_message.append('please provide an id!')
        else: response_message.append('please provide a Model!')
       
        return response_data, response_message, response_successflag, response_status

    def addbankaccount(self, classOBJpackage, serializerOBJpackage, data, createdInstance=None): # New
        response = {'flag': True, 'message': [], 'instance': {}}
        if isinstance(data.get('address'), dict):
            address_required_fields = ['address', 'city', 'state_division', 'country']
            address_response_data, address_response_message, address_response_successflag, address_response_status = self.addtocolass(
                classOBJ=classOBJpackage['Address'],
                Serializer=serializerOBJpackage['Address'],
                data=data['address'],
                required_fields=address_required_fields
            )
            if address_response_successflag == 'success':
                data.update({'address': address_response_data.instance.id})
                createdInstance.append(address_response_data.instance)
            elif response_successflag == 'error':
                response['flag'] = False
                response['message'].extend([f'bank account address\'s {each}' for each in address_response_message])
        
        if response['flag']:
            required_fields = ['bank_name', 'branch_name', 'account_type', 'account_no', 'routing_no']
            response_data, response_message, response_successflag, response_status = self.addtocolass(
                classOBJ=classOBJpackage['Bankaccount'],
                Serializer=serializerOBJpackage['Bankaccount'],
                data=data,
                required_fields=required_fields
            )
            if response_successflag == 'success':
                response['instance'] = response_data.instance
                createdInstance.append(response_data.instance)
        return response