from views.admin import AdminView
from forms.admin_forms import CreateScheduleForm
from flask import render_template, redirect, request, url_for
from models.database import db, Group, Schedule

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