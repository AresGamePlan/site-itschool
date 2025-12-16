from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from localization.base import language
from models.database import Course, Group, User, db, Schedule, Order, Student
from forms.admin_forms import CreateCourseForm, CreateGroupForm, UserFilterForm, EditUserForm, CreateScheduleForm, TransactionForm, ChangePasswordForm
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(func):
    def out_func(*args, **kwargs):
        if not current_user.is_admin():
            return redirect(url_for("main.index"))

        return func(*args, **kwargs)
    return out_func

class AdminView(MethodView):
    decorators = [login_required, language, admin_required]

#Работает
#Работает 2

class AdminDashboardView(AdminView):

    def get(self, **kwargs):
        return render_template("admin/index.html", data = kwargs)

class AdminGroupListView(AdminView):

    def get(self, **kwargs):
        group_list = Group.query.all()
        kwargs["group_list"] = group_list

        return render_template("admin/groupList.html", data = kwargs)

class AdminCreateGroupView(AdminView):

    def get(self, **kwargs):
        form = CreateGroupForm()

        form.course.choices = [(c.id, c.name) for c in Course.query.all()]
        form.teacher.choices = [(t.id, t.fullname) for t in User.query.filter_by(role="teacher").all()]

        return render_template("admin/createGroup.html", form=form, data = kwargs)
    
    def post(self, **kwargs):
        form = CreateGroupForm()

        form.course.choices = [(c.id, c.name) for c in Course.query.all()]
        form.teacher.choices = [(t.id, t.fullname) for t in User.query.filter_by(role="teacher").all()]

        if form.validate_on_submit():
            id_course = form.course.data
            id_teacher = form.teacher.data
            name = form.name.data
            new_group = Group(name=name, course_id = id_course, teacher_id = id_teacher)
            db.session.add(new_group)
            db.session.commit()

            return redirect(url_for("admin.groupList"))


class AdminCourseListView(AdminView):

    def get(self, **kwargs):
        course_list = Course.query.all()
        kwargs["course_list"] = course_list

        return render_template("admin/courseList.html", data = kwargs)
    
class AdminCreateCourseView(AdminView):

    def get(self, **kwargs):
        form = CreateCourseForm()
        
        return render_template("admin/createCourse.html", form = form, data = kwargs)
    
    def post(self, **kwargs):
        name = request.form.get("name")

        new_course = Course(name = name)
        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for("admin.courseList"))

class AdminCreateScheduleView(AdminView):

    def get(self, **kwargs):
        form = CreateScheduleForm()
        group_id = request.args.get("group_id")
        group = Group.query.get(group_id)

        kwargs["group"] = group

        return render_template("admin/createSchedule.html", data = kwargs, form = form)
    
    def post(self, **kwargs):
        form = CreateScheduleForm()

        print("Form data:", request.form)
        print("Form validate:", form.validate_on_submit())
        print(form.errors)

        if form.validate_on_submit():
            group_id = form.group_id.data
            group = Group.query.get(group_id)
            print(group.schedule)
            teacher_id = group.teacher_id
            time_start = form.time_start.data
            time_finish = form.time_finish.data
            days = [
                form.monday.data,
                form.tuesday.data,
                form.wednesday.data,
                form.thursday.data,
                form.friday.data,
                form.saturday.data,
                form.sunday.data
            ]

            schedule = Schedule.query.filter_by(group_id=group_id).first()

            if schedule:
                schedule.time_start = time_start
                schedule.time_finish = time_finish
                schedule.monday = days[0]
                schedule.tuesday = days[1]
                schedule.wednesday = days[2]
                schedule.thursday = days[3]
                schedule.friday = days[4]
                schedule.saturday = days[5]
                schedule.sunday = days[6]
            else:
                schedule = Schedule(
                    group_id=group_id,
                    time_start=time_start,
                    time_finish=time_finish,
                    monday=days[0],
                    tuesday=days[1],
                    wednesday=days[2],
                    thursday=days[3],
                    friday=days[4],
                    saturday=days[5],
                    sunday=days[6]
                )
                db.session.add(schedule)
            db.session.commit()

            return redirect(url_for("admin.groupList"))


class AdminUserListView(AdminView):

    def get(self, **kwargs):
        form = UserFilterForm(request.args)

        query = User.query

        if form.name.data:
            query = query.filter(User.username.ilike(f"%{form.name.data}%"))

        if form.role.data:
            query = query.filter(User.role == form.role.data)

        users = query.all()
        kwargs["user_list"] = users

        return render_template("admin/userList.html", data = kwargs, form = form)

class AdminChangeUserDataView(AdminView):

    def get(self, **kwargs):
        form_filter = UserFilterForm(request.args)

        query = User.query

        if form_filter.name.data:
            query = query.filter(User.username.ilike(f"%{form_filter.name.data}%"))

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
    
class AdminScheduleGroupView(AdminView):

    def get(self, **kwargs):
        group_id = request.args.get("group_id")
        group = Group.query.get(group_id)
        schedule = group.schedule
        if schedule == None:
            text_cell = "Нет расписания"
            kwargs["text_cell"] = text_cell
            kwargs["schedule"] = [True]
            kwargs["group_name"] = group.name
            return render_template("admin/scheduleGroup.html", data = kwargs)

        text_cell = group.name
        text_cell += "\n" + schedule.time_start.strftime("%H:%M")
        text_cell += "\n" + schedule.time_finish.strftime("%H:%M")

        kwargs["text_cell"] = text_cell
        kwargs["schedule"] = [schedule.monday, schedule.tuesday,schedule.wednesday,schedule.thursday,schedule.friday,schedule.saturday,schedule.sunday]
        kwargs["group_name"] = group.name

        return render_template("admin/scheduleGroup.html", data = kwargs)

class AdminQrCodeScanerView(AdminView):

    def get(self, **kwargs):

        return render_template("admin/qrScaner.html", data = kwargs)
    
    def post(self, **kwargs):

        qr_data = request.json.get("qr_data")

        qr_data = int(qr_data)

        redirect_url = url_for("admin.transaction", qr=qr_data)  # пример

        return jsonify({
            "success": True,
            "message": "QR-код успешно считан",
            "redirect_url": redirect_url
        })

class AdminTransactionView(AdminView):

    def get(self, **kwargs):
        form = TransactionForm()
        user = User.query.get(request.args.get("qr"))

        kwargs["user"] = user

        return render_template("admin/transaction.html", data = kwargs, form = form)
    
    def post(self, **kwargs):

        form = TransactionForm(request.form)
        user = User.query.get(form.user_id.data)

        if user.coins - form.count_coins.data < 0:
            return redirect(url_for("admin.noCoins"))

        transaction = Order(user_id = form.user_id.data, count = form.count_coins.data)

        db.session.add(transaction)
        user.coins -= form.count_coins.data
        db.session.commit()

        return redirect(url_for("admin.succes"))

class AdminScheduleView(AdminView): # Для Рамазана

    def get(self, **kwargs):
        schedules = Schedule.query.all()
        schedules_groups = []

        for s in schedules:
            schedules_strings = ["","","","","","","", ""]
            if s.monday:
                schedules_strings[0] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.tuesday:
                schedules_strings[1] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.wednesday:
                schedules_strings[2] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.thursday:
                schedules_strings[3] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.friday:
                schedules_strings[4] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.saturday:
                schedules_strings[5] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")
            if s.sunday:
                schedules_strings[6] += s.time_start.strftime("%H:%M") + "-" + s.time_finish.strftime("%H:%M")

            schedules_strings[7] = s.group.name
            schedules_groups.append(schedules_strings)
            

        kwargs["schedule"] = schedules_groups
        
        return render_template("admin/schedule.html", data = kwargs)
    
class AdminStudentListView(AdminView): # Для Ильи

    def get(self, **kwargs):
        students = Student.query.all()
        kwargs["students"] = students

        return render_template("admin/studentList.html", data = kwargs)
    
class AdminNoCoinsView(AdminView):

    def get(self, **kwargs):

        return render_template("admin/noCoins.html", data = kwargs)

class AdminSuccesView(AdminView):

    def get(self, **kwargs):

        return render_template("admin/succes.html", data = kwargs)
    
class AdminChangePasswordView(MethodView):
    decorators = [login_required, admin_required, language]

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

# Изменения

# Регистрация маршрута
admin_bp.add_url_rule("/", view_func=AdminDashboardView.as_view("index"))
admin_bp.add_url_rule("/groupList", view_func=AdminGroupListView.as_view("groupList"))
admin_bp.add_url_rule("/createGroup", view_func=AdminCreateGroupView.as_view("createGroup"))
admin_bp.add_url_rule("/courseList", view_func=AdminCourseListView.as_view("courseList"))
admin_bp.add_url_rule("/createCourse", view_func=AdminCreateCourseView.as_view("createCourse"))
admin_bp.add_url_rule("/userList", view_func=AdminUserListView.as_view("userList"))

admin_bp.add_url_rule("/editUserList", view_func=AdminChangeUserDataView.as_view("editUserList"))
admin_bp.add_url_rule("/schedule", view_func=AdminScheduleView.as_view("schedule"))
admin_bp.add_url_rule("/studentList", view_func=AdminStudentListView.as_view("studentList"))

admin_bp.add_url_rule("/createSchedule", view_func=AdminCreateScheduleView.as_view("createSchedule"))
admin_bp.add_url_rule("/scheduleGroup", view_func=AdminScheduleGroupView.as_view("scheduleGroup"))

admin_bp.add_url_rule("/qrScaner", view_func=AdminQrCodeScanerView.as_view("qrScaner"))
admin_bp.add_url_rule("/transaction", view_func=AdminTransactionView.as_view("transaction"))

admin_bp.add_url_rule("/succes", view_func=AdminSuccesView.as_view("succes"))
admin_bp.add_url_rule("/noCoins", view_func=AdminNoCoinsView.as_view("noCoins"))

admin_bp.add_url_rule("/changePassword", view_func=AdminChangePasswordView.as_view("changePassword"))