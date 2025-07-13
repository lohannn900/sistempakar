from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Aturan

# === Setup Aplikasi Flask ===
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'  # Ganti di production dengan environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# === Setup Login Manager ===
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# === Load User dari database ===
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Halaman Register ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Cek jika username sudah dipakai
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan. Silakan pilih yang lain.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun berhasil dibuat. Silakan login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# === Halaman Login ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Username atau password salah.')
    return render_template('login.html')

# === Logout ===
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Berhasil logout.')
    return redirect(url_for('login'))

# === Halaman Utama (Index) ===
@app.route('/')
@login_required
def index():
    aturan_dict = {}
    aturan_data = Aturan.query.all()
    for row in aturan_data:
        aturan_dict.setdefault(row.kategori, {})[row.pelaku] = {
            "fakta": row.fakta,
            "sanksi": row.sanksi
        }
    return render_template('index.html', aturan=aturan_dict)

# === Endpoint AJAX untuk cek aturan berdasarkan kategori dan pelaku ===
@app.route('/cek_aturan', methods=['POST'])
@login_required
def cek_aturan():
    data = request.get_json()
    kategori = data.get("kategori")
    pelaku = data.get("pelaku")

    aturan = Aturan.query.filter_by(kategori=kategori, pelaku=pelaku).first()
    if aturan:
        return jsonify(fakta=aturan.fakta, sanksi=aturan.sanksi)
    return jsonify(error="Aturan tidak ditemukan"), 404

# === Jalankan aplikasi Flask ===
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
