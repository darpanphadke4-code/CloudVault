
from flask import send_file
import io
from services.azure_blob import download_blob
from services.azure_blob import delete_file

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from models import db, File
from services.azure_blob import upload_file

files = Blueprint("files", __name__)


# ---------------- Upload ---------------- #

@files.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            flash("Please select a file.", "warning")
            return redirect(url_for("files.upload"))

        try:

            # Upload to Azure
            blob_info = upload_file(uploaded_file)

            # Save metadata in SQLite
            new_file = File(
                original_filename=uploaded_file.filename,
                blob_name=blob_info["blob_name"],
                content_type=blob_info["content_type"],
                uploaded_by=session["user_id"]
            )

            db.session.add(new_file)
            db.session.commit()

            flash("File uploaded successfully to Azure!", "success")

            return redirect(url_for("files.my_files"))

        except Exception as e:

            db.session.rollback()

            flash(f"Upload failed: {str(e)}", "danger")

            return redirect(url_for("files.upload"))

    return render_template("upload.html")

# ---------------- My Files ---------------- #

@files.route("/myfiles")
def my_files():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_files = File.query.filter_by(
        uploaded_by=session["user_id"]
    ).all()

    return render_template(
        "myfiles.html",
        files=user_files
    )


# ---------------- Download ---------------- #

@files.route("/download/<int:file_id>")
def download(file_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    file = File.query.filter_by(
        id=file_id,
        uploaded_by=session["user_id"]
    ).first_or_404()

    file_data = download_blob(file.blob_name)

    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=file.original_filename,
        mimetype=file.content_type
    )


# ---------------- Delete ---------------- #

@files.route("/delete/<int:file_id>")
def delete(file_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    file = File.query.filter_by(
        id=file_id,
        uploaded_by=session["user_id"]
    ).first_or_404()

    try:

        delete_file(file.blob_name)

        db.session.delete(file)

        db.session.commit()

        flash("File deleted successfully!", "success")

    except Exception as e:

        db.session.rollback()

        flash(f"Delete failed: {str(e)}", "danger")

    return redirect(url_for("files.my_files"))