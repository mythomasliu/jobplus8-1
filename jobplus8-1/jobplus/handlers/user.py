<<<<<<< HEAD

from flask import Blueprint ,render_template,redirect,url_for,flash
from flask_login import login_user,login_required
from jobplus.models import db,User
from jobplus.forms import LoginForm,RegisterForm

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/')
def user_index():
    return render_template('user/index.html')


@user.route('/profile/<int:user_id>',methods=['GET','POST'])
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('user/profile.html',user=user)

=======
from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

user = Blueprint('user',__name__,url_prefix='/user')
@user.route('/')
def user_index():
    return render_template('user/index.html')
>>>>>>> 蓝图生成、注册、主页和对应模板修改
