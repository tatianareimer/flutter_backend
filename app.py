from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:android2022!inf1300@localhost/cce_app"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ysafvvroofbffc:95cd603cd3c46a9bb77a0561b4941707e60bad415d0ec5226f4aabc9c2adf3bb@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d3najhi1ikpu7r"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = 'alunos'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    lastlogin = db.Column(db.String(50))

    def __repr__(self):
        return '<Aluno %r>' % self.username

    def to_json(self):
        json_user = {
            'username': self.username,
        }
        return json_user

@app.route("/")
def hello_world():
    return "<p>Backend do aplicativo do CCE!</p>"

@app.route("/alunos", methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return make_response(jsonify([aluno.to_json() for aluno in alunos] ), 200)