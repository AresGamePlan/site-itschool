from views.admin import AdminView
from models.database import Course, db
from forms.admin_forms import CreateCourseForm
from flask import render_template, request, redirect, url_for

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