from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hastane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class drUser(db.Model):
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

def export_user_to_json():
    with app.app_context():
        # Veritabanını ve tabloları oluştur
        db.create_all() 
        users = drUser.query.all()
        data = []
        for user in users:
            data.append(
            {
                'id':user.id,
                'dr_email':user.dr_email,
                'password':user.password,
                'dr_ad':user.dr_ad,
                'dr_soyad':user.dr_soyad,
                'dr_tc_kimlik_no':user.dr_tc_kimlik_no,
                'dr_cinsiyet':user.dr_cinsiyet,
                'dr_dogum_gunu': user.dr_dogum_gunu.strftime('%Y-%m-%d') if user.dr_dogum_gunu else None,
                'dr_uzmanlik_alani':user.dr_uzmanlik_alani,
                'dr_diploma_no':user.dr_diploma_no,
                'dr_telefon':user.dr_telefon,
                'dr_hastane_adi':user.dr_hastane_adi
            })

        json_path = os.path.join(os.path.dirname(__file__), 'drusers.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} kullanıcı başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_user_to_json()

