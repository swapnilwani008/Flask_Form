from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    college = db.Column(db.String(50))

    def __init__(self, name, college):
        self.name = name
        self.college = college

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        college = request.form['college']
        student = Student(name=name, college=college)
        db.session.add(student)
        db.session.commit()

    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get(student_id)
    return render_template('student.html', student=student)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
