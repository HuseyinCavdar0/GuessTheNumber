from flask import Flask, render_template

# Flask uygulamasını başlat
app = Flask(
    __name__,
    template_folder="templates",  # varsayılan zaten "templates" ama açıkça yazmak netlik sağlar
    static_folder="static"        # varsayılan "static"
)


@app.route("/")
def index():
    """
    Ana sayfa.
    Tarayıcıya templates/index.html dosyasını gönderir.
    """
    return render_template("index.html")


if __name__ == "__main__":
    # Web arayüzünü tüm ağdan erişilebilir yapıyoruz.
    # Örn: http://192.168.x.x:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
