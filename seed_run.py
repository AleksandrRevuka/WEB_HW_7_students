import click
from sqlalchemy import func

from db import session
from models import Student, Group, Subject, Teacher, TeacherSubject


def make_list_teacher() -> None:
    result = (
        session.query(Teacher.id, Teacher.teacher, Subject.subject_name)
        .join(TeacherSubject, Teacher.id == TeacherSubject.teacher_id)
        .join(Subject, Subject.id == TeacherSubject.subject_id)
    )

    for id, teacher, subject_name in result:
        click.echo(
            f"Teacher ID: {id}, Teacher Name: {teacher}, Subject Name: {subject_name}"
        )


def make_list_student() -> None:
    result = session.query(Student.id, Student.student, Group.group_name).join(
        Group, Student.group_id == Group.id
    )

    for id, student_name, group in result:
        click.echo(
            f"Student ID: {id}, Student Name: {student_name}, Group Name: {group}"
        )


def make_list_subject() -> None:
    result = session.query(Subject.id, Subject.subject_name)

    for id, subject_name in result:
        click.echo(f"Subject ID: {id}, Subject Name: {subject_name}")


def make_list_group() -> None:
    result = (
        session.query(
            Group.id, Group.group_name, func.count(Student.id).label("count_students")
        )
        .join(Student, Student.group_id == Group.id)
        .group_by(Group.id, Group.group_name)
    )

    for id, group_name, count in result:
        click.echo(f"Group ID: {id}, Group Name: {group_name}, Count students: {count}")


def controller_command_list(model) -> None:
    if model == "Teacher":
        make_list_teacher()
    elif model == "Student":
        make_list_student()
    elif model == "Subject":
        make_list_subject()
    elif model == "Group":
        make_list_group()


def remove_field(model, id: int, message: str) -> None:
    result = session.query(model).filter_by(id=id).first()
    if result:
        session.delete(result)
        session.commit()
        click.echo(f"{message} ID {id} has been removed from the database.")
    else:
        click.echo(f"{message} ID {id} not found.")


def controller_command_remove(model, id: int) -> None:
    if model == "Teacher":
        message = "Teacher with"
        remove_field(Teacher, id, message)

    elif model == "Student":
        message = "Student with"
        remove_field(Student, id, message)

    elif model == "Subject":
        message = "Subject with"
        remove_field(Subject, id, message)

    elif model == "Group":
        message = "Group with"
        remove_field(Group, id, message)


def create_object(model, name_object: str, message: str, field: str) -> None:
    if field == "teacher":
        new_object = model(teacher=name_object)

    elif field == "student":
        new_object = model(student=name_object)

    elif field == "subject_name":
        new_object = model(subject_name=name_object)

    elif field == "group_name":
        new_object = model(group_name=name_object)

    if new_object:
        session.add(new_object)
        session.commit()
        click.echo(f"{message} name {name_object} has been created from the database.")
    else:
        click.echo(f"{message} name {name_object} not create.")


def controller_command_create(model, name: str) -> None:
    if model == "Teacher":
        message = "Teacher with"
        create_object(Teacher, name, message, field="teacher")

    elif model == "Student":
        message = "Student with"
        create_object(Student, name, message, field="student")

    elif model == "Subject":
        message = "Subject with"
        create_object(Subject, name, message, field="subject_name")

    elif model == "Group":
        message = "Group with"
        create_object(Group, name, message, field="group_name")


def update_object(
    model, object_id: int, new_name_object: str, message: str, field: str
) -> None:
    new_object = session.query(model).filter_by(id=object_id).first()

    if new_object:
        if field == "teacher":
            new_object.teacher = new_name_object

        elif field == "student":
            new_object.student = new_name_object

        elif field == "subject_name":
            new_object.subject_name = new_name_object

        elif field == "group_name":
            new_object.group_name = new_name_object

        session.commit()
        click.echo(
            f"{message} name {new_name_object} has been updated from the database."
        )
    else:
        click.echo(f"{message} ID {object_id} not found.")


def controller_command_update(model: str, id: int, name: str) -> None:
    if model == "Teacher":
        message = "Teacher with"
        update_object(Teacher, id, name, message, field="teacher")

    elif model == "Student":
        message = "Student with"
        update_object(Student, id, name, message, field="student")

    elif model == "Subject":
        message = "Subject with"
        update_object(Subject, id, name, message, field="subject_name")

    elif model == "Group":
        message = "Group with"
        update_object(Group, id, name, message, field="group_name")


@click.command()
@click.option(
    "--action",
    "-a",
    type=click.Choice(["create", "list", "update", "remove"]),
    required=True,
    help="CRUD operation to perform: create, list, update, or remove.",
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(["Teacher", "Student", "Subject", "Group"]),
    required=True,
    help="The model on which the operation will be performed: Teacher, Student, or Subject.",
)
@click.option(
    "--id", type=int, help="The ID of the model to perform update or remove operations."
)
@click.option(
    "--name", type=str, help="The name to be used in create or update operations."
)
def main(action, model, id, name):
    if action == "create":
        controller_command_create(model, name)

    elif action == "list":
        controller_command_list(model)

    elif action == "update":
        controller_command_update(model, id, name)

    elif action == "remove":
        controller_command_remove(model, id)


if __name__ == "__main__":
    main()
