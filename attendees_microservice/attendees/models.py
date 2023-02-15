from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse


class AccountVO(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)


class ConferenceVO(models.Model):
    import_href = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)


class Attendee(models.Model):
    """
    The Attendee model represents someone that wants to attend
    a conference
    """

    email = models.EmailField()
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    conference = models.ForeignKey(
        ConferenceVO,
        related_name="attendees",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def create_badge(self):
        try:
            self.badge
        except ObjectDoesNotExist:
            Badge.objects.create(attendee=self)

    def get_api_url(self):
        return reverse("api_show_attendee", kwargs={"pk": self.pk})


class Badge(models.Model):
    """
    The Badge model represents the badge an attendee gets to
    wear at the conference.

    Badge is a Value Object and, therefore, does not have a
    direct URL to view it.
    """

    created = models.DateTimeField(auto_now_add=True)

    attendee = models.OneToOneField(
        Attendee,
        related_name="badge",
        on_delete=models.CASCADE,
        primary_key=True,
    )
