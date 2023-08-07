from db import session
from sqlalchemy import text, distinct, func

from models import (Student, 
                    Group, 
                    Subject, 
                    Teacher, 
                    Journal, 
                    StudentTeacher, 
                    TeacherSubject,
                    StudentSubject)



def select_1():
    subquery = session.query(
        Journal.student_id,
        func.round(func.avg(Journal.gread), 4).label('average_grade')
    ).group_by(Journal.student_id).subquery()

    top_5_students = session.query(Student, subquery.c.average_grade).\
        join(subquery, Student.id == subquery.c.student_id).\
        order_by(subquery.c.average_grade.desc()).\
        limit(5).all()
        
    for student, average_grade in top_5_students:
        print(f"Student ID: {student.id}, Student: {student.student}, Average Grade: {average_grade}")
    
    
def select_2():
    result = session.query(Student.id, Student.student, func.round(func.avg(Journal.gread), 4).label('average_grade')) \
        .join(Journal, Student.id == Journal.student_id) \
        .join(Subject, Journal.subject_id == Subject.id) \
        .filter(Subject.subject_name == 'Computer Science') \
        .group_by(Student.id) \
        .order_by(func.avg(Journal.gread).desc()) \
        .limit(1) \
        .all()

    if result:
        student_id, student_name, average_grade = result[0]
    print(f"Student ID: {student_id}, Student Name: {student_name}, Average Grade: {average_grade}")
    

def select_3():
    result = session.query(Group.id, Group.group_name, func.round(func.avg(Journal.gread), 4).label("average_grade")) \
        .join(Student, Group.id == Student.group_id) \
        .join(Journal, Student.id == Journal.student_id) \
        .join(Subject, Journal.subject_id == Subject.id) \
        .filter(Subject.subject_name == "Psychology") \
        .group_by(Group.id)
        
    for id, group, average_grade in result:
        print(f"Group ID: {id}, Group Name: {group}, Average Grade: {average_grade}")


def select_4():
    with open("query_04.sql") as f:
        sql = f.read()
        query = text(sql)
        result = session.execute(query).all()
    print(result)
    
def select_5():
    result = session.query(Teacher.id, Teacher.teacher, Subject.subject_name) \
        .join(TeacherSubject, Teacher.id == TeacherSubject.teacher_id) \
        .join(Subject, Subject.id == TeacherSubject.subject_id) \
        .filter(Teacher.teacher == "Tammy Carey")

    for id, teacher, subject_name in result:
        print(f"Teacher ID: {id}, Teacher Name: {teacher}, Subject Name: {subject_name}")


def select_6():
    result = session.query(Student.id, Student.student) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.group_name == "LR-94")
        
    for id, student_name in result:
        print(f"Student ID: {id}, Student Name: {student_name}")
        
        
def select_7():
    result = session.query(Student.id, Student.student, Journal.gread) \
        .join(Journal, Student.id == Journal.student_id) \
        .join(Subject, Journal.subject_id == Subject.id) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Subject.subject_name == "History", Group.group_name == "TL-05")
        
    for id, student_name, gread in result:
        print(f"Student ID: {id}, Student Name: {student_name}, Gread: {gread}")
        

def select_8():
    result = session.query(func.round(func.avg(Journal.gread), 4).label('average_grade')) \
        .join(StudentTeacher, StudentTeacher.student_id == Journal.student_id) \
        .join(Teacher, Teacher.id == StudentTeacher.teacher_id) \
        .join(Student, StudentTeacher.student_id == Student.id) \
        .filter(Teacher.teacher == "James Watkins")
        
    for average_grade in result:
        print(f"Average grade: {average_grade[0]}")


def select_9():
    result = session.query(distinct(Subject.subject_name)) \
        .join(StudentSubject, Subject.id == StudentSubject.subject_id) \
        .join(Student, StudentSubject.student_id == Student.id) \
        .filter(Student.student == "Terry Juarez")
        
    for subject_name in result:
        print(f"Subject Name: {subject_name[0]}")


def select_10():
    result = session.query(Subject.subject_name) \
        .join(StudentSubject, StudentSubject.subject_id == Subject.id) \
        .join(Student, StudentSubject.student_id == Student.id) \
        .join(StudentTeacher, StudentTeacher.student_id == Student.id) \
        .join(Teacher, StudentTeacher.teacher_id == Teacher.id) \
        .filter(Teacher.teacher == "James Watkins", Student.student == "Richard Hunt")
        

    for subject_name in result:
        print(f"Subject Name: {subject_name[0]}")

if __name__ == "__main__":
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()