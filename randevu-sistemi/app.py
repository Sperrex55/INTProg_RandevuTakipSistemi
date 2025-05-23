from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hastane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'giris'
socketio = SocketIO(app)

ADMIN_TC = '12345678901'
ADMIN_PASSWORD = 'admin123'

# MODELLER
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tc_kimlik_no = db.Column(db.String(11), unique=True, nullable=False)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    cinsiyet = db.Column(db.String(10), nullable=False)
    dogum_tarihi = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(128), nullable=False)

class drUser (UserMixin, db.Model):
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

    def __repr__(self):
        return f"<Randevu {self.hasta_adi} {self.randevu_tarihi} {self.randevu_saati}>"

# KULLANICI YÜKLEYİCİ
@login_manager.user_loader
def load_user(user_id):
    if 'user_type' in session:
        if session['user_type'] == 'vatandas':
            return User.query.get(int(user_id))
        elif session['user_type'] == 'doktor':
            return drUser .query.get(int(user_id))
    return None

# GİRİŞ FONKSİYONU
def login_user_by_type(user_type, tc_kimlik_no, password):
    if user_type == 'vatandas':
        user = User.query.filter_by(tc_kimlik_no=tc_kimlik_no).first()
    else:
        user = drUser .query.filter_by(dr_tc_kimlik_no=tc_kimlik_no).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        session['user_type'] = user_type
        return True
    return False

# ROUTE'LER
@app.route("/")
def vatandas():
    return render_template("vatandas.html")

@app.route("/giris", methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        tc_kimlik_no = request.form.get('tc_kimlik_no', '').strip()
        password = request.form.get('password', '').strip()

        if not tc_kimlik_no or not password:
            flash('Lütfen TC kimlik numarası ve şifrenizi giriniz!', 'danger')
            return redirect(url_for('giris'))

        if login_user_by_type('vatandas', tc_kimlik_no, password):
            flash('Başarıyla giriş yaptınız!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('randevu'))

        flash('TC kimlik numarası veya şifre hatalı!', 'danger')
        return redirect(url_for('giris'))

    return render_template("giris.html")

@app.route("/kayit", methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('sifre')
            tc_kimlik_no = request.form.get('tc_kimlik_no')

            if not all([email, password, tc_kimlik_no]):
                flash('Lütfen tüm alanları doldurun!', 'danger')
                return redirect(url_for('kayit'))

            if User.query.filter_by(email=email).first() or User.query.filter_by(tc_kimlik_no=tc_kimlik_no).first():
                flash('Bu e-posta veya TC kimlik numarası zaten kayıtlı!', 'danger')
                return redirect(url_for('kayit'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(
                email=email,
                password=hashed_password,
                ad=request.form.get('ad'),
                soyad=request.form.get('soyad'),
                tc_kimlik_no=tc_kimlik_no,
                cinsiyet=request.form.get('cinsiyet'),
                dogum_tarihi=datetime.strptime(request.form.get('dogum_tarihi'), '%Y-%m-%d').date(),
                telefon=request.form.get('telefon')
            )

            db.session.add(new_user)
            db.session.commit()

            flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
            return redirect(url_for('giris'))

        except Exception as e:
            db.session.rollback()
            flash(f'Kayıt sırasında hata oluştu: {str(e)}', 'danger')
            return redirect(url_for('kayit'))

    return render_template('kayit.html')

@app.route("/randevu")
@login_required
def randevu():
    tum_randevular = Randevu.query.filter_by(kullanici_id=current_user.id).order_by(Randevu.randevu_tarihi, Randevu.randevu_saati).all()
    bugun = date.today()
    aktif_randevular = [r for r in tum_randevular if r.randevu_tarihi >= bugun]
    gecmis_randevular = [r for r in tum_randevular if r.randevu_tarihi < bugun]

    return render_template(
        "randevu.html",
        user=current_user,
        aktif_randevular=aktif_randevular,
        gecmis_randevular=gecmis_randevular
    )

@app.route("/bolumler")
def bolumler():
    return render_template("bolumler.html")

@app.route("/hakkımızda")
def hakkımızda():
    return render_template("hakkımızda.html")

@app.route("/doktorgiris", methods=['GET', 'POST'])
def doktorgiris():
    if request.method == 'POST':
        dr_tc_kimlik_no = request.form.get('dr_tc_kimlik_no')
        password = request.form.get('password')

        if not dr_tc_kimlik_no or not password:
            flash('Lütfen TC kimlik numarası ve şifrenizi giriniz!', 'danger')
            return render_template("doktorgiris.html")

        if login_user_by_type('doktor', dr_tc_kimlik_no, password):
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('doktorpanel'))

        flash('TC kimlik numarası veya şifre hatalı!', 'danger')

    return render_template("doktorgiris.html")

@app.route("/doktorkayit", methods=['GET', 'POST'])
def doktorkayit():
    if request.method == 'POST':
        try:
            dr_email = request.form.get('dr_email')
            password = request.form.get('dr_password')
            dr_tc_kimlik_no = request.form.get('dr_tc_kimlik_no')

            if drUser .query.filter_by(dr_email=dr_email).first() or drUser .query.filter_by(dr_tc_kimlik_no=dr_tc_kimlik_no).first():
                flash('Bu e-posta veya TC kimlik numarası zaten kayıtlı!', 'danger')
                return redirect(url_for('doktorkayit'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_doctor = drUser (
                dr_email=dr_email,
                password=hashed_password,
                dr_ad=request.form.get('dr_ad'),
                dr_soyad=request.form.get('dr_soyad'),
                dr_tc_kimlik_no=dr_tc_kimlik_no,
                dr_cinsiyet=request.form.get('dr_cinsiyet'),
                dr_dogum_gunu=datetime.strptime(request.form.get('dr_dogum_gunu'), '%Y-%m-%d').date(),
                dr_uzmanlik_alani=request.form.get('dr_uzmanlik_alani'),
                dr_diploma_no=request.form.get('dr_diploma_no'),
                dr_telefon=request.form.get('dr_telefon'),
                dr_hastane_adi=request.form.get('dr_hastane_adi')
            )

            db.session.add(new_doctor)
            db.session.commit()

            flash('Doktor kaydı başarıyla oluşturuldu!', 'success')
            return redirect(url_for('doktorgiris'))

        except Exception as e:
            db.session.rollback()
            flash(f'Kayıt sırasında hata oluştu: {str(e)}', 'danger')
            return redirect(url_for('doktorkayit'))

    return render_template('doktorkayit.html')

@app.route("/randevuara")
@login_required
def randevuara():
    return render_template("randevuara.html", user=current_user)

@app.route("/konumagorehastane")
@login_required
def konumagorehastane():
    return render_template("konumagorehastane.html", user=current_user)

@app.route("/doktorpanel")
@login_required
def doktorpanel():
    if session.get('user_type') != 'doktor':
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('vatandas'))
    
    randevular = Randevu.query.filter_by(doktor_bolumu=current_user.dr_uzmanlik_alani).order_by(Randevu.randevu_tarihi, Randevu.randevu_saati).all()
    return render_template("doktorpanel.html", drUser =current_user, randevular=randevular)

@app.route('/admingiris', methods=['GET', 'POST'])
def admingiris():
    if request.method == 'POST':
        tc_kimlik_no = request.form.get('tc_kimlik_no')
        password = request.form.get('password')
        
        if tc_kimlik_no == ADMIN_TC and password == ADMIN_PASSWORD:
            session['admin_giris'] = True
            session['admin_tc'] = tc_kimlik_no  # Ek güvenlik için
            flash('Başarıyla giriş yapıldı.', 'success')
            return redirect(url_for('adminpanel'))
        else:
            flash('Geçersiz TC Kimlik No veya şifre.', 'danger')
    
    return render_template('admingiris.html')

@app.route('/adminpanel')
def adminpanel():
    
    if not session.get('admin_giris'):
        flash('Bu sayfaya erişmek için yönetici girişi yapmalısınız.', 'warning')
        return redirect(url_for('admingiris'))
    
    try:
        users = User.query.order_by(User.id.desc()).all()
        doctors = drUser .query.order_by(drUser .id.desc()).all()
        return render_template('adminpanel.html', users=users, doctors=doctors)
    
    except Exception as e:
        flash('Veriler yüklenirken hata oluştu: ' + str(e), 'danger')
        app.logger.error(f"Admin panel error: {str(e)}")
        return render_template('adminpanel.html', users=[], doctors=[])

@app.route('/admincikis')
def admincikis():
    session.clear()  # Tüm oturum verilerini temizle
    flash('Başarıyla çıkış yapıldı.', 'info')
    return redirect(url_for('admingiris'))

@app.route("/kullanicisil/<int:id>", methods=['POST'])
def kullanicisil(id):
    try:
        user_to_delete = User.query.get(id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Kullanıcı başarıyla silindi.', 'success')
        else:
            flash('Kullanıcı bulunamadı.', 'danger')
    except Exception as e:
        flash(f'Hata: {str(e)}', 'danger')
    return redirect(url_for('adminpanel'))

@app.route("/kullaniciguncelle/<int:id>", methods=['GET', 'POST'])
def kullaniciguncelle(id):
    user = User.query.get(id)
    if not user:
        flash('Kullanıcı bulunamadı!', 'danger')
        return redirect(url_for('adminpanel'))

    if request.method == 'POST':
        user.ad = request.form.get('ad')
        user.soyad = request.form.get('soyad')
        user.email = request.form.get('email')
        db.session.commit()
        flash('Kullanıcı bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('adminpanel'))

    return render_template('kullaniciguncelle.html', user=user)

@app.route('/doktorsil/<int:id>', methods=['POST'])
def doktorsil(id):
    if not session.get('admin_giris'):
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('admingiris'))
    
    doctor = drUser .query.get_or_404(id)
    try:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doktor başarıyla silindi.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Silme işlemi sırasında hata oluştu: ' + str(e), 'danger')
    
    return redirect(url_for('adminpanel'))

@app.route('/doktorguncelle/<int:id>', methods=['GET', 'POST'])
def doktorguncelle(id):
    if not session.get('admin_giris'):
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('admingiris'))
    
    doctor = drUser .query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            doctor.dr_ad = request.form['dr_ad']
            doctor.dr_soyad = request.form['dr_soyad']
            doctor.dr_uzmanlik_alani = request.form['dr_uzmanlik_alani']
            doctor.dr_hastane_adi = request.form['dr_hastane_adi']
            doctor.dr_email = request.form['dr_email']
            doctor.dr_telefon = request.form['dr_telefon']
            
            if request.form['dr_password']:
                doctor.password = generate_password_hash(request.form['dr_password'])
            
            db.session.commit()
            flash('Doktor bilgileri güncellendi.', 'success')
            return redirect(url_for('adminpanel'))
            
        except Exception as e:
            db.session.rollback()
            flash('Güncelleme sırasında hata oluştu: ' + str(e), 'danger')
    
    return render_template('doktorguncelle.html', doctor=doctor)

@app.route("/randevu_olustur", methods=['GET', 'POST'])
@login_required
def randevu_olustur():
    if request.method == 'POST':
        try:
            randevu_tarihi = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d').date()
            randevu_saati = datetime.strptime(request.form.get('appointment_time'), '%H:%M').time()

            existing_appointment = Randevu.query.filter_by(
                randevu_tarihi=randevu_tarihi,
                randevu_saati=randevu_saati,
                doktor_bolumu=request.form.get('doctor_id')
            ).first()

            if existing_appointment:
                flash('Bu tarih ve saatte zaten bir randevu var. Lütfen başka bir zaman seçin.', 'danger')
                return redirect(url_for('randevu_olustur'))

            yeni = Randevu(
                hasta_adi=f"{current_user.ad} {current_user.soyad}",
                tc_no=request.form.get('tc_no'),
                telefon=request.form.get('phone_number'),
                doktor_bolumu=request.form.get('doctor_id'),
                                randevu_tarihi=randevu_tarihi,
                randevu_saati=randevu_saati,
                kullanici_id=current_user.id
            )
            db.session.add(yeni)
            db.session.commit()
            flash('Randevunuz başarıyla oluşturuldu!', 'success')
            return redirect(url_for('randevu'))
        except Exception as e:
            db.session.rollback()
            flash(f'Randevu kaydında hata: {e}', 'danger')
            return redirect(url_for('randevu_olustur'))

    return render_template("randevu_olustur.html", user=current_user)


@app.route("/arama")
@login_required
def arama():
    return render_template("arama.html")


@app.route('/onayla', methods=['POST'])
@login_required
def onayla():
    randevu_id = request.form.get('randevu_id')
    randevu = Randevu.query.get(int(randevu_id))
    if randevu:
        randevu.durum = 'Onaylandı'
        db.session.commit()
        socketio.emit('randevu_onaylandi', {'randevu_id': randevu_id, 'durum': 'Onaylandı'})
        return jsonify({'success': True, 'new_status': 'Onaylandı'})
    return jsonify({'success': False, 'message': 'Randevu bulunamadı'}), 404


@app.route('/reddet', methods=['POST'])
@login_required
def reddet():
    randevu_id = request.form.get('randevu_id')
    randevu = Randevu.query.get(int(randevu_id))
    if randevu:
        randevu.durum = 'Reddedildi'
        db.session.commit()
        socketio.emit('randevu_reddedildi', {'randevu_id': randevu_id, 'durum': 'Reddedildi'})
        return jsonify({'success': True, 'new_status': 'Reddedildi'})
    return jsonify({'success': False, 'message': 'Randevu bulunamadı'}), 404


@app.route("/cikis")
@login_required
def cikis():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('vatandas'))


#if __name__ == "__main__":
 #   with app.app_context():
  #      db.create_all()
   # socketio.run(app, debug=True)
import os
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
