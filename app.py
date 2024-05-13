from flask import render_template, request, redirect, Flask
from sqlite3 import connect
from random import choice, randint
from os import chdir, remove
import os

app=Flask(__name__)
db=connect("url.db", check_same_thread=False)
sql=db.cursor()
alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890&'

sql.execute("""CREATE TABLE IF NOT EXISTS urls(
                url TEXT NOT NULL,
                url_id TEXT UNIQUE
)""")

db.commit()

ip_adress_pre = "0.0.0.0"
ip_adress = ip_adress_pre + ":5050"

def delete_qrs():
    entries = os.listdir()
    for entry in entries:
        if 'img' in entry:
            name=entry
            os.remove(name)
            
@app.route("/")
def red():
    delete_qrs()
    global name
    try:
        remove(name)
    except:
        pass
    return render_template("index.html", ip_adress=ip_adress)

name=''
    

@app.route("/get_link/", methods=['POST'])
def get_from_main_page():
    delete_qrs()
    message = ''
    inp_ref = ''
    if request.method=="POST":
        inp_ref = request.form.get("inp_ref")
        if "http" in inp_ref:
            out_ref=''
            for i in range(5):
                out_ref = out_ref+ choice(alphabet)
            sql.execute("""INSERT INTO urls (url, url_id) VALUES (?, ?)""", (inp_ref, out_ref))
            db.commit()
            out_ref = f"http://{ip_adress}/" + out_ref
            message = out_ref
    return render_template("getlink.html", message=message, ip_adress=ip_adress)

@app.route("/qr/", methods=['POST'])
def get_qr_code():
    delete_qrs()
    import qrcode
    from os import chdir
    chdir("C:\\Users\\Misha\\Documents\\python\\EIS\\murl"+"\\static\\")
    global name
    if request.method=="POST":
        inp_ref = request.form.get("inp_ref2")
        name=''
        for i in range(10):
            name = name+ str(randint(0,9))
        name = "img"+name+".png"
        img = qrcode.make(inp_ref)
        type(img)
        img.save(name)
    return render_template("getqr.html", img=f"/static/{name}", ip_adress=ip_adress)

@app.route("/<link_id>/")
def redir(link_id):
    delete_qrs()
    if link_id!=None:
        sql.execute("""SELECT url FROM urls WHERE url_id=(?)""", (link_id,))
        out = sql.fetchone()
        out=out[0]
        return redirect(out)
    
@app.route("/qr_link_enter/")
def qr():
    delete_qrs()
    return render_template("link_qr.html", ip_adress=ip_adress)

@app.route("/short_link_enter/")
def link():
    delete_qrs()
    return render_template("link_short.html", ip_adress=ip_adress)

@app.route("/account/")
def acc():
    delete_qrs()
    return render_template("account.html", ip_adress=ip_adress)

if __name__ == "__main__":
    app.run(host=ip_adress_pre, port=5050, debug=False)