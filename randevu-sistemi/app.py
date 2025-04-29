from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def vatandas():
    return render_template("vatandas.html")

@app.route("/kayit")
def kayit():
    return render_template("kayit.html")

@app.route("/giris")
def giris():
    return render_template("giris.html")

@app.route("/bolumler")
def bolumler():
    return render_template("bolumler.html")

@app.route("/hakkımızda")
def hakkımızda():
    return render_template("hakkımızda.html")

@app.route("/doktorgiris")
def doktorgiris():
    return render_template("doktorgiris.html")

@app.route("/doktorkayit")
def doktorkayit():
    return render_template("doktorkayit.html")

@app.route("/randevu")
def randevu():
    return render_template("randevu.html")

@app.route("/randevuara")
def randevuara():
    return render_template("randevuara.html")

@app.route("/konumagorehastane.html")
def konumagorehastane():
    return render_template("konumagorehastane.html")

@app.route("/doktorpanel")
def doktorpanel():
    return render_template("doktorpanel.html")





if __name__ == "__main__":
    app.run(debug=True)