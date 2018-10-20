

from flask import Blueprint ,render_template,redirect,url_for
from flask_login import login_user,login_required,current_user
from jobplus.models import db,Company,User
#from jobplus.forms import LoginForm,RegisterForm

company = Blueprint('company',__name__,url_prefix='/company')


@company.route('/')
def company_index():
    return render_template('company/index.html')




@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('company/profile.html',user=user)

