<<<<<<< HEAD

from flask import Blueprint ,render_template,redirect,url_for
from flask_login import login_user,login_required
from jobplus.models import db,Company,User
#from jobplus.forms import LoginForm,RegisterForm

company = Blueprint('company',__name__,url_prefix='/company')


=======
from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

company = Blueprint('company',__name__,url_prefix='/company')
>>>>>>> 蓝图生成、注册、主页和对应模板修改
@company.route('/')
def company_index():
    return render_template('company/index.html')

<<<<<<< HEAD


@company.route('/admin/profile/<int:user_id>',methods=['GET','POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('company/profile.html',user=user)

=======
>>>>>>> 蓝图生成、注册、主页和对应模板修改
