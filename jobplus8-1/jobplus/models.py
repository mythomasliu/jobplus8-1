# -*- coding: utf-8 -*-

from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    """设置一个专用于创建时间和更新时间的基类，避免重复劳动"""
    # abstract表示不要吧这个类作为数据库表类
    __abstract__ = True
    # 两个时间数据表项的基类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default= datetime.utcnow,onupdate = datetime.utcnow)


""" 多对多中间关系表，用于职位的投递功能，用户和职位之间的id可以互相交叉联系"""

user_job =db.Table(
            'user_job',
            db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE')),
            db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete="CASCADE"))
            )

"""用户表包括三个角色"""
class User(Base,UserMixin):

    __tablename__ = 'user'

    USER = 10
    COMPANY = 20
    ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)#默认id，自增
    name = db.Column(db.String(32))#用户真实姓名，修改资料时使用
    username = db.Column(db.String(32),unique=True,index = True,nullable=False)#用户名
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)#邮箱
    role = db.Column(db.SmallInteger,default=USER)#权限，默认为用户
    _password = db.Column('password',db.String(256),nullable=False)#密码
    phonenumber = db.Column(db.Text)#手机号
    work_experience = db.Column(db.SmallInteger)#工作年限时长  
    upload_resume_url =db.Column(db.String(64))#个人简历url
    is_disable = db.Column(db.Boolean,default=False)#用户是是否禁用标示
    companys = db.relationship('Company',uselist=False)#公司的链接关系口
    jobs = db.relationship('Job',secondary=user_job)#工作的链接关系口
    
    def __repr__(self):#调试打印
        return '<User:{}>'.format(self.username)

    @property#对外密码
    def password(self):
        return self._password

    @password.setter#加密存储
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):#登录校对密码
        return check_password_hash(self._password,password)

    @property#判断是否管理员权限
    def is_admin(self):
        return self.role ==self.ADMIN

    @property#判断是否公司权限
    def is_company(self):
        return self.role==self.COMPANY

    @property#判断是否为用户
    def is_user(self):
        return self.role==self.USER


# 职位与公司是多对一的关系
class Job(Base):

    __tablename__ = 'job'

    id = db.Column(db.Integer,primary_key=True,nullable=False)#id自增
    jobname = db.Column(db.String(32),unique=True,nullable=False)#工作名称，岗位名称
    description = db.Column(db.String(128))#职位描述
    experience_requirement = db.Column(db.String(32))#工作能力和经验要求
    degree_requirement = db.Column(db.String(32))#学历要求
    lowest_salary = db.Column(db.Integer)#最低薪酬
    highest_salary = db.Column(db.Integer)#最高薪酬
    location = db.Column(db.String(24))#工作地点
    education = db.Column(db.String(32))#受教育程度
    job_label = db.Column(db.String(128))#职位标签，标签用逗号隔开
    is_fulltime = db.Column(db.Boolean,default=True)#是否全职、兼职等
    is_open = db.Column(db.Boolean,default=True)#职位是否开放或者关闭状态

    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('Company',uselist=False,backref=db.backref('job',lazy='dynamic'))

    

    def __repr__(self):
        return '<Job {}>'.format(self.name)



#用于记录用户求职者投递建立到职位的状态信息
class Dilevery(Base):

    __tablename__ = 'delivery'

    #等待企业审核
    STATUS_WAITING = 1
    #被拒绝
    STATUS_REJECT=2
    #被接受，等待通知面试
    STATUS_ACCEPT =3

    id = db.Column(db.Integer,primary_key=True)#id自增
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))#工作id，默认为空
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))#用户id，默认为空
    status = db.Column(db.SmallInteger,default=STATUS_WAITING)#投递状态，默认为等待企业审核
    
    response = db.Column(db.String(256))#企业回应数据


        

#公司与用户id是一对一的关系
class Company(Base):

    __tablename__ = 'company'

    id = db.Column(db.Integer,primary_key=True)


    url = db.Column(db.String(512),nullable=False)#公司网址
    logo = db.Column(db.String(512))#公司logo
    about = db.Column(db.String(1024),nullable=False)#公司详情
    #description = db.Column(db.String(24))#不知道有啥用
    location = db.Column(db.String(64))#公司地址

    phone = db.Column(db.Text)#公司电话
    c_email = db.Column(db.String(24),nullable=False)#公司邮箱

    tags = db.Column(db.String(128))#公司标签
    stack = db.Column(db.String(128))#公司技术站

    field = db.Column(db.String(32))#队伍建设
    financing = db.Column(db.String(32))#好处大大的

    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
 
    user = db.relationship('User',uselist=False,backref=db.backref('company',uselist=False))
    
    def __repr__(self):
        return '<Company {}>'.format(self.id)

    
