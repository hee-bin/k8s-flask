from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from typesense import Client
import os

app = Flask(__name__)

# 환경변수 설정
DB_USER = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_NAME = os.environ.get('MYSQL_DB')
TYPESENSE_API_KEY = os.environ.get('TYPESENSE_API_KEY')

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Typesense 클라이언트 설정
typesense_client = Client({
    'nodes': [{
        'host': 'typesense.type-ns.svc.cluster.local',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': TYPESENSE_API_KEY,
    'connection_timeout_seconds': 2
})



class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50))
    title = db.Column(db.String(50))
    writer = db.Column(db.String(10))
    content = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String, nullable=True)  # 이미지 파일 경로를 문자열로 저장

    reviews = db.relationship('NoteReview', backref='note', lazy=True)

    def __repr__(self):
        return f'<Note {self.title}>'


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50))
    title = db.Column(db.String(50))
    writer = db.Column(db.String(10))
    content = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String, nullable=True)  # 이미지 파일 경로를 문자열로 저장

    reviews = db.relationship('JobReview', backref='job', lazy=True)

    def __repr__(self):
        return f'<Job {self.title}>'

 


@app.route('/search', methods=['GET'])
def search_all():
    query = request.args.get('query', '')
    results = {}

    # 노트 검색
    notes_search_results = typesense_client.collections['notes'].documents.search({
        'q': query,
        'query_by': 'title,content'
    })
    results['notes'] = [hit['document'] for hit in notes_search_results['hits']]

    # 직업 검색
    jobs_search_results = typesense_client.collections['jobs'].documents.search({
        'q': query,
        'query_by': 'title,content'
    })
    results['jobs'] = [hit['document'] for hit in jobs_search_results['hits']]

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)