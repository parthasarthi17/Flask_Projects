from flask import Flask, request, render_template, redirect, jsonify, url_for, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_recaptcha import ReCaptcha
from middleware import middleware
from functools import wraps


app = Flask(__name__)
api = Api(app)

app.config['RECAPTCHA_SITE_KEY'] = '6LeV5RoeAAAAABcqy4HkOh-IqjmU3yK33MbU6pZx'
app.config['RECAPTCHA_SECRET_KEY'] = '6LeV5RoeAAAAADq63a02G9Bx98rts-ThFaD0xs-n'

import requests
import json




#app.wsgi_app = middleware(app.wsgi_app)

recaptcha = ReCaptcha(app)

@app.before_request
def before_request():
    print('-----------------------')
    #print(request.__dict__, '+================inoked=================')
    print('======inoked========')
    #print(request.form)

    if request.method == 'POST':
        #parser = reqparse.RequestParser()
        #parser.add_argument('text', type=str, help='Name can not be blank', required=True)
        #parser.add_argument('g-recaptcha-response', type=str, help='Password can not be blank', required=True)
        #args = parser.parse_args()

        #texxt = args["text"]
        #print(texxt)
        print(request.form['text'])

        # 03AGdBq25kyAlB-j48mrIeHVHl0fcYPQ0Rh7Tr2c5D91jw7RxZtV4xWFpxJEf7hTKglQqK5wEJ3uvNcSccB1XaVAGMr30t7LPZ16BgaiR5tjchb-0UtZfo-c2SaBmFTVfaHIr8oiOykuKeTx6o1WXWLNtt165t6LmdqvoLmJx5UlvdJXjuUx4zoSotBDwETN5vVHS7U-NzloA5Pb9cgivrQmG4u51_-Sfs4E2xaw5tAgL0xEDJWcY-6kPFgXqxUU-9LvhwKvGb6GYgvQaeAZDVG3ZshlWZSAjgg9nhXhlY1niobSeYSqKXYMyYEpKVOgGMZcI6hGo-Lh6F5tctJU1MykMFEdcRX30sWwzykA2URv_xVyj7SjQXY3SPzprfbgE4VHrkjlCi0lJ5-FNKr25UK_FZOI9v_kj_eVdxpZ2U3ROeDji8aDiPSM6mbngcK-ecw96_o0h3abSE


        #xx = '03AGdBq265ZBsL_DT0NYL6SZRvjhK6FtdVGldOiavVe8lbrMZSsVK2krAbqV5DNxq6p60ey0w4DA-lHp38L9mElUCi2NkqcGI3N4XR7QTjSUzJ51T02QNI1fBIeQTwJ7eGhzgRPeTBBC-a-bcYSjQfJtiONjfSvfk3f3r1v7wvkLSycwZ21BtwWEZRnO-MGNKokEfUDcYLdqPPYXu1rjDZo29KtKGh5Fz_f2HGjwG1z5b646NKTjTmgEYvoj2iGybV24c1EvC6gYG9Ngz0SkPW7MDh1m6DXTjyCSFguulU423k809JXmb6dnGEV7kH1yh1hcoJHt8cmwrlOs4f5wbo2G7Q6But1-6xyXgjNC0CAtr399sjQNKFAYtqNXztba5fDogMAcgaJ4b4ZqFEgMz1b3ckpHdighUJvoHEsCRY0V-bAaMbBxQQ83yVoRIdjEUTLFDgUAq9QRbDItEmQ2ENjeLDV2vPdagvQA'

        captcha_key = request.form['g-recaptcha-response']

        secret_key = '6LeV5RoeAAAAADq63a02G9Bx98rts-ThFaD0xs-n'

        print(captcha_key)


        captcha_data = {
                                'secret': secret_key,
                                'response': captcha_key
                }

        #r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)

        #response = json.loads(r.text)
        #print(response)
        #verify = response['success']

        #if verify:
            #print(verify)
            #print("success!!")


        #xxx = '03AGdBq27dGJleQDR2ok34lzPRqU7kX5HdrWaIkCl4hTeezeboagvzSS9SBr4QneMHSIFHuJly3VsSzCWsN4Y2j657R6NuSjj1AmEZ4DRQ3HQ1dVceqmUmvbKYrec_ZqQguqWcCiB5wxCU9Vul85-FapPBJ5JE9X8xDwF8jCD4-PguY3q88vcxSettC6MTlhpN3WJRQIrd8DUBXlbWtRha9SnxDmS7L2FUwvFyPhiQYIvInO6Bi_KAQCT4AFgarVwXba5GxuIHNu2whrIc2eqHnoxwvSLsd0HMZ5q78epn0vrG5Gioq6_49yZlzz6AAJWnqDf0CSRAyZXJmLSyesPXwK4-QG_t1ZEXqdbv_aCr33uKmpLuYv90UISSqYFzHIaY6IA5dUviBKnUOsDryW_cTdImqqkO_rMS4C7IRXjQl4Rn1_yJ941TbAUTJ3NlHf4pKAHKj1krzRwn'



        #print(request.args.get("text"))
        #if recaptcha.verify(captcha_key): # Use verify() method to see if ReCaptcha is filled out
        #    print('Thanks for filling out the form!') # Send success message

        #else:
        #    print('bs')
        #    print(request.form)


    print('-----------------------')


@app.route('/', methods=['GET', 'POST'])
def index():
    message = '' # Create empty message
    if request.method == 'POST': # Check to see if flask.request.method is POST
        print('---------------------------')
        print(request.form['text'])
        print('---------------------------')

    return render_template('index.html', message=message)

#class index(Resource):
#
#    def post(self):
#            parser = reqparse.RequestParser()
#            parser.add_argument('text', type=str, help='Name can not be blank', required=True)
#            parser.add_argument('g-recaptcha-response', type=str, help='Password can not be blank', required=True)
#            args = parser.parse_args()
#
#            texxt = args["text"]
#            print(texxt)
#            print(request.args)
#            print(request.args.get('text'))
#            return "hello"
#api.add_resource(index, "/")

#sOm3uheXbs6SCMNISfnnZZ1GYYh14WOBaIh2D5VtaH88M65DG6b3yK8F1DNHW72Z


if __name__ == '__main__':
    app.run()
