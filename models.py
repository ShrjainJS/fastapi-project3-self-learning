# This file helps SQL Alchemy to understand what kind of tables
# we will be creating in the Database. A database Model would be
# an actual record of inside a database table

# This import means that we are creating this model for our database file
from database import Base
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# The Todos takes in the Base created as Super Class - Base itself is a 'Base Class' for ORM to work the pythonic way
# Using this inheritence, when ever we declare attributes like Columns, Relationships,
# the 'declarative' system automatically takes care of generating 'Table' and 'Mapper' objects under the hood.


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column()

class Todos(Base):
    # This is just a way for SQLAlchemy to know what to name the table.
    __tablename__ = 'todos'

    # id = Column(Integer, primary_key=True, index=True)
    # title = Column(String)
    # description = Column(String)
    # priority = Column(Integer)
    # complete = Column(Boolean, default=False)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    priority: Mapped[int] = mapped_column()
    complete: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
