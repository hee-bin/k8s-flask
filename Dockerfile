# 기본 이미지로 파이썬 3.10 슬림 버전 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app

# 환경변수 설정
ENV FLASK_APP=mysql_to_typesense.py

# Flask 서버 실행
CMD ["flask", "run", "--host=0.0.0.0"]
