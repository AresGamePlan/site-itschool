from views.admin import AdminView
from forms.admin_forms import TransactionForm
from flask import render_template, request, url_for, redirect, jsonify
from models.database import db, User, Order

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
    
class AdminNoCoinsView(AdminView):

    def get(self, **kwargs):

        return render_template("admin/noCoins.html", data = kwargs)

class AdminSuccesView(AdminView):

    def get(self, **kwargs):

        return render_template("admin/succes.html", data = kwargs)