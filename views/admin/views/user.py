from views.admin import AdminView
from forms.admin_forms import UserFilterForm, EditUserForm, ChangePasswordForm
from flask import request, render_template, url_for, redirect
from werkzeug.security import generate_password_hash
from models.database import db, User, Student

class AdminUserListView(AdminView):

    def get(self, **kwargs):
        form = UserFilterForm(request.args)

        query = User.query

        if form.name.data:
            query = query.filter(User.fullname.ilike(f"%{form.name.data}%"))

        if form.role.data:
            query = query.filter(User.role == form.role.data)

        users = query.all()
        kwargs["user_list"] = users

        return render_template("admin/userList.html", data = kwargs, form = form)
    
class AdminUserDeleteView(AdminView):
    def get(self, **kwargs):
        user_id = request.args.get("user_id")
        user = User.query.get(user_id)
        if not user:
            return redirect(url_for("admin.userList"))
        
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("admin.userList"))

class AdminChangeUserDataView(AdminView):

    def get(self, **kwargs):
        form_filter = UserFilterForm(request.args)

        query = User.query

        if form_filter.name.data:
            query = query.filter(User.fullname.ilike(f"%{form_filter.name.data}%"))

        if form_filter.role.data:
            query = query.filter(User.role == form_filter.role.data)

        users = query.all()
        kwargs["user_list"] = users

        users_forms = []

        for user in users:
            form = EditUserForm()
            form.id.data = user.id
            form.name.data = user.fullname
            form.role.data = user.role

            users_forms.append(form)

        kwargs["user_forms"] = users_forms
        
        return render_template("admin/editUserList.html", data = kwargs, form_filter = form_filter)
    
    def post(self, **kwargs):
        id = request.form.get("id")
        new_name = request.form.get("name")
        new_role = request.form.get("role")
        print(id)
        print(new_role)

        user = User.query.get(id)
        if user.fullname != new_name:
            user.fullname = new_name

        user.role = new_role
        db.session.commit()

        return redirect(url_for("admin.editUserList"))
    
class AdminChangePasswordView(AdminView):

    def get(self, **kwargs):
        form = ChangePasswordForm()

        user_id = request.args.get("user_id")
        user = User.query.get(user_id)

        if not user:
            return redirect(url_for("admin.userList"))

        kwargs["user"] = user
        return render_template("admin/changePassword.html", data=kwargs, form=form)

    def post(self, **kwargs):
        form = ChangePasswordForm(request.form)
        user_id = form.user_id.data
        new_password = form.new_password.data

        user = User.query.get(user_id)
        if not user:
            return redirect(url_for("admin.userList"))

        # Хешируем пароль
        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()

        return redirect(url_for("admin.userList"))

class AdminStudentListView(AdminView): # Для Ильи

    def get(self, **kwargs):
        students = Student.query.all()
        kwargs["students"] = students

        return render_template("admin/studentList.html", data = kwargs)