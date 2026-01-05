import csv
from io import BytesIO
from datetime import datetime, date, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Task
from .app import db

routes = Blueprint("routes", __name__)

# ---------------- DASHBOARD + ADD TASK + SEARCH ----------------
@routes.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    # ADD TASK
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority")
        due_date_str = request.form.get("due_date")

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

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

    # FILTER & SEARCH
    status = request.args.get("status")
    search = request.args.get("search", "").strip()

    query = Task.query.filter_by(user_id=current_user.id)

    if status == "completed":
        query = query.filter_by(completed=True)
    elif status == "pending":
        query = query.filter_by(completed=False)

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%") |
            Task.description.ilike(f"%{search}%")
        )

    tasks = query.all()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        status=status,
        search=search
    )

# ---------------- DELETE TASK ----------------
@routes.route("/task/delete/<int:id>")
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("routes.dashboard"))

# ---------------- COMPLETE TASK ----------------
@routes.route("/task/complete/<int:id>")
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
    return redirect(url_for("routes.dashboard"))

# ---------------- EDIT TASK ----------------
@routes.route("/task/edit/<int:id>", methods=["POST"])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        return redirect(url_for("routes.dashboard"))

    task.title = request.form.get("title")
    task.description = request.form.get("description")
    task.priority = request.form.get("priority")

    due_date_str = request.form.get("due_date")
    task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None

    db.session.commit()
    return redirect(url_for("routes.dashboard"))

# ---------------- ANALYTICS ----------------
@routes.route("/analytics")
@login_required
def analytics():

    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    productivity_score = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    priority_data = (
        db.session.query(Task.priority, func.count(Task.id))
        .filter_by(user_id=current_user.id)
        .group_by(Task.priority)
        .all()
    )

    priorities = [p[0] for p in priority_data]
    priority_counts = [p[1] for p in priority_data]

    today = date.today()
    week_ago = today - timedelta(days=6)

    weekly_data = (
        db.session.query(Task.due_date, func.count(Task.id))
        .filter(
            Task.user_id == current_user.id,
            Task.due_date >= week_ago,
            Task.due_date <= today
        )
        .group_by(Task.due_date)
        .all()
    )

    week_dates = [str(w[0]) for w in weekly_data]
    week_counts = [w[1] for w in weekly_data]

    return render_template(
        "analytics.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        productivity_score=productivity_score,
        priorities=priorities,
        priority_counts=priority_counts,
        week_dates=week_dates,
        week_counts=week_counts
    )

# ---------------- EXPORT CSV ----------------
@routes.route("/export/csv")
@login_required
def export_csv():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    def generate():
        yield "Title,Priority,Due Date,Status\n"
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            yield f"{task.title},{task.priority},{task.due_date},{status}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks.csv"}
    )

# ---------------- EXPORT PDF ----------------
@routes.route("/export/pdf")
@login_required
def export_pdf():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    text = pdf.beginText(40, 800)

    text.setFont("Helvetica", 11)
    text.textLine("Task Analytics Report")
    text.textLine("----------------------")
    text.textLine("")

    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        text.textLine(f"{task.title} | {task.priority} | {task.due_date} | {status}")

    pdf.drawText(text)
    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return Response(
        buffer,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tasks.pdf"}
    )
