from flask import Flask, request, render_template, redirect
from flask_mail import Mail, Message


app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'asdasdasdasdasdasd1787@gmail.com'
app.config['MAIL_PASSWORD'] = 'Qwerty54321!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
        print(request.form)
        emailid=request.form['emailid']
        body=request.form['body']
        subject=request.form['subject']

        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[emailid])
        msg.body = body
        mail.send(msg)
        return redirect('/')

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
