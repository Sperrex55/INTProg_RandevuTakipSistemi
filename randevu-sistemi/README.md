# 📌 Proje Başlığı

> Randevu Takip Sistemi

## 🧾 Proje Tanıtımı

Bu uygulama, vatandaşların kolay ve hızlı şekilde hastane randevusu almasını, doktorların kendi panelleri üzerinden randevuları takip ve yönetmesini sağlayan modern bir web tabanlı hastane randevu sistemidir.
Flask framework’ü kullanılarak geliştirilmiş olup, vatandaş, doktor ve yönetici giriş sistemleri; randevu oluşturma, görüntüleme ve arama işlemleri yapılabilir.

### 🚀 Tasarım Özellikleri

- Modern ve responsive (mobil uyumlu) tasarım
- Bootstrap 5 framework kullanımı
- Bootstrap Icons entegrasyonu
- Kolay kullanılabilir ve sade arayüz
- Kullanıcı, doktor ve yönetici panelleri
- Randevu oluşturma, görüntüleme ve yönetme
- Konuma göre hastane görüntüleme
- Kayıt ve giriş sistemi

### 🚀 Proje Özellikleri

- 🔐 Kullanıcı, doktor ve yönetici kayıt & giriş işlemleri
- 📅 Randevu oluşturma, görüntüleme ve silme
- 🩺 Doktor paneli üzerinden randevu takibi
- 🏥 Konuma göre hastane listeleme
- 📊 Yönetici paneli ile sistem yönetimi
- 📦 JSON dosyaları ile veri saklama
- 💻 Modern ve responsive arayüz (Bootstrap 5)
- 🎨 Bootstrap Icons ile ikon desteği


## Kullanılan Teknolojiler

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Jinja2 Template Engine (Flask ile)


## ⚙️ Kurulum ve Çalıştırma

### ✅ Gereksinimler
Örneğin:  

Bu projeyi çalıştırmak için bilgisayarınızda aşağıdaki yazılımlar kurulu olmalıdır:

- Python 3.x


Ayrıca aşağıdaki kütüphaneler kullanılmaktadır:

- flask
- Flask-Login 0.6.3
- Flask-SQLALchemy 3.1.1
- WerkZeug 3.0.1
- Flask-SocketIO 5.3.6
- python-socketio 5.11.2
- python-engineio 4.9.1

> Not: Bu kütüphaneleri yüklemek için `pip install -r requirements.txt` terminal'e yazarak otomatik olarak yükleyebilirsiniz.

### 🚀 Uygulamayı Başlatma
Örneğin: 
Uygulama tarayıcınızda http://127.0.0.1:5000/ adresinde çalışacaktır.


## 📂 Proje Dosya Yapısı

```
randevu-sistemi/
├── app.py                       # Ana Python uygulama dosyası
├── requirements.txt             # Gerekli Python paketlerini içeren dosya
├── db2json.py                   # JSON veri script dosyası (Kullanıcı verisi)
├── db3json.py                   # JSON veri script dosyası (Doktor verisi)
├── db4json.py                   # JSON veri script dosyası (Randevu verisi)
├── drusers.json                 # Doktor kullanıcı verisi
├── randevular.json              # Randevu verileri
├── users.json                   # Vatandaş kullanıcı verisi
│
├── static/                      # Statik dosyalar (CSS, resimler)
│   ├── resimler/                # Görsel dosyalar
│   │   ├── anasayfaresim.jpg
│   │   ├── eczanelogo.png
│   │   ├── hakkinda.jpg
│   │   ├── tcsağlıkbakanlığı.png
│   │   ├── ttb.png
│   │   └── ...
│   ├── css/                     # Stil dosyaları
│   │   ├── bolumler.css
│   │   ├── doktorgiris.css
│   │   ├── doktorpanel.css
│   │   ├── giris.css
│   │   ├── hakkımızda.css
│   │   ├── kayıt.css
│   │   ├── konumagörehastane.css
│   │   ├── randevu.css
│   │   ├── randevu_olustur.css
│   │   ├── vatandas.css
│   │   └── doktorkayıt.css
│
├── templates/                   # HTML şablon dosyaları
│   ├── admingiris.html
│   ├── adminpanel.html
│   ├── base.html
│   ├── bolumler.html
│   ├── doktorgiris.html
│   ├── doktorkayit.html
│   ├── doktorpanel.html
│   ├── giris.html
│   ├── hakkımızda.html
│   ├── kayit.html
│   ├── konumagorehastane.html
│   ├── kullaniciguncelle.html
│   ├── randevu.html
│   ├── randevuara.html
│   ├── randevu_olustur.html
│   ├── vatandas.html
│   └── ...
│
├── instance/                    # Uygulama örneği için dosyalar
│   └── hastane.db               # SQLite veritabanı dosyası
│
└── README.md                    # Proje açıklama dosyası
```



