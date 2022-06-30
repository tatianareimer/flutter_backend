from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
            'fullname': self.fullname
        }
        return json_professor

class Curso(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    classroom = db.Column(db.String(50))
    schedule = db.Column(db.JSON)

    def __repr__(self):
        return f'id: {str(self.id)}, name: {self.name}, classroom: {self.classroom}, schedule: {str(self.schedule)}'

    def to_json(self):
        json_curso = {
            'id': self.id,
            'name': self.name,
            'classroom': self.classroom,
            'schedule': self.schedule
        }
        return json_curso

class Presenca(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    present = db.Column(db.Boolean, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'id: {str(self.id)}, present: {str(self.present)}, course_id: {str(self.course_id)}, student_id: {str(self.student_id)}, date: {self.date}' 

    def to_json(self):
        json_presenca = {
            'id': self.id,
            'present': self.present,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'date': self.date
        }
        return json_presenca

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

# Login do app - professor
@app.route("/login/professor", methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        username_entered = request.args.get('username')
        password_entered = request.args.get('password')
        #i = generate_password_hash(password_entered)
        #print(i)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username_entered):
            user = Professor.query.filter(Professor.email == username_entered).first()
        else:
            user = Professor.query.filter(Professor.cpf == username_entered).first()
        if user is not None and check_password_hash(user.password, password_entered):
            return make_response(jsonify(user.to_json()), 201)
            #return make_response(jsonify({'signed_in': True}),200)
        return make_response(jsonify({'signed_in': False}),400)

# Login do app - aluno
@app.route("/login/aluno", methods=['GET', 'POST'])
def login_aluno():
    if request.method == 'POST':
        username_entered = request.args.get('username')
        password_entered = request.args.get('password')
        #i = generate_password_hash(password_entered)
        #print(i)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username_entered):
            user = Aluno.query.filter(Aluno.email == username_entered).first()
        else:
            user = Aluno.query.filter(Aluno.cpf == username_entered).first()
        if user is not None and check_password_hash(user.password, password_entered):
            return make_response(jsonify(user.to_json()), 201)
            #return make_response(jsonify({'signed_in': True}),200)
        return make_response(jsonify({'signed_in': False}),400)

# Post aluno na lista de presença de uma matéria em um determinado dia 
@app.route("/attendances/alunos", methods=['POST'])
def post_attendance_aluno():
    data = request.get_json()
    added = 0
    try:
        for element in data:
            last_id = Presenca.query.order_by(Presenca.id.desc()).first()
            if (last_id == None):
                last_id = 1
            else:
                last_id = last_id.id + 1
            attendance = Presenca(id=last_id,present=element['present'], course_id=element['course_id'], student_id=element['student_id'], date=element['date'])
            db.session.add(attendance)
            db.session.commit()
            if (attendance.id):  
                added += 1 
        if (added == len(data)):
            return make_response(jsonify({'added': True}),201)
        else:
            return make_response(jsonify({'added': False}),400)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({'added': False}),400)

# Get lista de presença por disciplina
@app.route("/curso/<int:course_id>/dates", methods=['GET'])
def get_attendance_dates(course_id):
    dates = Presenca.query.filter(Presenca.course_id == course_id).all()
    return make_response(jsonify([date.to_json() for date in dates]), 200)

# Get lista de alunos por presença em um dia
@app.route("/alunos/presenca", methods=['POST'])
def get_dates_students():
    data = request.get_json()
    date = data["data"]
    course = data["curso"]
    result = db.session.query(Aluno, Presenca).with_entities(Aluno.fullname, Presenca.present).join(Presenca).filter(Presenca.date == date, Presenca.student_id == Aluno.id, Presenca.course_id == course).all()
    dictResult = [{'name': name, 'present': present} for name, present in result]
    return make_response(jsonify(dictResult), 201)

#generate hash for passwords
@app.route("/generate", methods=['POST'])
def generate_hash():
    pass_string = request.args.get('hash')
    i = generate_password_hash(pass_string)
    return make_response(jsonify({'hash': i}),201)




        