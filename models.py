"""Models
The Database models for the Journal App
"""


import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('journal.db',
                          pragmas={'foreign_keys': 1})


def slugify(string):
    """Takes a string and turns it into a valid slug"""

    slug = ""

    for character in string:
        regular_characters = "abcdejghijklmnopqrstuvwxyz0123456789_"

        if character.lower() in regular_characters:
            slug += character
        elif character.lower() in extended_characters:
            slug += extended_characters[character.lower()]
        else:  # fallback
            slug += '-'
    return slug

class User(UserMixin, Model):
    """The User, enables multiple people to privately use the same instance
    of Learning Journal"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        """Create a User and write it to the database."""
        with DATABASE.transaction():
            try:
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password)
                )
            except IntegrityError:
                raise ValueError("User already exists")


class JournalEntry(Model):
    """The main Model class for the application."""

    """In order to meet the specifications of the project for route
    names, titles are currently set to be unique. To make this application
    truly multi-user for production, we would change the routes so that
    the url for every journal entry would include the user's username so
    that multiple users could have journal entries with the same name,
    then we could remove the unique requirement for title"""
    title = CharField(unique=True)
    learning_date = DateTimeField()
    url_slug = CharField(unique=True)
    time_spent = IntegerField()  # minutes
    what_learned = TextField()
    resources = TextField()
    """Note that the syntax for initialising a ForeignKeyField has changed
    in peewee 3.0 (see the backwards incompatible section at:
    http://docs.peewee-orm.com/en/latest/peewee/changes.html)
    particularly:
    rel_model -> model
    related_name -> backref
    """
    user = ForeignKeyField(
        model=User,
        backref='journal_entries'
    )

    class Meta:
        database = DATABASE
        # `-` indicates descending order
        order_by = ('-learning_date',)

    @classmethod
    def create_journal_entry(cls, title, learning_date, time_spent,
                             what_learned, resources, user):

        # Create a unique slug
        prospective_slug = slugify(title)
        valid_slug = False
        slug_suffix = None
        while not valid_slug:
            if not slug_suffix:
                trying_slug = prospective_slug
            else:
                trying_slug = prospective_slug + str(slug_suffix)
            try:
                JournalEntry.get(JournalEntry.url_slug == trying_slug)
            except DoesNotExist:
                prospective_slug = trying_slug
                valid_slug = True
            else:  # slug already exists
                if not slug_suffix:
                    slug_suffix = 1
                else:
                    slug_suffix += 1

        with DATABASE.transaction():
            try:
                cls.create(
                    title=title,
                    learning_date=learning_date,
                    url_slug=prospective_slug,
                    time_spent=time_spent,
                    what_learned=what_learned,
                    resources=resources,
                    user=user
                )
            except IntegrityError:
                raise ValueError("Entry already exists")


class SubjectTag(Model):
    """Tags for particular subjects. Many-to-many with JournalEntry because
    multiple journal entries can have a particular tag, and a journal entry
    can have multiple tags.
    """
    name = CharField(unique=True)

    class Meta:
        database = DATABASE
        order_by = ('name',)


class JournalEntry_SubjectTag(Model):
    """Using peewee's built-in manytomany field is advised against by the
    author.
    See: http://docs.peewee-orm.com/en/latest/peewee/relationships.html
    """
    journal_entry = ForeignKeyField(
        model=JournalEntry,
        backref='journal_entry_subject_tags',
        on_delete='CASCADE'
    )
    subject_tag = ForeignKeyField(
        model=SubjectTag,
        backref='journal_entry_subject_tags',
        on_delete='CASCADE'
    )

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(
        [User, JournalEntry, SubjectTag, JournalEntry_SubjectTag],
        safe=True
    )
    DATABASE.close()