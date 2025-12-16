from flask import render_template, redirect, url_for
from forms.admin_forms import CreateGroupForm
from models.database import Course, User, Group, db
from views.admin import AdminView


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