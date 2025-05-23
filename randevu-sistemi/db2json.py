from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hastane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tc_kimlik_no = db.Column(db.String(11), unique=True, nullable=False)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    cinsiyet = db.Column(db.String(10), nullable=False)
    dogum_tarihi = db.Column(db.Date, nullable=True)  # Nullable yapıldı
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(128), nullable=False)

def export_user_to_json():
    with app.app_context():
        # Veritabanını ve tabloları oluştur
        db.create_all()
        users = User.query.all()

        data = []
        for user in users:
            data.append({
                'id': user.id,
                'tc_kimlik_no': user.tc_kimlik_no,
                'ad': user.ad,
                'soyad': user.soyad,
                'cinsiyet': user.cinsiyet,
                'dogum_tarihi': user.dogum_tarihi.strftime('%Y-%m-%d') if user.dogum_tarihi else None,
                'email': user.email,
                'telefon': user.telefon,
                'password': generate_password_hash(user.password)  # Şifreyi hash'leyerek ekle
            })

        json_path = os.path.join(os.path.dirname(__file__), 'users.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} kullanıcı başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_user_to_json()
