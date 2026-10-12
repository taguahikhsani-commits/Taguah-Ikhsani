from datetime import datetime, timezone
import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Article, User, ContactMessage, AcademicProgram, Lecturer

admin_bp = Blueprint("admin", __name__)


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def make_slug(value):
    value = re.sub(r"[^a-zA-Z0-9\s-]", "", value.lower()).strip()
    return re.sub(r"[-\s]+", "-", value)[:230] or "artikel"


@admin_bp.get("/")
@roles_required("admin", "editor")
def dashboard():
    return render_template(
        "admin/dashboard.html",
        article_count=Article.query.count(),
        published_count=Article.query.filter_by(status="published").count(),
        message_count=ContactMessage.query.count(),
        lecturer_count=Lecturer.query.count(),
        recent_articles=Article.query.order_by(Article.updated_at.desc()).limit(5).all(),
    )


@admin_bp.get("/berita")
@roles_required("admin", "editor")
def articles():
    return render_template("admin/articles.html", articles=Article.query.order_by(Article.updated_at.desc()).all())


@admin_bp.route("/berita/tambah", methods=["GET", "POST"])
@roles_required("admin", "editor")
def article_create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        status = request.form.get("status", "draft")
        excerpt = request.form.get("excerpt", "").strip()
        if not title or not body:
            flash("Judul dan isi berita wajib diisi.", "danger")
        elif status not in {"draft", "published"}:
            flash("Status artikel tidak valid.", "danger")
        else:
            base = make_slug(title)
            slug = base
            suffix = 2
            while Article.query.filter_by(slug=slug).first():
                slug = f"{base}-{suffix}"
                suffix += 1
            article = Article(
                title=title, slug=slug, body=body, excerpt=excerpt,
                status=status, author_id=current_user.id,
                published_at=datetime.now(timezone.utc) if status == "published" else None,
            )
            db.session.add(article)
            db.session.commit()
            flash("Berita berhasil disimpan.", "success")
            return redirect(url_for("admin.articles"))
    return render_template("admin/article_form.html", article=None)


@admin_bp.route("/berita/<int:article_id>/edit", methods=["GET", "POST"])
@roles_required("admin", "editor")
def article_edit(article_id):
    article = db.get_or_404(Article, article_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        status = request.form.get("status", "draft")
        if not title or not body or status not in {"draft", "published"}:
            flash("Judul, isi, atau status tidak valid.", "danger")
        else:
            article.title = title
            article.excerpt = request.form.get("excerpt", "").strip()
            article.body = body
            article.status = status
            if status == "published" and article.published_at is None:
                article.published_at = datetime.now(timezone.utc)
            db.session.commit()
            flash("Perubahan berita disimpan.", "success")
            return redirect(url_for("admin.articles"))
    return render_template("admin/article_form.html", article=article)


@admin_bp.post("/berita/<int:article_id>/hapus")
@roles_required("admin")
def article_delete(article_id):
    article = db.get_or_404(Article, article_id)
    db.session.delete(article)
    db.session.commit()
    flash("Berita berhasil dihapus.", "success")
    return redirect(url_for("admin.articles"))


@admin_bp.get("/pesan")
@roles_required("admin", "editor")
def messages():
    return render_template("admin/messages.html", messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())


@admin_bp.post("/pesan/<int:message_id>/baca")
@roles_required("admin", "editor")
def message_read(message_id):
    message = db.get_or_404(ContactMessage, message_id)
    message.is_read = True
    db.session.commit()
    flash("Pesan ditandai telah dibaca.", "success")
    return redirect(url_for("admin.messages"))


@admin_bp.app_errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403
