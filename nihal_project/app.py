from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace the connection string with your RDS details
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost:5432/user_data'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    pin = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    pin = request.form['pin']

    print(firstname)
    print(lastname)
    user = session.query(User).filter(User.firstname == firstname, User.lastname == lastname).first()
    print(user)
    if user is None:
        print("here")
        return render_template('invalid.html')
         
    if user.pin != pin:
        return render_template('invalid.html') 
        print("here1")
    
    return render_template('valid.html')     
    # Continue with the rest of your logic...

if __name__ == '__main__':
    app.run(debug=True)