from flask import Flask,render_template,request,redirect
import csv
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
app = Flask(__name__)
print(__name__)

@app.route('/index.html')
def hello_world():
    return render_template('index.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
	return render_template(page_name)


def write_to_database(data):
	with open('database.txt','a') as database:
		email=data["email"]
		subject=data["subject"]
		message=data["message"]
		database.write(f'\n email:  {email},subject:  {subject},message:  {message}')

def write_to_csv(data):
	with open('database.csv',newline='', mode='a') as db:
		email=data["email"]
		subject=data["subject"]
		message=data["message"]
		writer=csv.writer(db,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow([email,subject,message])


def send_mail(data):
	html=Template(Path('new.html').read_text())
	email = EmailMessage()
	email['from'] = 'Priyanshu'
	email['to'] = 'Priyanshupareta@gmail.com'
	email['subject'] = data["subject"]
	email['message'] = data["message"]
	email.set_content(html.substitute({'email':data["email"],'message':data["message"]}),'html')

	with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
	    smtp.ehlo()
	    smtp.starttls()
	    smtp.login('priyanshuparetaforpython@gmail.com','kabirsingh123')
	    smtp.send_message(email)



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
    	try:
    		data=request.form.to_dict()
    		write_to_csv(data)
    		send_mail(data)
    		return redirect('/thankyou.html')

    	except:
    		return 'Could not write to database'
	
    else:
        return 'Invalid username/password'