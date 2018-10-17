from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default= datetime.utcnow,onupdate = datetime.utcnow)


#多对多中间关系表
user_job =db.Table(
            'user_job',
            db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE')),
            db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete="CASCADE")))

class User(Base,UserMixin):
    __tablename__ = 'user'
    
    ROLE_EMPLOYEE = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index = True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_EMPLOYEE)
    _password = db.Column('password',db.String(256),nullable=False)
    phonenumber = db.Column(db.Text)
    work_experience = db.Column(db.SmallInteger)
    jobs = db.relationship('Job',secondary=user_job)
    upload_resume_url =db.Column(db.String(64))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role ==self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role==self.ROLE_COMPANY

# 用户与职位是多对多的关系
class Job(Base):
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    jobname = db.Column(db.String(32),unique=True,nullable=False)
    experience_requirement = db.Column(db.String(32))
    degree_requirement = db.Column(db.String(32))
    lowest_salary = db.Column(db.Integer,nullable=False)
    highest_salary = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String(24))
    education = db.Column(db.String(32),nullable=False)#受教育程度
    #职位标签，标签用逗号隔开
    job_label = db.Column(db.String(128),nullable=False)
    is_fulltime = db.Column(db.Boolean,default=True)
    is_open = db.Column(db.Boolean,default=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Job {}>'.format(self.name)


class Dilevery(Base):
    __tablename__ = 'delivery'
    #等待企业审核
    STATUS_WAITING = 1
    #被拒绝
    STATUS_REJECT=2
    #被接受，等待通知面试
    STATUS_ACCEPT =3

    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    status = db.Column(db.SmallInteger,default=STATUS_WAITING)
    #企业回应
    response = db.Column(db.String(256))


        

#公司与职员关系是一对多的关系
class Company(Base):
    __tablename__ = 'company'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(32),unique=True,nullable=False)
    #公司位置
    email = db.Column(db.String(24),nullable=False)
    describtion = db.Column(db.String(100)) #公司描述
    about = db.Column(db.String(1024))#公司详情
    tags = db.Column(db.String(128))#公司标签
    stack = db.Column(db.String(128))#技术栈标签
    location = db.Column(db.String(64),nullable=False)
    logo = db.Column(db.String(64),nullable=False)
    url = db.Column(db.String(32),nullable=False)
    field = db.Column(db.String(32),nullable=False)
    financing = db.Column(db.String(32),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL')) 
    user = db.relationship('User',uselist=False,backref=db.backref('company',uselist=False))
    def __repr__(self):
        return '<Company {}>'.format(self.name)

    
