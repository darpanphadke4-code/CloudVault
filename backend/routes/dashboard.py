from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from models import File

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def dashboard_home():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Get all files uploaded by this user
    files = (
        File.query
        .filter_by(uploaded_by=user_id)
        .order_by(File.upload_date.desc())
        .all()
    )

    total_files = len(files)

    total_size = sum(file.file_size for file in files)

    # Convert bytes to a readable format
    if total_size < 1024:
        storage_used = f"{total_size} Bytes"
    elif total_size < 1024 * 1024:
        storage_used = f"{total_size / 1024:.2f} KB"
    elif total_size < 1024 * 1024 * 1024:
        storage_used = f"{total_size / (1024 * 1024):.2f} MB"
    else:
        storage_used = f"{total_size / (1024 * 1024 * 1024):.2f} GB"

    latest_file = files[0].original_filename if files else "No uploads yet"

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        total_files=total_files,
        storage_used=storage_used,
        latest_file=latest_file
    )