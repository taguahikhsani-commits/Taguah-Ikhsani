# Website Program Studi Pendidikan Teknik Informatika (PTI)

Website responsif berbasis **Python Flask, Jinja2, Bootstrap 5, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, dan Flask-WTF**. Termasuk halaman publik, CMS berita, autentikasi berbasis peran, serta formulir kontak.

> Konten visi/misi, alamat, email, data dosen, dan akademik pada halaman contoh harus diverifikasi dan diganti dengan informasi resmi institusi sebelum website dipublikasikan.

## Fitur
- Beranda, profil, akademik, dosen, daftar berita, detail berita, dan kontak.
- CMS artikel: tambah, edit, draft/publikasi; hapus hanya untuk admin.
- Login menggunakan password hash, perlindungan CSRF, dan role admin/editor.
- Kotak masuk pesan pengunjung.
- Model data user, artikel, kategori, program akademik, dosen, pengaturan situs, dan pesan kontak.
- SQLite untuk pengembangan; MySQL melalui DATABASE_URL.

## Menjalankan secara lokal
Disarankan Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
cp .env.example .env
python run.py
```
Buka http://127.0.0.1:5000. SQLite lokal `pti.db` digunakan secara default.

## Database MySQL
Buat database dan user khusus aplikasi, lalu isi `DATABASE_URL` melalui environment:

```text
mysql+pymysql://pti_user:KATA_SANDI@127.0.0.1:3306/pti_db?charset=utf8mb4
```
File `schema.sql` berisi rancangan skema MySQL. Untuk pengelolaan perubahan skema yang berkelanjutan, gunakan Flask-Migrate:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "initial schema"
flask --app run.py db upgrade
```
Perintah `db init` hanya sekali; simpan folder `migrations/` ke Git.

## Membuat akun admin pertama
Tidak ada password default yang disediakan. Siapkan database lalu jalankan:

```bash
flask --app run.py shell
```

Di shell Python:

```python
from app import db
from app.models import User
user = User(full_name="Administrator PTI", email="admin@domain-kampus.ac.id", role="admin")
user.set_password("GANTI_DENGAN_PASSWORD_KUAT")
db.session.add(user)
db.session.commit()
```
Gunakan email dan password kuat milik pengelola resmi. Login melalui `/masuk`, dashboard pada `/admin/`.

## Produksi
- Set `SECRET_KEY` acak yang kuat; jangan simpan rahasia di Git.
- Set `FLASK_DEBUG=0`, gunakan HTTPS dan WSGI server, bukan server development Flask.
- Contoh: `gunicorn -w 2 -b 0.0.0.0:8000 run:app`.
- Siapkan backup database dan unggahan, pemantauan, dan prosedur restore.
- Sebelum go-live, lengkapi kontak resmi, kebijakan privasi, SEO, dan seluruh konten institusi.

## Batasan awal
Fondasi CMS sudah tersedia, tetapi CRUD program akademik, dosen, kategori, pengaturan situs, upload gambar, reset password, audit log, dan rate limiting login perlu dilengkapi sesuai kebutuhan operasional. Lakukan audit keamanan dan pengujian di lingkungan target sebelum publikasi.
