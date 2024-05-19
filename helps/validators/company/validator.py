from django.core.exceptions import ValidationError


def validate_company_type_code(value):
    # 'CMPTP-00001'
    if len(value) == 11:
        if not (value[:6] == 'CMPTP-' and value[6:len(value)].isnumeric()):
            raise ValidationError('Follow the pattern CMPTP-01234')
    else:
        raise ValidationError('code must has to be 11 char long!')
    
def validate_bank_account_type_code(value):
    if len(value) == 9:
        if not (value[:4] == 'BAT-' and value[4:len(value)].isnumeric()):
            raise ValidationError('Follow the pattern BAT-01234')
    else:
        raise ValidationError('code must has to be 9 char long!')