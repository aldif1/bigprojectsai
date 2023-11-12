from flask import Flask, render_template,request,jsonify,redirect,url_for
from flask_cors import CORS
import numpy
import random
import tflearn
import tensorflow
import nltk,pickle,json,random;#nltk.download('popular')
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import pymysql.cursors
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('content.json').read())
UPLOAD_FOLDER = 'application/static/upload/'
app = Flask(__name__)
import os
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="dudu rohosio"
    ))
CORS(app)

class Base(DeclarativeBase):
      pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://LENOVO:123@192.168.56.116:3306/rendah_kalori_tinggi_kalori"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the app with the extension
db.init_app(app)

db.Model
db.session

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, )
    email: Mapped[str] = mapped_column(String(255))
    #nama = db.Column(db.String(100))
    #umur = db.Column(db.Integer)
    #alamat = db.Column(db.TEXT)
    #notelepon = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/chatbot',methods=["POST"])
def chatbotl():
    msg = request.form['user_msg']
    
    return "response"

@app.route('/json')
def defjson():
  return jsonify({"status":200,"description":"hello world"})
@app.route('/get')
def method_name():
  userText = request.args.get('msg')
  return chat(userText)
try:
  with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)
except:
  words = []
  labels = []
  docs_x = []
  docs_y = []
with open('content.json') as user_file:
  data = json.load(user_file)
with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load('modell.h5')
def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]
  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]

  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1

  return numpy.array(bag)

def chat(msg):
    results = model.predict([bag_of_words(msg, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    responses=""
    print(tag)
    for tg in data["intents"]:
      if tg['tag'] == tag:
        responses = tg['responses']
    print(responses)
    print(random.choice(responses))
    return random.choice(responses)
@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/tampil.html", users=users)
@app.route("/newuser")
def new_user():
    nama = "Satrio Aldi Firmansyah"
    return render_template("user/newuser.html",nama=nama)
@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("/user/index.html")

           
@app.route('/data')
def data():
    return 'Nama : Satrio Aldi Firmansyah'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('user.html', name=name)


def show_the_login_form():
    return render_template('login.html')

@app.route('/loginput')
def showPut():
    return 'data berhasil  diubah'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return show_the_login_form()
    else:
        return show_the_login_form()
    

@app.route("/users/<int:id>")
def tampil_user(id):
    userr = db.get_or_404(User,id)
    return render_template("update.html",user=userr)

    
@app.route("/users/update/<int:id>", methods=["POST"])
def update_user(id):
    username=request.form["username"]
    email=request.form["email"]

    user=User.query.get(id)

    user.username=username
    user.email=email

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("user_list"))


@app.route("/users/delete/<int:id>",methods=["DELETE"])
def delete_user(id):
    userr = db.get_or_404(User,id)

    db.session.delete(userr)
    db.session.commit()

    return redirect(url_for("user_list"))



#http://127.0.0.1:5000/users

if __name__ == '__main__':
    app.run(ssl_context='adhoc',host="0.0.0.0",debug=True, port=5000)