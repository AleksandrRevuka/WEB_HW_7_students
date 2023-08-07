from string import ascii_uppercase

import faker
from random import randint, choice
from db import session
from models import (Student, 
                    Group, 
                    Subject, 
                    Teacher, 
                    Journal, 
                    StudentTeacher, 
                    TeacherSubject,
                    StudentSubject)

NUMBER_STUDENTS = 50
NUMBER_GROUP = 3
NUMBER_SUBJECT = 8
NUMBER_TEACHER = 5
NUMBER_GREADS = 20
SUBJECTS = [
    "Mathematics",
    "Biology",
    "History",
    "Chemistry",
    "Physics",
    "Literature",
    "Computer Science",
    "Psychology",
]

GREADS = [1, 2, 3, 4, 5]
PROBABILITIES = [1, 5, 15, 45, 34]


def get_random_gread():
    rand_num = randint(1, 100)
    cumulative_prob = 0
    for i, prob in enumerate(PROBABILITIES):
        cumulative_prob += prob
        if rand_num <= cumulative_prob:
            return GREADS[i]
        

def generate_fake_data(number_students, 
                       number_groups, 
                       number_subjects, 
                       number_teachers, 
                       number_greads):

    fake_data = faker.Faker()

    generated_names = set()
    
    for _ in range(number_groups):
        group = fake_data.bothify(text="??-##", letters=ascii_uppercase)
        group_obj = Group(group_name=group)
        session.add(group_obj)
        
    session.commit()

    for _ in range(number_students):
        student_name = fake_data.name()
        while student_name in generated_names:
            student_name = fake_data.name()
        generated_names.add(student_name)
        id = randint(1, number_groups)
        student_obj = Student(student=student_name, group_id=id)
        session.add(student_obj)

    session.commit()
    
    for subject in SUBJECTS:
        subject_obj = Subject(subject_name=subject)
        session.add(subject_obj)
        
    session.commit()

    for _ in range(number_teachers):
        teacher_obj = Teacher(teacher=fake_data.name())
        session.add(teacher_obj)
        
    session.commit()
    
    
    students = session.query(Student).all()
    teachers = session.query(Teacher).all()
    subjects = session.query(Subject).all()
    
    for student in students:
        used_subject_ids = set()
        for _ in range(1, 3):
            while True:
                subject = choice(subjects)
                if subject.id not in used_subject_ids:
                    break
            
            used_subject_ids.add(subject.id)
            
            student_subject_obj = StudentSubject(
                student_id=student.id,
                subject_id=subject.id
            )
            session.add(student_subject_obj)
    
    session.commit()
    
    students_subjects = session.query(StudentSubject).all()
    
    for student_subject in students_subjects:

        for _ in range(randint(1, number_greads + 1)):

            journal_obj = Journal(
                student_id=student_subject.student_id,
                subject_id=student_subject.subject_id,
                gread=get_random_gread(),
                gread_date=fake_data.date_this_year())
            
            session.add(journal_obj)
                
    session.commit()
    
    for teacher in teachers:
        used_subject_ids = set()
        teacher_group_id = randint(1, number_groups)
        for _ in range(randint(1, 3)):
            while True:
                subject = choice(subjects)
                if subject.id not in used_subject_ids:
                    break
            
            used_subject_ids.add(subject.id)
            
            teacher_subject_obj = TeacherSubject(
                teacher_id=teacher.id,
                subject_id=subject.id,
                group_id=teacher_group_id
            )
            session.add(teacher_subject_obj)
    
    session.commit()
    
    students = session.query(Student).all()
    teacher_subjects = session.query(TeacherSubject).all()
    student_subjects = session.query(StudentSubject).all()

    student_group_mapping = {student.id: student.group_id for student in students}

    for student_subject in student_subjects:
        student_id = student_subject.student_id
        subject_id = student_subject.subject_id
        group_id = student_group_mapping.get(student_id)

        for teacher_subject in teacher_subjects:
            if group_id == teacher_subject.group_id and subject_id == teacher_subject.subject_id:
                teacher_id = teacher_subject.teacher_id
                student_teacher_obj = StudentTeacher(
                    student_id=student_id,
                    teacher_id=teacher_id
                )
                session.add(student_teacher_obj)

    session.commit()


if __name__ == "__main__":
    generate_fake_data(
        NUMBER_STUDENTS, NUMBER_GROUP, NUMBER_SUBJECT, NUMBER_TEACHER, NUMBER_GREADS
    )

