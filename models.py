from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship




class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student = Column(String(55), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))
    
    teachers = relationship("Teacher", secondary="student_to_teacher", back_populates="students")
    subjects = relationship("Subject", secondary="student_to_subject", back_populates="students")
    
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, unique=True, nullable=False)
    
    students = relationship('Student')
    
    
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher = Column(String(55), nullable=False, unique=True)
    
    students = relationship("Student", secondary="student_to_teacher", back_populates="teachers")
    subjects = relationship("Subject", secondary="teacher_to_subject", back_populates="teachers")
  
    
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String, nullable=False, unique=True)
    
    teachers = relationship("Teacher", secondary="teacher_to_subject", back_populates="subjects")
    students = relationship("Student", secondary="student_to_subject", back_populates="subjects")

class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete='CASCADE', onupdate='CASCADE'))
    gread = Column(Integer)
    gread_date = Column(Date)


class StudentTeacher(Base):
    __tablename__ = 'student_to_teacher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Column = Column("teacher_id", Integer, ForeignKey("teachers.id", ondelete="CASCADE"))
    student_id: Column = Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"))
    
    
class TeacherSubject(Base):
    __tablename__ = 'teacher_to_subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Column = Column("teacher_id", Integer, ForeignKey("teachers.id", ondelete="CASCADE"))
    subject_id: Column = Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))


class StudentSubject(Base):
    __tablename__ = 'student_to_subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id: Column = Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"))
    subject_id: Column = Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"))