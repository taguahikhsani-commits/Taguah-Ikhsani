-- Database website Program Studi Pendidikan Teknik Informatika (PTI)
-- MySQL 8.0+ | Charset utf8mb4
-- Jalankan di MySQL Workbench/phpMyAdmin sebagai user yang berwenang.

CREATE DATABASE IF NOT EXISTS pti_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pti_db;

CREATE TABLE IF NOT EXISTS user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(180) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'editor',
  is_active_account BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_user_email (email),
  CONSTRAINT chk_user_role CHECK (role IN ('admin', 'editor'))
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS category (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  slug VARCHAR(120) NOT NULL UNIQUE,
  INDEX ix_category_slug (slug)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS academic_program (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(180) NOT NULL,
  slug VARCHAR(200) NOT NULL UNIQUE,
  description TEXT NOT NULL,
  icon VARCHAR(80) NOT NULL DEFAULT 'bi-mortarboard',
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS lecturer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(160) NOT NULL,
  academic_title VARCHAR(100) NOT NULL DEFAULT '',
  expertise VARCHAR(220) NOT NULL DEFAULT '',
  email VARCHAR(180) NOT NULL DEFAULT '',
  photo VARCHAR(255) NULL,
  bio TEXT NULL,
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  INDEX ix_lecturer_name (full_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS article (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(220) NOT NULL,
  slug VARCHAR(240) NOT NULL UNIQUE,
  excerpt VARCHAR(500) NOT NULL DEFAULT '',
  body TEXT NOT NULL,
  cover_image VARCHAR(255) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  category_id INT NULL,
  author_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  published_at DATETIME NULL,
  INDEX ix_article_status (status),
  INDEX ix_article_published_at (published_at),
  CONSTRAINT chk_article_status CHECK (status IN ('draft', 'published')),
  CONSTRAINT fk_article_category FOREIGN KEY (category_id)
    REFERENCES category(id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_article_author FOREIGN KEY (author_id)
    REFERENCES user(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS site_setting (
  id INT AUTO_INCREMENT PRIMARY KEY,
  `key` VARCHAR(100) NOT NULL UNIQUE,
  value TEXT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contact_message (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(180) NOT NULL,
  subject VARCHAR(180) NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_contact_created_at (created_at),
  INDEX ix_contact_is_read (is_read)
) ENGINE=InnoDB;

-- Data awal kategori berita (aman dijalankan berulang kali).
INSERT IGNORE INTO category (name, slug) VALUES
  ('Pengumuman', 'pengumuman'),
  ('Kegiatan', 'kegiatan'),
  ('Prestasi', 'prestasi'),
  ('Akademik', 'akademik');

-- Pengaturan dasar. Ganti nilainya dengan data resmi kampus sebelum publikasi.
INSERT IGNORE INTO site_setting (`key`, value) VALUES
  ('site_name', 'Program Studi Pendidikan Teknik Informatika'),
  ('institution_name', 'Nama Institusi'),
  ('official_email', 'email-resmi@kampus.ac.id'),
  ('official_phone', ''),
  ('official_address', 'Alamat resmi institusi'),
  ('vision', 'Masukkan visi resmi program studi.'),
  ('mission', 'Masukkan misi resmi program studi.');

-- Jangan memasukkan password admin langsung ke SQL.
-- Buat akun admin melalui Flask shell agar password di-hash oleh Werkzeug.
