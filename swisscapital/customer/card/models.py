from customer.database_config import db
from datetime import datetime
from datetime import datetime,timezone


userfeature = db.Table('userfeature',
    db.Column('User_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('HumanFeature_id', db.String, db.ForeignKey('human_feature.id'), primary_key=True)
)

class User(db.Model):
  _searchable_=['first_name','last_name','personal_no','card_no']
  id = db.Column(db.Integer(), primary_key=True,nullable = False)
  first_name = db.Column(db.String(80),unique = False, nullable=False)
  last_name = db.Column(db.String(80),unique = False, nullable=False)
  cit = db.Column(db.String(80),nullable=False) #მოქალაქე
  gender = db.Column(db.String(10),nullable=False)
  personal_no = db.Column(db.String(15),unique=True,nullable=False)
  birth_of_date = db.Column(db.DateTime,nullable = False)
  date_of_exspiry = db.Column(db.DateTime,nullable = False)
  card_no = db.Column(db.String(10),nullable=False,unique = True)
  signature = db.Column(db.String(180) ,unique = True,nullable = False)
  place_of_birth = db.Column(db.String(200) ,unique = False,nullable=False)
  date_of_issue = db.Column(db.DateTime,nullable = False)
  issuing_autority = db.Column(db.String(100) ,unique = False,nullable = False)
  profile=db.Column(db.String(180) ,unique = True,nullable =False)
  date_crated=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
  # one to one
  department_id = db.Column(db.Integer, db.ForeignKey('department.id'),nullable=False)
  department = db.relationship('Department', backref=db.backref('User', lazy=True ))
  # many to many
  feature = db.relationship("HumanFeature",secondary=userfeature,backref=db.backref('features', lazy='dynamic'))

  def __repr__(self):
      return f'User {self.first_name} with Personal No: {self.personal_no}'


class HumanFeature(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    feature = db.Column(db.String(50),nullable=False,unique = True)
    description = db.Column(db.String(200),nullable=False)
   
    
    def __repr__(self):
      return self.feature


class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    department = db.Column(db.String(50),nullable=False,unique = True)
    description = db.Column(db.String(200),nullable=False)

    def __repr__(self):
      return self.department


