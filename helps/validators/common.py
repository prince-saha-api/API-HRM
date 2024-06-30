from django.core.exceptions import ValidationError
import re
 
def validate_phonenumber(value):
    result = re.findall('^01[3456789][0-9]{8}$|^8801[3456789][0-9]{8}$|^\+8801[3456789][0-9]{8}$', value)
    if not result: raise ValidationError('Please insert a valid BD number!')
 
def validate_phone_number(value):
    if len(value) == 14:
        if value[:5] == '+8801':
            if value[5:len(value)].isnumeric():
                if not (value[5] in ['3', '4', '5', '6', '7', '8', '9']):
                    raise ValidationError('Please insert a valid BD number!')
            else:
                raise ValidationError('Please insert a valid BD number!')
        else:
            raise ValidationError('Please insert a valid BD number!')
    elif len(value) == 13:
        if value[:4] == '8801':
            if value[4:len(value)].isnumeric():
                if not (value[4] in ['3', '4', '5', '6', '7', '8', '9']):
                    raise ValidationError('Please insert a valid BD number!')
            else:
                raise ValidationError('Please insert a valid BD number!')
        else:
            raise ValidationError('Please insert a valid BD number!')
    elif len(value) == 11:
        if value[:2] == '01':
            if value[2:len(value)].isnumeric():
                if not (value[2] in ['3', '4', '5', '6', '7', '8', '9']):
                    raise ValidationError('Please insert a valid BD number!')
            else:
                raise ValidationError('Please insert a valid BD number!')
        else:
            raise ValidationError('Please insert a valid BD number!')
    else:
        raise ValidationError('Please insert a valid BD number!')
    
def validate_office_id(value):
    if len(value) == 10:
        if value[:3] == 'API':
            if not value[3:len(value)].isnumeric(): raise ValidationError('Please insert a valid ID! Ex: API1234567')
        else: raise ValidationError('Please insert a valid ID! Ex: API1234567')
    else: raise ValidationError('Please insert a valid ID! Ex: API1234567')