from flask import Blueprint ,render_template,flash,redirect,url_for
from flask_login import login_user,login_required,logout_user
from jobplus.forms import LoginForm,RegisterForm
from jobplus.models import db,User


front = Blueprint('front',__name__,url_prefix='/')
@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_admin:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                return redirect(url_for('admin.index',user_id=user.id))
            elif user.is_company:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                return redirect(url_for('company.profile',user_id=user.id))
            else:
                login_user(user,form.remember_me.data)
                flash('登陆成功,欢迎您的到来','success')
                return redirect(url_for('user.user_profile',user_id=user.id))
        return render_template('404.html'),404
    return render_template('login.html',form = form)



@front.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html',form=form)




@front.errorhandler(404)
def page_no_found(e):
    return render_template('404.html'),404
