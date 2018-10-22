from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,IntegerField,TextAreaField
from wtforms import FileField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError,Required
from wtforms.validators import URL
from jobplus.models import User,Job,db,Company
from flask import flash

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(3,24,message='用户名长度必须大于3小于24位数')])
    email = StringField('电子邮箱',validators=[DataRequired(),Email(message='email格式错误')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24,message='密码长度必须大于6位小于24位')])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password',message='重复密码必须与上一个密码相同')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return user


class LoginForm(FlaskForm):
    email = StringField('电子邮箱',validators=[DataRequired(),Email(message='Email格式错误')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24,message='密码长度需大于6位小于24位')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('用户名未注册')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')



class UserProfileForm(FlaskForm):
    name = StringField('真实姓名',validators=[DataRequired(),Length(1,15,message='姓名长度需要小于15且不能为空')])
    username = StringField('用户名',validators=[DataRequired(),Length(3,24,message='用户名长度必须大于3小于24位数')])
    email = StringField('电子邮箱',validators=[DataRequired(),Email(message='email格式错误')])
    password = PasswordField('密码')
    phonenumber = StringField('手机号',validators=[Length(11,12,message='请输入11位长度手机号码')])
    work_experience = IntegerField('工作年限')
    upload_resume_url = StringField('个人简历URL地址')
     
    submit = SubmitField('提交')

    def __init__(self,id,**kw):
        super(UserProfileForm,self).__init__(**kw)
        self.id=id

    def validate_username(self,field):
        if User.query.filter(User.username == field.data,User.id != self.id).first():
            raise ValidationError('您修改的用户名称已存在')

    def validate_email(self,field):
        if User.query.filter(User.email == field.data,User.id != self.id).first():
            raise ValidationError('您修改的邮箱已注册')
   
    def validate_password(self,field):
        if field.data != ''and (len(str(field.data)) < 3 or len(str(field.data)) >24) :
            raise ValidationError('您修改的密码长度必须在3到23位之间')


    def Profile_update(self,user):
        user.name = self.name.data
        user.email = self.email.data
        user.username = self.username.data
        user.phonenumber = self.phonenumber.data
        user.work_experience = self.work_experience.data
        user.upload_resume_url = self.upload_resume_url.data

        if self.password.data:
            user.password = self.password.data

        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('数据提交失败','success')
        return user

class CompanyProfileForm(FlaskForm):
    username = StringField('公司名称',validators=[DataRequired(),Length(2,54,message='公司名称长度必须大于2小于54位数')])
    email = StringField('注册电子邮箱',validators=[DataRequired(),Email(message='email格式错误')])
    password = PasswordField('密码')
    c_email = StringField('公司电子邮箱联系方式',validators=[DataRequired(),Email(message='email格式错误')])
    phone = StringField('公司电话联系方式')
    url = StringField('公司网站',validators=[DataRequired(),Length(0,64)])
    logo = StringField('Logo')    
    location = StringField('公司地址',validators=[Length(0,64)])
    financing = StringField('福利待遇')
    field = StringField('公司团队')
    about = TextAreaField('公司详情',validators=[DataRequired(),Length(0,1024)])
    submit = SubmitField('提交')

    def __init__(self,id,**kw):
        super(CompanyProfileForm,self).__init__(**kw)
        self.id=id

    def validate_username(self,field):
        if User.query.filter(User.username == field.data,User.id != self.id).first():
            raise ValidationError('您修改的公司名称已存在')

    def validate_email(self,field):
        if User.query.filter(User.email == field.data,User.id != self.id).first():
            raise ValidationError('您修改的邮箱已注册')

    def validate_password(self,field):
        if field.data != ''and (len(str(field.data)) < 3 or len(str(field.data)) >24) :
            raise ValidationError('您修改的密码长度必须在3到23位之间')

    """公司资料数据更新"""
    def Company_update(self,user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:#密码判断，如果修改了，则保存新密码
            user.password = self.password.data
        if user.company:#判断用户在公司数据库中是否存在
            tmp = user.company#如果存在，获取公司数据表对象
        else:
            tmp = Company()#如果不存在，新建公司数据表对象
            tmp.user_id = user.id#公司数据表外链到用户表id中

        self.populate_obj(tmp)#提交表单数据赋值到公司表中


        db.session.add(user)
        db.session.add(tmp)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('数据提交失败','success')
        return user

#管理员增加用户资料
class AddUserForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2,20,message='用户名长度错误')])
    name = StringField('真实姓名',validators=[DataRequired(),Length(1,15,message='姓名长度需要小于15且不能为空')])
    email = StringField('邮箱', validators=[Required(),Email()])
    phonenumber = StringField('手机号码', validators=[Required(), Length(11,11)])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')


    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        try:
            db.session.commit()
            flash('求职者添加成功','success')
        except:
            db.session.rollback()
            flash('用户创建失败','info')
        return user


#管理员增加公司资料
class AddCompanyForm(FlaskForm):
    name = StringField('公司名称', validators=[Required(), Length(2,40,message='公司名称长度必须在2到40个字符之间')])
    email = StringField('注册邮箱', validators=[Required(), Email(message='请输入合法的邮箱')])
    password = PasswordField('密码', validators=[Required(), Length(6,24,message='请输入6到24位字符密码')])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password',message='重复密码不一致')])
    url = StringField('企业网站', validators=[Required(), URL(message='请输入合法的网址')])
    about = TextAreaField('公司详情',validators=[DataRequired(),Length(0,1024)])

    submit = SubmitField('完成')

    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('公司名称已经存在')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')

    def create_company(self):
        user = User(
            username=self.name.data,
            email=self.email.data,
            password=self.password.data,
            role=20
        )
        company = Company(
                       c_email=self.email.data,
                       url=self.url.data,
                       about=self.about.data,
                       user=user,
                       )
        db.session.add(user)
        db.session.add(company)
        
        try:
            db.session.commit()
            flash('公司数据添加成功','success')
        except:
            db.session.rollback()
            flash('公司信息创建失败','info')
        return user, company


#管理员增加和修改职位资料
class AddJobForm(FlaskForm):
    jobname = StringField('职位名称')
    lowest_salary = IntegerField('最低薪酬')
    highest_salary = IntegerField('最高薪酬')
    experience_requirement = StringField('经验要求')
    description = StringField('职位描述')
    degree_requirement = StringField('职位学历要求')
    company_id = IntegerField('职位所属公司id')
    submit = SubmitField('提交')

    def validate_company_id(self, field):
        if not Company.query.filter_by(id=field.data).first():
            raise ValidationError('所属公司id不存在，请核对后重新输入')


    def create_job(self):
        job = Job()
        self.populate_obj(job)
        db.session.add(job)
        try:
            db.session.commit()
            flash('职位添加成功','success')
        except:
            db.session.rollback()
            flash('职位信息创建失败','info')
        return job

    def update_job(self,job):
        self.populate_obj(job)
        db.session.add(job)
        try:
            db.session.commit()
            flash('职位添加成功','success')
        except:
            db.session.rollback()
            flash('职位信息更新失败','info')
        return job

