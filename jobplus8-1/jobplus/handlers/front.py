from flask import Blueprint ,render_template,flash,redirect,url_for
from flask_login import login_user,login_required,logout_user
from jobplus.forms import LoginForm,RegisterForm
from jobplus.models import db,User,Company

front = Blueprint('front', __name__)
@front.route('/')
def index():
    return render_template('index.html')

#用户登录路由
@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_disable:
                flash('您的账号已被禁用，请联系客服！','info')
                return render_template('login.html',form = form)
            if user.is_admin:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                return redirect(url_for('admin.index'))
            elif user.is_company:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                if user.company:
                    return redirect(url_for('.index'))                    
                else:
                    return redirect(url_for('company.profile'))
            else:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                if user.name:
                    return redirect(url_for('.index'))
                else:
                    return redirect(url_for('user.user_profile'))
        return render_template('404.html'),404
    return render_template('login.html',form = form)


#用户注册路由

@front.route('/register',methods=['GET','POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登陆','success')
        return redirect(url_for('.login'))
    return render_template('register.html',form=form)

#公司注册路由
@front.route('/register_company',methods=['GET','POST'])
def company_register():
    form = RegisterForm()
    #form.username.label = '公司名称'
    if form.validate_on_submit():
        role_user = form.create_user()
        role_user.role = 20
        db.session.add(role_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        flash('注册成功，请登陆','success')
        return redirect(url_for('.login'))
    return render_template('register_company.html',form=form)



#用户注销路由
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经成功登出','success')
    return redirect(url_for('.index'))

#404路由信息
@front.errorhandler(404)
def page_no_found(e):
    return render_template('404.html'),404
