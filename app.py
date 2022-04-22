from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ysafvvroofbffc:95cd603cd3c46a9bb77a0561b4941707e60bad415d0ec5226f4aabc9c2adf3bb@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d3najhi1ikpu7r"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

# models

class Aluno(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    lastlogin = db.Column(db.String(50))

    def __repr__(self):
        return f'id: {str(self.id)}, email: {self.email}, cpf: {self.cpf}, fullname: {self.fullname}'

    def to_json(self):
        json_aluno = {
            'id': self.id,
            'email': self.email,
            'cpf': self.cpf,
            'fullname': self.fullname
        }
        return json_aluno

class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    lastlogin = db.Column(db.String(50))

    def __repr__(self):
        return f'id: {str(self.id)}, email: {self.email}, cpf: {self.cpf}, fullname: {self.fullname}' 

    def to_json(self):
        json_professor = {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname
        }
        return json_professor

class Curso(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    classroom = db.Column(db.String(50))
    begin = db.Column(db.Integer)
    finish = db.Column(db.Integer)
    days = db.Column(db.ARRAY(db.String))

    def __repr__(self):
        return f'id: {str(self.id)}, name: {self.name}, classroom: {self.classroom}, begin: {str(self.begin)}, finish: {str(self.finish)}, days:{str(self.days)}'

    def to_json(self):
        json_curso = {
            'id': self.id,
            'name': self.name,
            'classroom': self.classroom,
            'begin': self.begin,
            'finish': self.finish,
            'days': self.days
        }
        return json_curso

class CursoProfessor(db.Model):
    __tablename__ = 'professors_courses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))

# controllers

@app.route("/")
def hello_world():
    return "<p>Backend do aplicativo do CCE!</p>"

@app.route("/alunos", methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return make_response(jsonify([aluno.to_json() for aluno in alunos]), 200)

@app.route("/professores/<int:professor_id>/cursos", methods=['GET'])
def get_cursos_professor(professor_id):
    cursos = Curso.query.join(CursoProfessor).filter(CursoProfessor.professor_id == professor_id, CursoProfessor.course_id == Curso.id).all()
    return make_response(jsonify([curso.to_json() for curso in cursos]), 200)

