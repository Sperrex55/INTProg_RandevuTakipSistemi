# Hastane Randevu Sistemi Tasarımı

Hastane randevularınızı kolayca almanın, yönetmenin ve takip etmenin en modern yolu artık burada. MediRandevu ile uzun bekleme sürelerine veda edin, zamanınızı verimli kullanmanız için tasarlanmış bir web arayüzüdür.

## Tasarım Özellikleri

- Modern ve responsive tasarım
- Bootstrap 5 framework kullanımı
- Bootstrap Icons entegrasyonu
- Kullanıcı dostu arayüz


## Kullanılan Teknolojiler

- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Jinja2 Template Engine

## Proje Yapısı

```
randevu-sistemi/
│── app.py                      # Ana Flask uygulama dosyanız
│── requirements.txt            # Bağımlılıklar
├── static/                     # Statik dosyalar (CSS, JS, resimler)
│   ├── resimler/               # Resim dosyaları
│   │   ├── anasayfaresim.jpg
│   │   ├── eczanelogo.png
│   │   ├── hakkinda.jpg
│   │   ├── tcsaglikbakanlığı.png
│   │   └── itb.png
│   └── css/                    # CSS dosyaları
│       ├── bolumler.css
│       ├── doktorgiris.css
│       ├── doktorkayit.css
│       ├── doktorpanel.css
│       ├── giris.css
│       ├── hakkımızda.css
│       ├── kayıt.css
│       ├── konuma_gore_hastane.css  # Boşluk yerine alt çizgi kullanın
│       ├── randevu.css
│       ├── randevuara.css
│       └── vatandas.css
└── templates/                  # HTML şablonları
    ├── vatandas.html
    ├── kayit.html
    ├── giris.html
    ├── bolumler.html
    ├── hakkımızda.html
    ├── doktorgiris.html
    ├── doktorkayit.html
    ├── randevu.html
    ├── randevuara.html
    ├── konumagorehastane.html
    └── doktorpanel.html
```

## Tasarım Özellikleri

### Renkler
- primary-blue: #0d6efd;
- secondary-green: #28a745;
- accent-red: #dc3545;
- light-gray: #f8f9fa;
- dark-gray: #6c757d;
  

### Responsive Tasarım
- Mobil cihazlara uyumlu
- Tablet ve masaüstü için optimize edilmiş görünüm
- Grid sistemi ile esnek yerleşim

