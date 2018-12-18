from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_cors import CORS

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/2018-12-12ad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship('Student', backref='team', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.String(10), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.name'))
    github = db.Column(db.String(100))
    rfid = db.Column(db.String(100))
    lab_section = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    lab_attendances = db.relationship('LabAttendance', backref='student', lazy=True)
    sprint_checks = db.relationship('SprintCheck', backref='student', lazy=True)
    knowledge_area_masteries = db.relationship('KnowledgeAreaMastery', backref='student', lazy=True)
    guided_practices = db.relationship('GuidedPractice', backref='student', lazy=True)
    team_evaluations_given = db.relationship('TeamEvaluation', backref='evaluator', lazy='dynamic', foreign_keys='TeamEvaluation.evaluator_id')
    team_evaluations_received = db.relationship('TeamEvaluation', backref='evaluatee', lazy='dynamic', foreign_keys='TeamEvaluation.evaluatee_id')

class LabAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    attended = db.Column(db.Boolean)

class SprintCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(10000), nullable=False)

class GuidedPractice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(100), nullable=False)

class TeamEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    evaluatee_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    sprint_number = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)

class KnowledgeAreaMastery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.comp_id'), nullable=False)
    comment = db.Column(db.String(100))
    completed = db.Column(db.Boolean)



db.create_all()
manager = APIManager(flask_sqlalchemy_db=db)

manager.create_api(Team, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)
manager.create_api(Team, methods=['DELETE'], url_prefix='/remove')
manager.create_api(Team, methods=['POST'], url_prefix='/create')
manager.create_api(Team, methods=['GET'], url_prefix='/get')

manager.create_api(SprintCheck, methods=['POST'], url_prefix='/create')
manager.create_api(SprintCheck, methods=['GET'], url_prefix='/get')
manager.create_api(SprintCheck, methods=['DELETE'], url_prefix='/remove')
manager.create_api(SprintCheck, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)

manager.create_api(KnowledgeAreaMastery, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)
manager.create_api(KnowledgeAreaMastery, methods=['DELETE'], url_prefix='/remove')
manager.create_api(KnowledgeAreaMastery, methods=['POST'], url_prefix='/create')
manager.create_api(KnowledgeAreaMastery, methods=['GET'], url_prefix='/get')

manager.create_api(Student, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)
manager.create_api(Student, methods=['DELETE'], url_prefix='/remove')
manager.create_api(Student, methods=['POST'], url_prefix='/create')
manager.create_api(Student, methods=['GET'], url_prefix='/get')

manager.create_api(LabAttendance, methods=['POST'], url_prefix='/create')
manager.create_api(LabAttendance, methods=['GET'], url_prefix='/get')
manager.create_api(LabAttendance, methods=['DELETE'], url_prefix='/remove')
manager.create_api(LabAttendance, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)

manager.create_api(GuidedPractice, methods=['POST'], url_prefix='/create')
manager.create_api(GuidedPractice, methods=['GET'], url_prefix='/get')
manager.create_api(GuidedPractice, methods=['DELETE'], url_prefix='/remove')
manager.create_api(GuidedPractice, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)

manager.create_api(TeamEvaluation, methods=['POST'], url_prefix='/create')
manager.create_api(TeamEvaluation, methods=['GET'], url_prefix='/get')
manager.create_api(TeamEvaluation, methods=['DELETE'], url_prefix='/remove')
manager.create_api(TeamEvaluation, methods=['PATCH'], url_prefix='/update', allow_patch_many=True)

manager.init_app(app)

app.run()
