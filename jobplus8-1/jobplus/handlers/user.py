from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

user = Blueprint('user',__name__,url_prefix='/user')
@user.route('/')
def user_index():
    return render_template('user/index.html')
