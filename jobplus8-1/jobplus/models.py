
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime,utcnow)
    updated_at = db.Column(db.DateTime, default= datetime.utcnow,onupdate = datetime.utcnow)
class User(Base):
    __tablename__ = 'user'
    
    ROLE_EMPLOYEE = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index = True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_EMPLOYEE)
    _password = db.Column('password',db.String(256),nullable=False)
    phonenumber = db.Column(db.Integer,nullable=False)
    work_experience = db.Column(db.SamllInteger,nullable=False)
    job = db.relationship('Job')

class Job(Base):
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    jobname = db.Column(db.String(32),unique=True,nullable=False)
    release_time = db.Column(db.String(32))  #发布时间
    experience_required = db.Column(db.Integer,nullable=False)
    lowest_salary = db.Column(db.Integer,nullable=False)
    highest_salary = db.Column(db.Integer,nullable=False)
    education = db.Column(db.String(32),nullable=False)
    job_label = db.Column(db.String(64),nullable=False)
    job_description = db.Column(db.String(600))
    employee = db.relationship('User')
    employer = db.relationship('Company')

#公司与职员关系是一对多的关系
class Company(Base):
    __tablename__ = 'company'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(32),unique=True,nullable=False)
    label = db.Column(db.String(64),nullable=False)
    url = db.Column(db.String(32),nullable=False)
    field = db.Column(db.String(32),nullable=False)
    financing = db.Column(db.String(32),nullable=False)
    city = db.Column(db.String(32),nullable=False)
    
    
