from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError
from jobplus.models import User,Job,db,Company


class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(3,24,message='用户名长度必须大于3小于24位数')])
    email = StringField('电子邮箱',validators=[DataRequired(),Email(message='email格式错误')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24,message='密码长度必须大于6位小于24位')])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
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
    


class RegisterForm_Company(FlaskForm):
    username = StringField('公司名称',validators=[DataRequired(),Length(3,24,message='用户名长度必须大于3小于24位数')])
    email = StringField('电子邮箱',validators=[DataRequired(),Email(message='email格式错误')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24,message='密码长度必须大于6位小于24位')])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('公司名称已存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def create_company(self):
        user = User()
        self.populate_obj(user)
        user.role = 20

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

