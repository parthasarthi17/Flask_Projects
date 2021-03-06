#This application demonstrates how to have web users submit form data directly to your mail account via AWS SES.
from flask import Flask, render_template, flash, request
from flask_wtf import Form
from wtforms import Form, StringField, validators, TextAreaField
from wtforms.validators import DataRequired
import boto3
from conf import aws_conf as conf

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = conf.SECRET_KEY


#Reusbale Form to enter name and email
class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.DataRequired()])
    email = StringField('Email:', validators=[validators.DataRequired()])

#Form Main Page
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
#Send email using SES resource
    ses_client = boto3.client('ses')

    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        body=request.form['body']

        user_json = {}
        user_json['customer_email'] = request.form.get('email')
        user_json['comments'] = request.form.get('Thank you for your email')

        SUBJECT = 'Email generated by SES'
        BODY_HTML = render_template( 'pretty_json.html', user_json = user_json )

        # sending email with all details with amzon ses
        response = ses_client.send_email(
         Destination = { 'ToAddresses': [ email, ], },
         Message={ 'Body': { 'Html': { 'Charset': conf.CHARSET, 'Data': BODY_HTML, },
                            'Text': { 'Charset': conf.CHARSET, 'Data':[body], }, },
                  'Subject': { 'Charset': conf.CHARSET, 'Data': SUBJECT, },},
         Source=conf.SENDER, )

        if form.validate():
            return render_template('thank_you.html',respondent1=name,respondent2= email)
        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
