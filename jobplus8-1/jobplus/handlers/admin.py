from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required, company_required
from jobplus.models import User, Company, Job, db
from jobplus.forms import RegisterForm, AddUserForm, AddCompanyForm,CompanyProfileForm
from jobplus.forms import AddJobForm
from jobplus.forms import UserProfileForm

admin = Blueprint('admin',__name__,url_prefix='/admin')


#管理员登录后自动进入后台管理主页
@admin.route('/')
@admin_required
def index():
    return render_template('admin/admin_base.html')


#打开用户列表
@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/user_show.html',pagination=pagination)

#打开职位列表
@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/job_show.html',pagination=pagination)

#新增用户路由
@admin.route('/users/add_user',methods=['GET','POST'])
@admin_required
def user_add():
    form = AddUserForm()
    if form.validate_on_submit():
        form.create_user()
        return redirect(url_for('.users'))
    return render_template('admin/add_user.html', form=form)

#新增公司路由
@admin.route('/users/addcompany',methods=['GET','POST'])
@admin_required
def company_add():
    form = AddCompanyForm()
    if form.validate_on_submit():
        form.create_company()
        return redirect(url_for('.users'))
    return render_template('admin/add_company.html', form=form)

#新增职位路由
@admin.route('/job/addjob',methods=['GET','POST'])
@admin_required
def job_add():
    form = AddJobForm()
    if form.validate_on_submit():
        form.create_job()
        return redirect(url_for('.jobs'))
    return render_template('admin/add_job.html',form=form)

#编辑用户信息
@admin.route('/users/edituser/<int:user_id>',methods=['GET','POST'])
@admin_required
def edituser(user_id):
    user = User.query.get_or_404(user_id)
    form = UserProfileForm(obj=user,id=user.id)
    if form.validate_on_submit():
        form.Profile_update(user)
        flash('用户信息更新成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html',form=form,user=user)


#编辑公司信息
@admin.route('/users/editcompany/<int:company_id>',methods=['GET','POST'])
@admin_required
def editcompany(company_id):
    user = User.query.get_or_404(company_id)
    form = CompanyProfileForm(obj=user.company,
                              username=user.username,
                              email=user.email,
                              id=user.id)
    if form.validate_on_submit():
        form.Company_update(user)
        flash('企业更新成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_company.html',form=form,user=user)

#是否启用或禁用
@admin.route('/users/<int:user_id>/<action>')
@admin_required
def user_action(user_id,action):
    user = User.query.get_or_404(user_id)
    if str(action) == 'disable':
        user.is_disable=True
    if (action) == 'enable':
        user.is_disable=False
    db.session.add(user)
    try:
        db.session.commit()
        flash('用户操作成功','success')
    except:
        db.session.rollback()
        flash('用户操作失败')
    return redirect(url_for('admin.users'))

#职位上线或者下线
@admin.route('/jobs/<int:job_id>/<action>')
@admin_required
def job_action(job_id,action):
    job = Job.query.get_or_404(job_id)
    if str(action) == 'disable':
        job.is_open=False
    if str(action) == 'enable':
        job.is_open=True
    db.session.add(job)
    try:
        db.session.commit()
        flash('岗位操作成功','success')
    except:
        db.session.rollback()
        flash('岗位操作失败')
    return redirect(url_for('admin.users'))

