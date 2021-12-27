import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UsersUserModel(AbstractUser):
    """Default user for Hafenmeister."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # We will use the email address for user identification and do not require a username
    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True)

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """Return the name for the user."""
        return self.name

    def get_short_name(self):
        """Return the name for the user."""
        return self.name

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
