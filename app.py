# app.py
from flask import Flask, request, jsonify
from db import *  # Import the add_student function

app = Flask(__name__)
#
conn = get_db_connection()
cur = conn.cursor()

@app.route('/add_student', methods=['POST'])
def add_student_route():
    data = request.json
    student_name = data.get('student_name')
    id = data.get('id')
    print(id)


    if not student_name:
        return jsonify({'error': 'Student name is required'}), 400

    student_id = add_student(student_name,id)  # Call to add the student
    return jsonify({'message': 'Student added successfully', 'id': student_id}), 201


@app.route('/add_subject', methods=['POST'])
def add_subject_route():
    data = request.json
    subject_name = data.get('subjectname')
    print(subject_name)

    if not subject_name:
        return jsonify({'error': 'subject name is required'}), 400

    subject_id = add_subject(subject_name)  # Call to add the student
    return jsonify({'message': 'subject added successfully', 'id': subject_id}), 201


@app.route('/get_student_marks', methods=['GET'])
def get_student_marks():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.json
    student_name = data.get('student_name')
    subject_name = data.get('subject_name')

    if not student_name:
        return jsonify({'error': 'student_name is required'}), 400

    # SQL query to fetch marks for the student
    if subject_name:
        # If subject_name is provided, fetch marks for that specific subject
        query = '''
            SELECT 
                marks.id AS marks_id,
                students.student_name,
                subjects.subjectname,
                marks.marks
            FROM 
                marks
            JOIN 
                students ON marks.studentid = students.id
            JOIN 
                subjects ON marks.subjectid = subjects.subjectid
            WHERE 
                students.student_name = %s AND subjects.subjectname = %s
        '''
        cur.execute(query, (student_name, subject_name))
    else:
        # If subject_name is not provided, fetch all marks for the student
        query = '''
            SELECT 
                marks.id AS marks_id,
                students.student_name,
                subjects.subjectname,
                marks.marks
            FROM 
                marks
            JOIN 
                students ON marks.studentid = students.id
            JOIN 
                subjects ON marks.subjectid = subjects.subjectid
            WHERE 
                students.student_name = %s
        '''
        cur.execute(query, (student_name,))

    results = cur.fetchall()
    print(results)

    # Check if results are empty
    if not results:
        return jsonify({'error': 'No marks found for this student'}), 404

    # Transforming results into a more readable format
    marks_list = [
        {
            'student_name': row[1],
            'subject_name': row[2],
            'marks': float(row[3])
        }
        for row in results
    ]

    return jsonify(marks_list), 200


@app.route('/add_marks', methods=['POST'])
def add_marks():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.json
    student_name = data.get('student_name')
    subject_name = data.get('subject_name')
    marks = data.get('marks')

    if not student_name or not subject_name or marks is None:
        return jsonify({'error': 'student_name, subject_name, and marks are required'}), 400

    # Fetch student ID
    cur.execute("SELECT id FROM students WHERE student_name = %s", (student_name,))
    student = cur.fetchone()
    print(student)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    student_id = student[0]

    # Fetch subject ID
    cur.execute("SELECT subjectid FROM subjects WHERE subjectname = %s", (subject_name,))
    subject = cur.fetchone()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    subject_id = subject[0]

    # Insert marks into the marks table
    try:
        cur.execute("INSERT INTO marks (studentid, subjectid, marks) VALUES (%s, %s, %s)",
                    (student_id, subject_id, marks))
        conn.commit()  # Commit the transaction
        return jsonify({'message': 'Marks added successfully'}), 201
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500


@app.route('/get_students', methods=['GET'])
def get_students():
    try:
        # Execute the SQL query to fetch all student names
        cur.execute("SELECT student_name FROM students;")
        results = cur.fetchall()

        # Extracting student names from the results
        student_names = [row[0] for row in results]

        # Return the list of student names as a JSON response
        return jsonify(student_names), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_subject', methods=['GET'])
def get_subject():
    try:
        # Execute the SQL query to fetch all student names
        cur.execute("SELECT subjectname FROM subjects;")
        results = cur.fetchall()

        # Extracting student names from the results
        student_names = [row[0] for row in results]

        # Return the list of student names as a JSON response
        return jsonify(student_names), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500









if __name__ == '__main__':
    app.run(debug=True)