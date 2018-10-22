from flask import Blueprint ,render_template

#from jobplus.forms import LoginForm,RegisterForm

job = Blueprint('job',__name__,url_prefix='/job')
@job.route('/')
def job_index():
    return render_template('job/index.html')
