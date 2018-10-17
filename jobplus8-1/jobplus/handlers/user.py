
from flask import Blueprint ,render_template,redirect,url_for,flash
from flask_login import login_user,login_required
from jobplus.models import db,User
from jobplus.forms import LoginForm,RegisterForm,UserProfileForm

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/')
def user_index():
    return render_template('user/index.html')


@user.route('/profile/<int:user_id>',methods=['GET','POST'])
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = UserProfileForm(obj=user,id=user.id)
    if form.validate_on_submit():
        form.Profile_update(user)
        flash('您的个人资料修改成功！','success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html',form=form,user=user)
  


