from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from localization.base import language
from models.database import Schedule, Group, User, db, Student, Payroll
from forms.teacher_forms import AddStudemtForm, AddCoinsForm

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

def teacher_required(func):
    def out_func(*args, **kwargs):
        if not current_user.is_teacher():
            return redirect(url_for("main.index"))

        return func(*args, **kwargs)
    return out_func


class TeacherIndexView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):

        query = Group.query
        query = query.filter(Group.teacher_id == current_user.id)
        groups = query.all()

        kwargs["groups"] = groups

        return render_template("teacher/index.html", data = kwargs)

class TeacherAddStudentView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):
        form = AddStudemtForm()

        group_id = request.args.get("group_id")
        q = request.args.get("q", "").strip()

        if q:
            users = User.query.filter(
                User.fullname.ilike(f"%{q}%")
            ).all()
        else:
            users = User.query.all()

        kwargs["users"] = users
        kwargs["group_id"] = group_id
        kwargs["q"] = q

        return render_template(
            "teacher/addStudent.html",
            data=kwargs,
            form=form
        )
    
    def post(self, **kwargs):
        group_id  = request.form.get("group_id")
        user_id  = request.form.get("user_id")
        group = Group.query.get(group_id)
        user = User.query.get(user_id)

        if not user:
            return "Пользователь не найден"
        if not group:
            return "Группа не найдена"

        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            student = Student(user_id=user_id)
            db.session.add(student)

        if group in student.groups:
            return "Ученик уже состоит в этой группе"
        
        student.groups.append(group)
        db.session.commit()

        return redirect(url_for("teacher.studentList", group_id = group_id))

class TeacherExpelStudentView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):
        student_id = request.args.get("student_id")
        group_id = request.args.get("group_id")

        group = Group.query.get(group_id)
        student = Student.query.get(student_id)

        group.students.remove(student)
        db.session.commit()

        return redirect(url_for("teacher.studentList", group_id = group_id))
    
class TeacherStudentListView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):
        group_id  = request.args.get("group_id")
        group = Group.query.get(group_id )
        students = group.students
        kwargs["students"] = students
        kwargs["group_id"] = group_id

        return render_template("teacher/studentList.html", data = kwargs)

class TeacherAddCoinsView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):
        form = AddCoinsForm()
        student_id = request.args.get("student_id")
        group_id = request.args.get("group_id")
        student = Student.query.get(student_id)

        kwargs["student"] = student
        kwargs["group_id"] = group_id
        
        return render_template("teacher/addCoins.html", data = kwargs, form = form)
    
    def post(self, **kwargs):
        payroll_counts = [100,50,10,20,15,-10]

        payroll = []
        payroll.append(request.form.get("lesson"))
        payroll.append(request.form.get("hard_lesson"))
        payroll.append(request.form.get("help_other"))
        payroll.append(request.form.get("visit_all_lesson"))
        payroll.append(request.form.get("idea_for_school"))
        payroll.append(request.form.get("breach_on_lesson"))

        payroll_for_student = 0
        user_id = request.form.get("student_id")
        group_id = request.form.get("group_id")

        for p in range(len(payroll)):
            if payroll[p]:
                payroll_for_student += payroll_counts[p]
        
        user = User.query.get(user_id)
        user.coins += payroll_for_student
        pay_tran = Payroll(amount_coins = payroll_for_student, user_id = user_id, comment = request.form.get("comment"))
        db.session.add(pay_tran)
        db.session.commit()

        return redirect(url_for("teacher.studentList", group_id = group_id))

class TeacherScheduleView(MethodView):
    decorators = [login_required, teacher_required, language]

    def get(self, **kwargs):
        schedules = Schedule.query.filter(Group.teacher_id == current_user.id).all()
        for i in schedules:
            print(i.teacher_id)
        print("SCHEDULES:", schedules)
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
        return render_template("teacher/schedule.html", data = kwargs)

teacher_bp.add_url_rule("/", view_func=TeacherIndexView.as_view("index"))
teacher_bp.add_url_rule("/studentList", view_func=TeacherStudentListView.as_view("studentList"))
teacher_bp.add_url_rule("/addStudent", view_func=TeacherAddStudentView.as_view("addStudent"))
teacher_bp.add_url_rule("/addCoins", view_func=TeacherAddCoinsView.as_view("addCoins"))
teacher_bp.add_url_rule("/expalStudent", view_func=TeacherExpelStudentView.as_view("expalStudent"))
teacher_bp.add_url_rule("/schedule", view_func=TeacherScheduleView.as_view("schedule"))