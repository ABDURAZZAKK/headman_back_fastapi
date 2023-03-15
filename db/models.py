from datetime import datetime
import sqlalchemy
from .base import metadata



# users_groups = sqlalchemy.Table(
#     'users_groups',
#     metadata,
#     sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key=True),
#     sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key=True)
# )


studstat_accs = sqlalchemy.Table(
    "studstat_accs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("lastname", sqlalchemy.String),
    sqlalchemy.Column("firstname", sqlalchemy.String),
    sqlalchemy.Column("patr", sqlalchemy.String),
    sqlalchemy.Column("nbook", sqlalchemy.Integer),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('users.id', ondelete='SET NULL')),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("studstat_acc_id", sqlalchemy.ForeignKey('studstat_accs.id', ondelete='CASCADE'), nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)

groups = sqlalchemy.Table(
    "groups",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("headman", sqlalchemy.ForeignKey('users.id', ondelete='CASCADE')),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)

categories = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("group_id",sqlalchemy.ForeignKey('groups.id', ondelete='CASCADE')),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)

homeworks = sqlalchemy.Table(
    "homeworks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("task", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("path_to_files", sqlalchemy.String),
    sqlalchemy.Column("category_id", sqlalchemy.ForeignKey('categories.id', ondelete='CASCADE')),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.utcnow)
)
