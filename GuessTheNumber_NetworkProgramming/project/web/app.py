from flask import Flask, render_template

# Flask başlat
app = Flask(
    __name__,
    template_folder="templates",  
    static_folder="static"        
)


@app.route("/")
def index():
    #Ana sayfa   tarayıcıya templates/index.html dosyasını gönderir

    return render_template("index.html")


if __name__ == "__main__":
    # Web arayüzü tüm ağdan erişilebilir http://192.168.x.x:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
