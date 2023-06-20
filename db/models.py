from datetime import datetime
import sqlalchemy as sa



metadata = sa.MetaData()


studstat_accs = sa.Table(
    "studstat_accs",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("lastname", sa.String),
    sa.Column("firstname", sa.String),
    sa.Column("patr", sa.String),
    sa.Column("nbook", sa.Integer),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="SET NULL"),
    ),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime, default=datetime.utcnow),
)


users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("email", sa.String, unique=True),
    sa.Column("name", sa.String),
    sa.Column("hashed_password", sa.String),
    # sa.Column(
    #     "studstat_acc_id",
    #     sa.Integer,
    #     sa.ForeignKey("studstat_accs.id", ondelete="CASCADE"),
    #     nullable=True,
    # ),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime, default=datetime.utcnow),
)


groups = sa.Table(
    "groups",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("name", sa.String),
    sa.Column("creater", sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime, default=datetime.utcnow),
)


categories = sa.Table(
    "categories",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("name", sa.String),
    sa.Column("group_id", sa.ForeignKey("groups.id", ondelete="CASCADE")),
    sa.Column("creater", sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime, default=datetime.utcnow),
)


homeworks = sa.Table(
    "homeworks",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, unique=True),
    sa.Column("task", sa.String),
    sa.Column("status", sa.String),
    sa.Column("path_to_files", sa.String, nullable=True),
    sa.Column("category_id", sa.ForeignKey("categories.id", ondelete="CASCADE")),
    sa.Column("creater", sa.ForeignKey("users.id", ondelete="CASCADE")),
    sa.Column("created_at", sa.DateTime),
    sa.Column("updated_at", sa.DateTime, default=datetime.utcnow),
)
