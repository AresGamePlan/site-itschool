from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# ---------------------------------------------------------------
# ⬇️ User
# ---------------------------------------------------------------

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    coins = db.Column(db.Integer, default=0)

    student = db.relationship('Student', back_populates='user', uselist=False)
    payrolls = db.relationship("Payroll", back_populates="user", cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")

    schedules = db.relationship("Schedule", back_populates="teacher", cascade="all, delete-orphan")

    def is_admin(self): return self.role == 'admin'
    def is_teacher(self): return self.role == 'teacher'
    def is_student(self): return self.role == 'student'
    def is_user(self): return self.role == "user"


# ---------------------------------------------------------------
# ⬇️ Many-to-Many таблицы
# ---------------------------------------------------------------

student_courses = db.Table(
    'students_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete="CASCADE")),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id', ondelete="CASCADE")),
)

student_groups = db.Table(
    'students_groups',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete="CASCADE")),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id', ondelete="CASCADE")),
)


# ---------------------------------------------------------------
# ⬇️ Student
# ---------------------------------------------------------------

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True)

    user = db.relationship('User', back_populates='student')

    groups = db.relationship(
        'Group',
        secondary=student_groups,
        back_populates='students',
        passive_deletes=True
    )

    courses = db.relationship(
        'Course',
        secondary=student_courses,
        back_populates='students',
        passive_deletes=True
    )


# ---------------------------------------------------------------
# ⬇️ Course
# ---------------------------------------------------------------

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    students = db.relationship(
        'Student',
        secondary=student_courses,
        back_populates='courses'
    )

    groups = db.relationship(
        'Group',
        back_populates='course',
        cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------
# ⬇️ Group (исправлено)
# ---------------------------------------------------------------

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="SET NULL"),
        nullable=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id', ondelete="CASCADE"),
        nullable=False
    )

    students = db.relationship(
        'Student',
        secondary=student_groups,
        back_populates='groups',
        passive_deletes=True
    )

    course = db.relationship('Course', back_populates='groups')
    teacher = db.relationship("User")

    schedule = db.relationship(
        "Schedule",
        back_populates="group",
        cascade="all, delete-orphan", 
        uselist=False
    )

    lessons = db.relationship(
        "Lesson",
        back_populates="group",
        cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------
# ⬇️ Lesson
# ---------------------------------------------------------------

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id', ondelete="CASCADE"),
        nullable=False
    )

    day_of_week = db.Column(db.String(50))
    time_of_lesson = db.Column(db.String(50))

    group = db.relationship("Group", back_populates="lessons")


# ---------------------------------------------------------------
# ⬇️ Order
# ---------------------------------------------------------------

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    count = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="orders")

    


# ---------------------------------------------------------------
# ⬇️ Payroll
# ---------------------------------------------------------------

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    id = db.Column(db.Integer, primary_key=True)
    amount_coins = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(250), nullable=False)

    user = db.relationship("User", back_populates="payrolls")


# ---------------------------------------------------------------
# ⬇️ Schedule
# ---------------------------------------------------------------

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)

    time_start = db.Column(db.Time)
    time_finish = db.Column(db.Time)

    monday = db.Column(db.Boolean, default=False)
    tuesday = db.Column(db.Boolean, default=False)
    wednesday = db.Column(db.Boolean, default=False)
    thursday = db.Column(db.Boolean, default=False)
    friday = db.Column(db.Boolean, default=False)
    saturday = db.Column(db.Boolean, default=False)
    sunday = db.Column(db.Boolean, default=False)

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="SET NULL")
    )

    group_id = db.Column(
        db.Integer,
        db.ForeignKey('groups.id', ondelete="CASCADE"),
        nullable=False
    )

    teacher = db.relationship("User", back_populates="schedules")
    group = db.relationship("Group", back_populates="schedule")
"""
1. Role +

2. Teacher убрали

3. Course +

4. Group

5. Student

6. Lesson

Темы для изучения:
flask_sqlalchemy, связи однин к многим, многие к многим
"""