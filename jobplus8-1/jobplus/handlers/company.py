from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

company = Blueprint('company',__name__,url_prefix='/company')
@company.route('/')
def company_index():
    return render_template('company/index.html')

