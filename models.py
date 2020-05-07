import datetime
import regex as re


from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *
from flask_peewee.utils import slugify


DATABASE = SqliteDatabase("journal.db")


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ("-joined_at",)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin,
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref="entries")
    content = TextField()
    title = TextField()
    slug = CharField()
    time_spent = IntegerField()
    resources = TextField()
    tags = CharField(default="")

    def create_and_add_tags(self, tags):
        with DATABASE.transaction():
            for tag in tags:
                try:
                    tag.save(force_insert=True)
                except IntegrityError:
                    pass
            self.tags.add(tags)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub("[^\w]+", "-", self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)

        return ret

    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)


class Tag(Model):
    name = CharField(max_length=50, primary_key=True)
    entry = ManyToManyField(Entry, backref="tags")
    slug = CharField()

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return "<Tag %s>" % self.name

    def __str__(self):
        return self.name

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, Tag.entry.get_through_model()], safe=True)
    DATABASE.close()
