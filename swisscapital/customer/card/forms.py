from wtforms import Form,StringField, TextAreaField, SubmitField,validators,ValidationError,RadioField,IntegerField,SelectField
from flask_wtf.file import FileField,FileAllowed,FileField,FileRequired
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from .models import Department,User,HumanFeature
from wtforms.validators import DataRequired,Length,InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import date,datetime,timedelta
from wtforms_components import DateRange

class CardInfoForm(FlaskForm):
    first_name = StringField('First Name: ',validators=[DataRequired(),Length(min=3, max=50, message='Name length must be between %(min)d and %(max)d characters') ])
    last_name = StringField('Last Name: ',validators=[DataRequired(),Length(min=3, max=50, message='Last name length must be between %(min)d and %(max)d characters') ])
    cit = StringField('Cit: ',validators=[DataRequired(),Length(min=3, max=80, message='Cit name length must be between %(min)d and %(max)dcharacters') ])
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])  
    personal_no = StringField('Personal No: ',validators=[DataRequired(),Length(min=11, max=11, message='The person number mast be 11 characters') ] )
    birth_of_date = DateField('Birthdate: ', format='%Y-%m-%d',validators=[DateRange(min = date(1900, 1, 1),max = date.today(),message = 'imposible value try again! ')])
    # validators=(validators.Optional()))
    date_of_exspiry = DateField('Card Exspiry Date: ', format='%Y-%m-%d',validators=[DateRange(min=date.today(),max= date.today() + timedelta(10*365) , message = 'Imposible value try again!')])
    card_no = StringField('Card No: ',validators=[DataRequired(),Length(min=9, max=9, message='Card No length must be 9 characters') ])
    signature = FileField('Signature Image: ', validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please'),FileRequired()])
    place_of_birth = StringField('Pleace of birth: ',validators=[DataRequired(),Length(min=3, max=80, message='Name of location length must be between %(min)d and %(max)dcharacters') ])
    date_of_issue = DateField('Date of issue: ', format='%Y-%m-%d',validators=[DateRange(min = date.today() - timedelta(10*365) ,max=date.today(), message = 'Imposible value try again!')])
    issuing_autority = StringField('Inssuing autority: ', validators=[DataRequired(),Length(min=3, max=80, message='Name length must be between %(min)d and %(max)dcharacters') ])
    feature = StringField('Your features: ',validators=[DataRequired(),Length(min=1, max=100, message='Fearure name length must be between %(min)d and %(max)dcharacters') ])
    # department = QuerySelectField('Your department: ',query_factory=lambda: Department.query.all())
    profile =  FileField('Card image: ', validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please'),FileRequired()])
    submit=SubmitField('Register')

    # validate  Personal No
    def validate_personal_no(self,personal_no):
        if personal_no.data.isdigit() == False:
            raise ValidationError('Personal No must be number!')
        if User.query.filter_by(personal_no=personal_no.data).first():
            raise ValidationError('This Card ID alredy exist!')

    # validate exspiry date
    def validate_date_of_exspiry(self,date_of_exspiry):
        today = date.today()
        if self.date_of_issue.data is None:
            raise ValidationError('This ID Card data is incorrectly ')
        else:
            age = today.year - self.birth_of_date.data.year - ((today.month, today.day) <(self.birth_of_date.data.month, self.birth_of_date.data.day))
            range_of_ex = self.date_of_exspiry.data  - self.date_of_issue.data
            if age < 18 and range_of_ex != timedelta((4*365)+1):
                raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
            if range_of_ex % timedelta(2) == timedelta(0):
                if age >= 18 and range_of_ex != timedelta(((10 * 365)+2)):
                    print(range_of_ex,type(range_of_ex))
                    raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
            if range_of_ex % timedelta(2) != timedelta(0):
                if age >= 18 and range_of_ex != timedelta(((10 * 365)+3)):
                    print('two:',range_of_ex % timedelta(2) )
                    raise ValidationError('This Card ID is expired your or entered data is incorrectly ')


    # unique card no validation
    def validate_card_no(self,card_no):
        if card_no.data[2:3].isdigit()== True or card_no.data[3:4].isdigit() == True or (card_no.data[:2] + card_no.data[4:]).isdigit()==False:
            raise ValidationError('This Card ID not exist!')
        if User.query.filter_by(card_no = card_no.data).first():
            raise ValidationError('This Card ID already exist!')

    # validate issue date
    # if user is less 18 years old ISSUE DATE equals to 4 years and for adult 10 years old 
    def validate_date_of_issue(self, date_of_issue):
        today = date.today()
        if self.date_of_issue.data is None:
            raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
        else:
            age = today.year - self.birth_of_date.data.year - ((today.month, today.day) <(self.birth_of_date.data.month, self.birth_of_date.data.day))
            issue = today - self.date_of_issue.data
            if age < 18 and issue >= timedelta((4*365)+1):
                raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
            if age >= 18 and issue > timedelta(((10 * 365)+2)):
                raise ValidationError('This ID Card is expired or your entered data is incorrectly ')

     
class HumanFeatureform(FlaskForm):
    feature = StringField('Feature: ',[validators.DataRequired()])
    des = TextAreaField('Description',[validators.DataRequired()])
    submit=SubmitField('add feature')

    # feature validation 
    def validate_feature(self,feature):
        if HumanFeature.query.filter_by(feature=feature.data).first():
            raise ValidationError('This feature alredy exist!')


class DepartmentForm(FlaskForm):
    department = StringField('Department: ',[validators.DataRequired()])
    des = TextAreaField('Description',[validators.DataRequired()])
    submit=SubmitField('add department')

    #validation department
    def validate_department(self,department):
        if Department.query.filter_by(department=department.data).first():
            raise ValidationError('This department alredy exist!')

class UpdateInfoForm(FlaskForm):
    first_name = StringField('First Name: ',validators=[DataRequired(),Length(min=3, max=50, message='Name length must be between %(min)d and %(max)d characters') ])
    last_name = StringField('Last Name: ',validators=[DataRequired(),Length(min=3, max=50, message='Last name length must be between %(min)d and %(max)d characters') ])
    cit = StringField('Cit: ',validators=[DataRequired(),Length(min=3, max=80, message='Cit name length must be between %(min)d and %(max)dcharacters') ])
    gender = SelectField('Gender', choices = [('F','Female'),('M','Male')])  
    personal_no = StringField('Personal No: ',validators=[DataRequired(),Length(min=11, max=11, message='The person number mast be 11 characters') ] )
    birth_of_date = DateField('Birthdate: ', format='%Y-%m-%d',validators=[DateRange(min = date(1900, 1, 1),max = date.today(),message = 'imposible value try again! ')])
    # validators=(validators.Optional()))
    date_of_exspiry = DateField('Card Exspiry Date: ', format='%Y-%m-%d',validators=[DateRange(min=date.today(),max= date.today() + timedelta(10*365) , message = 'Imposible value try again!')])
    card_no = StringField('Card No: ',validators=[DataRequired(),Length(min=9, max=9, message='Card No length must be 9 characters') ])
    signature = FileField('Signature Image: ', validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please')])
    place_of_birth = StringField('Pleace of birth: ',validators=[DataRequired(),Length(min=3, max=80, message='Name of location length must be between %(min)d and %(max)dcharacters') ])
    date_of_issue = DateField('Date of issue: ', format='%Y-%m-%d',validators=[DateRange(min = date.today() - timedelta(10*365) ,max=date.today(), message = 'Imposible value try again!')])
    issuing_autority = StringField('Inssuing autority: ', validators=[DataRequired(),Length(min=3, max=80, message='Name length must be between %(min)d and %(max)dcharacters') ])
    feature = StringField('Your features: ',validators=[DataRequired(),Length(min=1, max=500, message='Fearure name length must be between %(min)d and %(max)dcharacters') ])
    # department = QuerySelectField('Your department: ',query_factory=lambda: Department.query.all())
    profile =  FileField('Card image: ', validators=[FileAllowed(['jpg','png','jpeg','gif'],'Image only please')])
    submit=SubmitField('Register')


    def validate_personal_no(self,personal_no):
        if personal_no.data.isdigit() == False:
            raise ValidationError('Personal No must be number!')

        # if User.query.filter_by(personal_no=personal_no.data).first():
        #     raise ValidationError('This Card ID alredy exist!')

        
    # validate Birthdate
    def validate_birth_date(self,birth_of_date):
        if self.birth_of_date.data is None:
            raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
        else:
            if birth_of_date.data.days > (120 * 365) and birth_of_date.data < datetime.date.today():
                raise ValidationError('Imposible value')

    # unique card no validation
    """ თუ Card_no ემთხვევა შეყვანილ Card_no და ასვე ამ Card_no გასწვრივ ემთხვევა მომხმარებლის მიერ შეყვანილ Personal_no """
    def validate_card_no(self,card_no):
        if card_no.data[2:3].isdigit()== True or card_no.data[3:4].isdigit() == True or (card_no.data[:2] + card_no.data[4:]).isdigit()==False:
            raise ValidationError('This Card ID type not exist!')

        #შესაძლებელია უნიკალური ბარათის ნომრის ვალიდაცია როცა მომხმარებელი ავტორიზებულია ამ ლოგიკით რადგანც ის უნიკალურია ბაზაში
        # card = User.query.filter_by(card_no = card_no.data).first()
        # if card != current_user.user.card_no:
        #     raise ValidationError('This Card ID already exist! 2')


               
    # validate issue date
    # if user is less 18 years old ISSUE DATE equals to 4 years and for adult 10 years old 
    def validate_date_of_issue(self, date_of_issue):
        today = date.today()
        if self.date_of_issue.data is None:
            raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
        else:
            age = today.year - self.birth_of_date.data.year - ((today.month, today.day) <(self.birth_of_date.data.month, self.birth_of_date.data.day))
            issue = today - self.date_of_issue.data
            if age < 18 and issue >= timedelta((4*365)+1):
                raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
            if age >= 18 and issue > timedelta(((10 * 365)+2)) or age >= 18 and issue > timedelta(((10 * 365)+3)):
                raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
    
    # validate exspiry date
    def validate_date_of_exspiry(self,date_of_exspiry):
        today = date.today()
        if self.date_of_issue.data is None:
            raise ValidationError('This ID Card data is incorrectly ')
        else:
            age = today.year - self.birth_of_date.data.year - ((today.month, today.day) <(self.birth_of_date.data.month, self.birth_of_date.data.day))
            range_of_ex = self.date_of_exspiry.data  - self.date_of_issue.data
            if age < 18 and range_of_ex != timedelta((4*365)+1):
                raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
            if range_of_ex % timedelta(2) == timedelta(0):
                if age >= 18 and range_of_ex != timedelta(((10 * 365)+2)):
                    print(range_of_ex,type(range_of_ex))
                    raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
            if range_of_ex % timedelta(2) != timedelta(0):
                if age >= 18 and range_of_ex != timedelta(((10 * 365)+3)):
                    print('two:',range_of_ex % timedelta(2) )
                    raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
