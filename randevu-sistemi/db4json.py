from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hastane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Randevu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hasta_adi = db.Column(db.String(100), nullable=False)
    tc_no = db.Column(db.String(11), nullable=False)
    telefon = db.Column(db.String(11), nullable=False)
    doktor_bolumu = db.Column(db.String(100), nullable=False)
    randevu_tarihi = db.Column(db.Date, nullable=False)
    randevu_saati = db.Column(db.Time, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def export_user_to_json():
    with app.app_context():
        # Veritabanını ve tabloları oluştur
        db.create_all() 
        randevular = Randevu.query.all()  # Tüm randevuları al
        data = []
        for randevu in randevular:
            data.append(
                {
                    'id': randevu.id,  # Burada Randevu objesinin id alanını kullan
                    'hasta_adi': randevu.hasta_adi,
                    'tc_no': randevu.tc_no,
                    'telefon': randevu.telefon,
                    'doktor_bolumu': randevu.doktor_bolumu,
                    'randevu_tarihi': randevu.randevu_tarihi.strftime('%Y-%m-%d') if randevu.randevu_tarihi else None,
                    'randevu_saati': randevu.randevu_saati.strftime('%H:%M') if randevu.randevu_saati else None,
                    'kullanici_id': randevu.kullanici_id
                }
            )

        json_path = os.path.join(os.path.dirname(__file__), 'randevular.json')  # Dosya adı 'randevular.json' olarak değiştirildi
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Toplam {len(data)} randevu başarıyla {json_path} dosyasına kaydedildi.")

if __name__ == '__main__':
    export_user_to_json()
