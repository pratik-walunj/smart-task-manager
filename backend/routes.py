from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

routes = Blueprint("routes", __name__)

@routes.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=current_user.username
    )
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from .app import db

routes = Blueprint("routes", __name__)

@routes.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        due_date_str = request.form.get("due_date")

        due_date = None
        if due_date_str:
           due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()


        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("routes.dashboard"))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)

@routes.route("/task/delete/<int:id>")
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("routes.dashboard"))


@routes.route("/task/complete/<int:id>")
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
    return redirect(url_for("routes.dashboard"))
