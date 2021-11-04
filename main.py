from flask import Flask,render_template, request , make_response ,url_for, redirect , flash
from forms import ContactForm
from flask_mail import Message, Mail 
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisismysecret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mohamednaim278@gmail.com'
app.config['MAIL_PASSWORD'] = 'mo12345naeM'

mail = Mail(app)



@app.route('/')
@app.route('/index.html')
@app.route('/Home')
def index():
    
    title = 'my website'
    return render_template('index.html', title= title)
    
    
@app.route('/about.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact.html')
@app.route('/contact', methods=['GET','POST'])
@app.route('/form', methods=['GET', 'POST'])
def contactForm():
	form = ContactForm()
	if request.method == 'GET':
		return render_template('contact.html', form=form)
	elif request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required !')
			return render_template('contact.html', form=form)
		else:
			msg = Message(form.subject.data, sender="mohamednaim278@gmail.com", recipients=['sami_alfattani@hotmail.com'])
			msg.body = """
			from: %s &lt;%s&gt
			%s
			"""% (form.name.data, form.email.data, form.message.data)
			mail.send(msg)
			return redirect(url_for('index'))
		return '<h1>Form submitted!</h1>'



@app.route('/course.html')
@app.route('/course')
def course():
    
    return render_template('course.html')


@app.route('/cookie')
def cookie():
    if request.args.get('t'):
       my_text = request.args.get('t')
    else:
        my_text = ''
    if request.args.get('new_cookie'):
        new_cookie = request.args.get('new_cookie') 
    else:
        new_cookie =''
    if request.cookies.get('my_cookie'):
        my_cookie = request.cookies.get('my_cookie')
    else:
        my_cookie = ''
        resp = make_response(my_cookie + ' | ' + my_text)
        if new_cookie != ' ':
            resp.set_cookie('my_cookie', new_cookie)  
            return resp  

@app.route('/handle_data', methods=['POST', 'GET'])
def handle_data():
    us = request.form['username']
    pw = request.form['password']
    
    return render_template(
        'index.html',
        message=f"{us} is registered {pw}",
        msg_class= "alert alert-success")

           
from waitress import serve    
if __name__ == "__main__":
   print("--PRODUCTION MODE ---")
   p = os.environ.get('PORT')
   p = '5050' if p == None else p
   serve(app, host='0.0.0.0', port=p)

   