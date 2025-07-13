from models import db, Aturan
from flask import Flask
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    with open("aturan_seed.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for kategori, pelaku_dict in data.items():
        for pelaku, isi in pelaku_dict.items():
            aturan = Aturan(
                kategori=kategori,
                pelaku=pelaku,
                fakta=isi["fakta"],
                sanksi=isi["sanksi"]
            )
            db.session.add(aturan)

    db.session.commit()
    print("✅ Aturan berhasil dimasukkan ke database.")
