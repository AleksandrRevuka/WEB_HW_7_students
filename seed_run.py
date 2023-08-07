import click
from sqlalchemy import func

from  db import session
from models import (Student, 
                    Group, 
                    Subject, 
                    Teacher, 
                    TeacherSubject)


def make_list_teacher():
    result = session.query(Teacher.id, Teacher.teacher, Subject.subject_name) \
        .join(TeacherSubject, Teacher.id == TeacherSubject.teacher_id) \
        .join(Subject, Subject.id == TeacherSubject.subject_id)
        
    for id, teacher, subject_name in result:
        click.echo(f"Teacher ID: {id}, Teacher Name: {teacher}, Subject Name: {subject_name}")
    
    
def make_list_student():
    result = session.query(Student.id, Student.student, Group.group_name) \
        .join(Group, Student.group_id == Group.id)
        
    for id, student_name, group in result:
        click.echo(f"Student ID: {id}, Student Name: {student_name}, Group Name: {group}")
    
    
def make_list_subject():
    result = session.query(Subject.id, Subject.subject_name)
     
    for id, subject_name in result:
        click.echo(f"Subject ID: {id}, Subject Name: {subject_name}")
    

def make_list_group():
    result = session.query(Group.id, Group.group_name, func.count(Student.id).label("count_students")) \
        .join(Student, Student.group_id == Group.id) \
        .group_by(Group.id, Group.group_name)
        
    for id, group_name, count in result:
        click.echo(f"Group ID: {id}, Group Name: {group_name}, Count students: {count}")
    

def controller_command_list(model):
    if model == "Teacher":
        make_list_teacher()
    elif model == "Student":
        make_list_student()
    elif model == "Subject":
        make_list_subject()
    elif model == "Group":
        make_list_group()


@click.command()
@click.option('--action', '-a', type=click.Choice(['create', 'list', 'update', 'remove']), required=True,
              help='CRUD operation to perform: create, list, update, or remove.')
@click.option('--model', '-m', type=click.Choice(['Teacher', 'Student', 'Subject', 'Group']), required=True,
              help='The model on which the operation will be performed: Teacher, Student, or Subject.')
@click.option('--id', type=int, help='The ID of the model to perform update or remove operations.')
@click.option('--name', type=str, help='The name to be used in create or update operations.')
def main(action, model, id, name):

    if action == 'create':
        click.echo("Логіка для створення об'єкту моделі з заданими параметрами (назвою)")

    elif action == 'list':
        controller_command_list(model)

    elif action == 'update':
        click.echo("Логіка для оновлення об'єкту моделі з заданим id та новою назвою")

    elif action == 'remove':
        click.echo("Логіка для видалення об'єкту моделі з заданим id")

if __name__ == '__main__':
    main()