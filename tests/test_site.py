def test_public_pages_load(client):
    for path in ('/', '/profil', '/akademik', '/dosen', '/berita', '/kontak'):
        response = client.get(path)
        assert response.status_code == 200, path

def test_admin_requires_login(client):
    response = client.get('/admin/')
    assert response.status_code == 302
    assert '/masuk' in response.headers['Location']

def test_login_and_dashboard(client):
    response = client.post('/masuk', data={'email': 'admin@example.test', 'password': 'test-password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard Pengelola' in response.data

def test_wrong_password_rejected(client):
    response = client.post('/masuk', data={'email': 'admin@example.test', 'password': 'wrong'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'tidak valid' in response.data

def test_contact_form_saves_message(client, app):
    response = client.post('/kontak', data={'name':'Siti','email':'siti@example.test','subject':'Informasi','message':'Mohon informasi program studi.'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Pesan berhasil dikirim' in response.data
    from app.models import ContactMessage
    with app.app_context():
        assert ContactMessage.query.count() == 1
