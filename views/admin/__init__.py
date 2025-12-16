from flask import Blueprint, url_for, redirect
from flask.views import MethodView
from localization.base import language
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(func):
    def out_func(*args, **kwargs):
        if not current_user.is_admin():
            return redirect(url_for("main.index"))

        return func(*args, **kwargs)
    return out_func

class AdminView(MethodView):
    decorators = [login_required, language, admin_required]

# Index
from .views.index import AdminDashboardView    

admin_bp.add_url_rule("/", view_func=AdminDashboardView.as_view("index"))

# Для групп
from .views.group import AdminCreateGroupView, AdminGroupListView

admin_bp.add_url_rule("/groupList", view_func=AdminGroupListView.as_view("groupList"))
admin_bp.add_url_rule("/createGroup", view_func=AdminCreateGroupView.as_view("createGroup"))

# Для курсов
from .views.course import AdminCourseListView, AdminCreateCourseView

admin_bp.add_url_rule("/courseList", view_func=AdminCourseListView.as_view("courseList"))
admin_bp.add_url_rule("/createCourse", view_func=AdminCreateCourseView.as_view("createCourse"))

# Для расписания
from .views.schedule import AdminScheduleGroupView, AdminCreateScheduleView, AdminScheduleView

admin_bp.add_url_rule("/createSchedule", view_func=AdminCreateScheduleView.as_view("createSchedule"))
admin_bp.add_url_rule("/schedule", view_func=AdminScheduleView.as_view("schedule"))
admin_bp.add_url_rule("/scheduleGroup", view_func=AdminScheduleGroupView.as_view("scheduleGroup"))

# Для пользователей
from .views.user import AdminChangeUserDataView, AdminUserListView, AdminChangePasswordView, AdminStudentListView

admin_bp.add_url_rule("/editUserList", view_func=AdminChangeUserDataView.as_view("editUserList"))
admin_bp.add_url_rule("/userList", view_func=AdminUserListView.as_view("userList"))
admin_bp.add_url_rule("/changePassword", view_func=AdminChangePasswordView.as_view("changePassword"))
admin_bp.add_url_rule("/studentList", view_func=AdminStudentListView.as_view("studentList"))

# Для коинов и системы списания
from .views.coin import AdminNoCoinsView, AdminQrCodeScanerView, AdminSuccesView, AdminTransactionView

admin_bp.add_url_rule("/qrScaner", view_func=AdminQrCodeScanerView.as_view("qrScaner"))
admin_bp.add_url_rule("/transaction", view_func=AdminTransactionView.as_view("transaction"))
admin_bp.add_url_rule("/succes", view_func=AdminSuccesView.as_view("succes"))
admin_bp.add_url_rule("/noCoins", view_func=AdminNoCoinsView.as_view("noCoins"))