from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from programs import samelogs_function
from programs import maincode_function
import boto3

#initiating flask object 
app = Flask(__name__) 
# setting an environment to production
ENV = 'prod'          

# connecting with amazon s3 instance for log files.
# Please enter your AWS IAM user's access_key and secret_access_key.
# note: Please do not share your acess key with anyone for sercurity reasons.

s3 = boto3.resource(service_name=###,
                    region_name='########',
                    aws_access_key_id='####################', 
                    aws_secret_access_key='########################################')

                    

    
# getting bucket
s3Buc=s3.Bucket('log-data-bucket1')
ENV = 'prod'

if ENV == 'dev':
    app.debug= True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:freeloader#007@localhost/admin_habits'
elif ENV == 'prod':
    app.debug= False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uuadhyxpvgoadl:12967f2d4d8fbc032396e7b099c5ecbbcaa75fcb630cc2139892acf5f2266ce6@ec2-3-222-127-167.compute-1.amazonaws.com:5432/de3okqprj58fsj'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initiating data base for sqlalchemy
db = SQLAlchemy(app)

class Log(db.Model):
    __tablename__='admin_data'
    id=db.Column(db.Integer, primary_key=True)
    log_name = db.Column(db.String(200))
    log_date = db.Column(db.String(200))
    log_keyword = db.Column(db.Text())
  
    
    def __init__(self, log_name, log_date, log_keyword):
        self.log_name=log_name
        self.log_date=log_date
        self.log_keyword=log_keyword
     


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        log_name = request.form['log_name']
        log_date = request.form['log_date']
        log_keyword = request.form['log_keyword']
        #print(customer, dealer, rating, comments)
        
        if log_name == '' or log_date == '':
            return render_template('index.html', message='Please enter the required inputs')
        
        data = Log(log_name, log_date, log_keyword)
        print("User Entered: ",log_name, log_date, log_keyword)
        db.session.add(data)
        db.session.commit()
        print("Data added to database")
        #samelogs_function.f1(log_name, log_date, log_keyword)
        maincode_function.main_func(log_name, log_date, log_keyword,s3Buc)
    return render_template('success.html')
        
        

if __name__ == '__main__':
    
    app.run()
