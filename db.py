# db.py
import psycopg


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg.connect(
        dbname='postgres',  # You can also try leaving this out
        password='Cizu@18',  # Password only
        host='localhost',
        port='5432'
    )
    return conn


def add_student(student_name,student_id=None):
    """Adds a student to the database and returns the student ID."""
    conn = get_db_connection()
    cur = conn.cursor()

    if student_id is None:  # Adding a new student
        cur.execute('INSERT INTO students (student_name) VALUES (%s) RETURNING id', (student_name,))
        new_student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_student_id
    else:  # Updating an existing student
        cur.execute('INSERT INTO students (id, student_name) VALUES (%s, %s)', (student_id, student_name))
        conn.commit()
        cur.close()
        conn.close()
        return student_id


def add_subject(subject_name):
    """Adds a student to the database and returns the student ID."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('INSERT INTO subjects (subjectname) VALUES (%s) RETURNING subjectid', (subject_name,))
    subject_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return subject_id
