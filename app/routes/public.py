from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Article, AcademicProgram, Lecturer, ContactMessage

public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def index():
    articles = Article.query.filter_by(status="published").order_by(Article.published_at.desc()).limit(3).all()
    programs = AcademicProgram.query.filter_by(is_published=True).order_by(AcademicProgram.sort_order).limit(3).all()
    return render_template("public/index.html", articles=articles, programs=programs)


@public_bp.get("/profil")
def profil():
    return render_template("public/profil.html")


@public_bp.get("/akademik")
def akademik():
    programs = AcademicProgram.query.filter_by(is_published=True).order_by(AcademicProgram.sort_order).all()
    return render_template("public/akademik.html", programs=programs)


@public_bp.get("/dosen")
def dosen():
    lecturers = Lecturer.query.filter_by(is_published=True).order_by(Lecturer.full_name).all()
    return render_template("public/dosen.html", lecturers=lecturers)


@public_bp.get("/berita")
def berita():
    page = request.args.get("page", 1, type=int)
    pagination = Article.query.filter_by(status="published").order_by(
        Article.published_at.desc()
    ).paginate(page=page, per_page=6, error_out=False)
    return render_template("public/berita.html", pagination=pagination)


@public_bp.get("/berita/<slug>")
def detail_berita(slug):
    article = Article.query.filter_by(slug=slug, status="published").first_or_404()
    return render_template("public/detail_berita.html", article=article)


@public_bp.route("/kontak", methods=["GET", "POST"])
def kontak():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        if not all((name, email, subject, message)) or len(message) > 5000:
            flash("Lengkapi seluruh kolom. Pesan maksimal 5.000 karakter.", "danger")
        else:
            db.session.add(ContactMessage(name=name, email=email, subject=subject, message=message))
            db.session.commit()
            flash("Pesan berhasil dikirim. Terima kasih telah menghubungi kami.", "success")
            return redirect(url_for("public.kontak"))
    return render_template("public/kontak.html")
