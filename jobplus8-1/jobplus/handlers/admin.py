from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

admin = Blueprint('admin',__name__,url_prefix='/admin')
@admin.route('/')
def admin_index():
    return render_template('admin/index.html')
