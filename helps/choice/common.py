DAYS = (('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'))
CALCULATION_TYPE = (('Percentage', 'Percentage'), ('Flat', 'Flat'))
MONTHS = (('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August','August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'))
MONTHS_D = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
MONTHS_DR = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}
STATUS = (('Pending','Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'))
ATTENDANCE_FROM = (('Device','Device'), ('Manual', 'Manual'), ('Remote', 'Remote'))
LEAVE_TYPE = (('Paid', 'Paid'), ('Non Paid', 'Non Paid'))
GENDER = (('Male', 'Male'), ('Female', 'Female'),)
AMOUNT_TYPE = (('Fixed Amount', 'Fixed Amount'), ('Percentage', 'Percentage'),)
LOAN_TYPE = (('Advance Salary', 'Advance Salary'), ('Loan', 'Loan'), ('Fine', 'Fine'),)
ADJUSTMENT_TYPE = (('From Salary', 'From Salary'), ('By Cash', 'By Cash'),)
ATTENDANCE_OVERTIME = (('Disabled', 'Disabled'), ('Overtime', 'Overtime'),)
PAYMENT_IN = (('Cash','Cash'), ('Cheque', 'Cheque'), ('Bank', 'Bank'))
INCREMENT_ON = (('Gross Salary','Gross Salary'), ('Basic Salary', 'Basic Salary'))
# JOBHISTORY_STATUS = (('Joining', 'Joining'), ('Increment', 'Increment'), ('Promotion', 'Promotion'))
STATUS_ADJUSTMENT = (('Joining', 'Joining'), ('Increment', 'Increment'), ('Promotion', 'Promotion'), ('Demotion', 'Demotion'), ('Transfer', 'Transfer'), ('Terminated', 'Terminated'))
JOB_STATUS = (
    ('OnGoing', 'OnGoing'),
    ('Resigned', 'Resigned'),
    ('Terminated', 'Terminated'),
    ('Retired', 'Retired'),
)
EMPLOYEE_TYPE = (
    ('Trainee', 'Trainee'),
    ('Apprentice', 'Apprentice'),
    ('Intern', 'Intern'),
    ('Probation', 'Probation'),
    ('Permanent', 'Permanent'),
    ('Temporary', 'Temporary'),
    ('Contractual', 'Contractual'),
    ('Comission', 'Comission'),
    ('Labour', 'Labour'),
)
MARITAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('Separated ', 'Separated')
)
BLOOD_GROUP = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('Golden Blood(Rh Null)', 'Golden Blood(Rh Null)'),
)
BANK_ACCOUNT_TYPE = (
    ('Current Account', 'Current Account'),
    ('Savings Account', 'Savings Account'),
    ('Salary Account', 'Salary Account'),
    ('Checking Account', 'Checking Account'),
    ('Business Account', 'Business Account'),
    ('Currency Account', 'Currency Account'),
    ('Interest Account', 'Interest Account'),
    ('Student Checking Account', 'Student Checking Account'),
    ('Basic Account', 'Basic Account'),
    ('Retirement Account', 'Retirement Account'),
    ('Fixed Deposit Account', 'Fixed Deposit Account')
)