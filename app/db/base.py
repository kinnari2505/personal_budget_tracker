'''
What does Base = declarative_base() do

It creates a special class called Base.
Any model class that inherits from Base automatically becomes a SQLAlchemy ORM mapped class.
SQLAlchemy uses this base to:
Keep track of all models
Map classes to database tables
Generate metadata (Base.metadata) used to create tables
'''

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()