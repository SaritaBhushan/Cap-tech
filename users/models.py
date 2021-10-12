# users/models.py
# from django.db import models
from django.db.models.fields import CharField, TimeField, BooleanField, DateField, DateTimeField, DecimalField, TextField, EmailField, PositiveIntegerField, IntegerField
from django.db.models import Model, ForeignKey, OneToOneField, CASCADE

from django.utils.translation import ugettext_noop
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from datetime import datetime, timedelta
from pytz import UTC

class User_role(Model):
    role = CharField(unique=True, max_length=30, db_index=True, null=False)

    def __str__(self):
        return self.role

    class Meta(object):
        # unique = ('role',)
        ordering = ["role"]


class UserProfile(Model):
    """This is where we store all the user demographic fields. We have a
    separate table for this rather than extending the built-in Django auth_user.

    """
    # cache key format e.g user.<user_id>.profile.country = 'SG'
    PROFILE_COUNTRY_CACHE_KEY = u"user.{user_id}.profile.country"

    class Meta(object):
        # db_table = "auth_userprofile"
        unique_together = ('name', 'surname')
        ordering = ["name", "surname"]
        permissions = (("can_deactivate_users", "Can deactivate, but NOT delete users"),)

    # CRITICAL TODO/SECURITY
    # Sanitize all fields.
    # This is not visible to other users, but could introduce holes later
    user = OneToOneField(User, unique=True, db_index=True, related_name='profile',on_delete=CASCADE,)
    name = CharField(blank=True, max_length=255, db_index=True)
    surname = CharField(blank=True, max_length=255, db_index=True)
    role = ForeignKey(User_role, to_field='id', related_name='user_role',on_delete=CASCADE,)

    # Location is no longer used, but is held here for backwards compatibility
    # for users imported from our first class.
    language = CharField(blank=True, max_length=255, db_index=True)
    location = CharField(blank=True, max_length=255, db_index=True)

    # Optional demographic data we started capturing from Fall 2012
    this_year = datetime.now(UTC).year
    VALID_YEARS = range(this_year, this_year - 120, -1)
    year_of_birth = IntegerField(blank=True, null=True, db_index=True)
    GENDER_CHOICES = (
        ('m', ugettext_noop('Male')),
        ('f', ugettext_noop('Female')),
        # Translators: 'Other' refers to the student's gender
        ('o', ugettext_noop('Other/Prefer Not to Say'))
    )
    gender = CharField(
        blank=True, null=True, max_length=6, db_index=True, choices=GENDER_CHOICES
    )

    # [03/21/2013] removed these, but leaving comment since there'll still be
    # p_se and p_oth in the existing data in db.
    # ('p_se', 'Doctorate in science or engineering'),
    # ('p_oth', 'Doctorate in another field'),
    LEVEL_OF_EDUCATION_CHOICES = (
        ('p', ugettext_noop('Doctorate')),
        ('m', ugettext_noop("Master's or professional degree")),
        ('b', ugettext_noop("Bachelor's degree")),
        ('a', ugettext_noop("Associate degree")),
        ('hs', ugettext_noop("Secondary/high school")),
        ('jhs', ugettext_noop("Junior secondary/junior high/middle school")),
        ('el', ugettext_noop("Elementary/primary school")),
        # Translators: 'None' refers to the student's level of education
        ('none', ugettext_noop("No formal education")),
        # Translators: 'Other' refers to the student's level of education
        ('other', ugettext_noop("Other education"))
    )
    level_of_education = CharField(
        blank=True, null=True, max_length=6, db_index=True,
        choices=LEVEL_OF_EDUCATION_CHOICES
    )
    mailing_address = TextField(blank=True, null=True)
    city = TextField(blank=True, null=True)
    country = CountryField(blank=True, null=True)

    # Activation Status
    status = BooleanField(default=True)
    # Time Stamp information
    created = DateTimeField(auto_now=True)
    updated = DateTimeField(auto_now_add=True)


    @property
    def age(self):
        """ Convenience method that returns the age given a year_of_birth. """
        year_of_birth = self.year_of_birth
        year = datetime.now(UTC).year
        if year_of_birth is not None:
            return self._calculate_age(year, year_of_birth)

    @property
    def gender_display(self):
        """ Convenience method that returns the human readable gender. """
        if self.gender:
            return self.__enumerable_to_display(self.GENDER_CHOICES, self.gender)


    def set_login_session(self, session_id=None):
        """
        Sets the current session id for the logged-in user.
        If session_id doesn't match the existing session,
        deletes the old session object.
        """
        meta = self.get_meta()
        old_login = meta.get('session_id', None)
        if old_login:
            SessionStore(session_key=old_login).delete()
        meta['session_id'] = session_id
        self.set_meta(meta)
        self.save()

    def __enumerable_to_display(self, enumerables, enum_value):
        """ Get the human readable value from an enumerable list of key-value pairs. """
        return dict(enumerables)[enum_value]

    def _calculate_age(self, year, year_of_birth):
        """Calculate the youngest age for a user with a given year of birth.

        :param year: year
        :param year_of_birth: year of birth
        :return: youngest age a user could be for the given year
        """
        # There are legal implications regarding how we can contact users and what information we can make public
        # based on their age, so we must take the most conservative estimate.
        return year - year_of_birth - 1



def get_user_by_username_or_email(username_or_email):
    """
    Return a User object, looking up by email if username_or_email contains a
    '@', otherwise by username.

    Raises:
        User.DoesNotExist is lookup fails.
    """
    if '@' in username_or_email:
        return User.objects.get(email=username_or_email)
    else:
        return User.objects.get(username=username_or_email)


def get_user(email):
    user = User.objects.get(email=email)
    u_prof = UserProfile.objects.get(user=user)
    return user, u_prof


def user_info(email):
    user, u_prof = get_user(email)
    print("User id", user.id)
    print("Username", user.username)
    print("E-mail", user.email)
    print("Name", u_prof.name)
    print("Location", u_prof.location)
    print("Language", u_prof.language)
    return user, u_prof


def change_email(old_email, new_email):
    user = User.objects.get(email=old_email)
    user.email = new_email
    user.save()


def change_name(email, new_name):
    _user, u_prof = get_user(email)
    u_prof.name = new_name
    u_prof.save()

def user_count():
    print("All users", User.objects.all().count())
    print( "Active users", User.objects.filter(is_active=True).count())
    return User.objects.all().count()


def active_user_count():
    return User.objects.filter(is_active=True).count()

class User_login_status(Model):
    user = ForeignKey(User, to_field='id', related_name='user_login',on_delete=CASCADE,)
    status = BooleanField(default=True)
    login = DateTimeField(null=False, blank=False)
    logout = DateTimeField(null=False, blank=False)


PERMISSION_STATUS_DELETE = 0
PERMISSION_STATUS_CREATE = 1
PERMISSION_STATUS_UPDATE = 2
PERMISSION_STATUS_READ = 3

PERMISSION_LEVEL_CHOICES = (
    (PERMISSION_STATUS_DELETE, ugettext_noop('Delete')),
    (PERMISSION_STATUS_CREATE, ugettext_noop('Create')),
    (PERMISSION_STATUS_UPDATE, ugettext_noop('Update')),
    (PERMISSION_STATUS_READ, ugettext_noop('Read')),
)

class User_permission(Model):
    model = TextField(max_length=255, null=False)
    # permissionlevel=  PositiveIntegerField(default=0)
    permissionlevel = CharField(
        blank=True, null=True, max_length=1, db_index=True,
        choices=PERMISSION_LEVEL_CHOICES
        )
    user = ForeignKey(User, to_field='id', related_name='user_id',on_delete=CASCADE,)