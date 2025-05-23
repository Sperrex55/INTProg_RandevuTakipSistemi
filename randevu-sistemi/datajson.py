from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

# Flask uygulamanızı başlatın
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hastane.db'  # Veritabanı bağlantı dizesi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Veritabanı modellerinizi tanımlayın
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tc_kimlik_no = db.Column(db.String(11), unique=True, nullable=False)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    cinsiyet = db.Column(db.String(10), nullable=False)
    dogum_tarihi = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(128), nullable=False)

class drUser (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dr_tc_kimlik_no = db.Column(db.String(11), unique=True, nullable=False)
    dr_ad = db.Column(db.String(50), nullable=False)
    dr_soyad = db.Column(db.String(50), nullable=False)
    dr_cinsiyet = db.Column(db.String(10), nullable=False)
    dr_dogum_gunu = db.Column(db.Date, nullable=False)
    dr_email = db.Column(db.String(120), unique=True, nullable=False)
    dr_uzmanlik_alani = db.Column(db.String(100), nullable=False)
    dr_diploma_no = db.Column(db.String(25), nullable=False)
    dr_telefon = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    dr_hastane_adi = db.Column(db.String(100), nullable=False)

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hasta_adi = db.Column(db.String(100), nullable=False)
    tc_no = db.Column(db.String(11), nullable=False)
    telefon = db.Column(db.String(11), nullable=False)
    doktor_bolumu = db.Column(db.String(100), nullable=False)
    randevu_tarihi = db.Column(db.Date, nullable=False)
    randevu_saati = db.Column(db.Time, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    durum = db.Column(db.String(20), default="Beklemede")

def export_to_json():
    with app.app_context():  # Uygulama bağlamını oluştur
        data = {
            "users": [],
            "doctors": [],
            "appointments": []
        }

        # Kullanıcıları ekle
        for user in User.query.all():
            data["users"].append({
                "id": user.id,
                "tc_kimlik_no": user.tc_kimlik_no,
                "ad": user.ad,
                "soyad": user.soyad,
                "cinsiyet": user.cinsiyet,
                "dogum_tarihi": user.dogum_tarihi.strftime('%Y-%m-%d'),
                "email": user.email,
                "telefon": user.telefon,
                "password": user.password  # Şifreyi hash'li olarak ekleyin
            })

        # Doktorları ekle
        for doctor in drUser .query.all():
            data["doctors"].append({
                "id": doctor.id,
                "dr_tc_kimlik_no": doctor.dr_tc_kimlik_no,
                "dr_ad": doctor.dr_ad,
                "dr_soyad": doctor.dr_soyad,
                "dr_cinsiyet": doctor.dr_cinsiyet,
                "dr_dogum_gunu": doctor.dr_dogum_gunu.strftime('%Y-%m-%d'),
                "dr_email": doctor.dr_email,
                "dr_uzmanlik_alani": doctor.dr_uzmanlik_alani,
                "dr_diploma_no": doctor.dr_diploma_no,
                "dr_telefon": doctor.dr_telefon,
                "dr_hastane_adi": doctor.dr_hastane_adi
            })

        # Randevuları ekle
        for appointment in Randevu.query.all():
            data["appointments"].append({
                "id": appointment.id,
                "hasta_adi": appointment.hasta_adi,
                "tc_no": appointment.tc_no,
                "telefon": appointment.telefon,
                "doktor_bolumu": appointment.doktor_bolumu,
                "randevu_tarihi": appointment.randevu_tarihi.strftime('%Y-%m-%d'),
                "randevu_saati": appointment.randevu_saati.strftime('%H:%M'),
                "kullanici_id": appointment.kullanici_id,
                "durum": appointment.durum
            })

        # JSON dosyasını yaz
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    export_to_json()
