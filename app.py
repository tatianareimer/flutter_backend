from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
import re

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

# Retorna o objeto Professor associado ao user_id (email ou cpf)
'''
@login_manager.user_loader
def professor_loader(user_id):
    if user_id is not None:
        if re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'):
            return Professor.query.get(email=user_id)
        else:
            return Professor.query.get(cpf=user_id)
    return None
'''  
class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'id: {str(self.id)}, email: {self.email}, cpf: {self.cpf}, fullname: {self.fullname}' 

    def to_json(self):
        json_professor = {
            'id': self.id,
            'email': self.email,
            'cpf': self.cpf,
            'fullname': self.fullname,
            'password': self.password
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

class CursoAluno(db.Model):
    __tablename__ = 'students_courses'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

# endpoints

@app.route("/")
def hello_world():
    return "<p>Backend do aplicativo do CCE!</p>"

@app.route("/alunos", methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return make_response(jsonify([aluno.to_json() for aluno in alunos]), 200)

# Get todos os cursos de um professor
@app.route("/professores/<int:professor_id>/cursos", methods=['GET'])
def get_cursos_professor(professor_id):
    cursos = Curso.query.join(CursoProfessor).filter(CursoProfessor.professor_id == professor_id, CursoProfessor.course_id == Curso.id).all()
    return make_response(jsonify([curso.to_json() for curso in cursos]), 200)

# Get todos os alunos em um curso
@app.route("/cursos/<int:course_id>/alunos", methods=['GET'])
def get_curso_alunos(course_id):
    alunos = Aluno.query.join(CursoAluno).filter(CursoAluno.course_id == course_id, CursoAluno.student_id == Aluno.id).all()
    return make_response(jsonify([aluno.to_json() for aluno in alunos]), 200)

@app.route("/login/professor", methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        username_entered = request.args.get('username')
        password_entered = request.args.get('password')
        i = generate_password_hash(password_entered)
        print(i)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username_entered):
            user = Professor.query.filter(Professor.email == username_entered).first()
        else:
            user = Professor.query.filter(Professor.cpf == username_entered).first()
        if user is not None and check_password_hash(user.password, password_entered):
            return jsonify({'signed_in': True})
        return jsonify({'signed_in': False})


        