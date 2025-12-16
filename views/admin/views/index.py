from views.admin import AdminView
from flask import render_template

class AdminDashboardView(AdminView):

    def get(self, **kwargs):
        return render_template("admin/index.html", data = kwargs)