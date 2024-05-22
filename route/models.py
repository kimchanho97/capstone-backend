from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(255), nullable=False, unique=True)
    nickname = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=False)

    tokens = db.relationship('Token', backref='User', uselist=False, lazy=True)
    projects = db.relationship('Project', backref='User', lazy=True)

    def __repr__(self):
        return f'<User {self.login}>'

class Token(db.Model):
    __tablename__ = 'Token'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True, nullable=False)
    access_token = db.Column(db.String(255), primary_key=True, nullable=False)

    def __repr__(self):
        return f'<Token {self.access_token}>'

class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    framework = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=0)
    auto_scaling = db.Column(db.Boolean, nullable=False, default=False)
    min_replicas = db.Column(db.Integer, nullable=True)
    max_replicas = db.Column(db.Integer, nullable=True)
    cpu_threshold = db.Column(db.Integer, nullable=True)
    domain_url = db.Column(db.String(255), nullable=True)
    webhook_url = db.Column(db.String(255), nullable=True)

    builds = db.relationship('Build', backref='Project', lazy=True, cascade='all, delete-orphan')
    deploys = db.relationship('Deploy', backref='Project', lazy=True, cascade='all, delete-orphan')
    secrets = db.relationship('Secret', backref='Project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'

class Build(db.Model):
    __tablename__ = 'Build'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), nullable=False)
    build_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    commit_msg = db.Column(db.String(255), nullable=False)
    image_name = db.Column(db.String(255), nullable=False)
    image_tag = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Build {self.id}>'

class Deploy(db.Model):
    __tablename__ = 'Deploy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), nullable=False)
    build_id = db.Column(db.Integer, db.ForeignKey('Build.id'), nullable=False)
    deploy_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Deploy {self.id}>'

class Secret(db.Model):
    __tablename__ = 'Secret'
    # project_id, key로 복합키 설정
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), primary_key=True, nullable=False)
    key = db.Column(db.String(255), primary_key=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Secret {self.key}>'

