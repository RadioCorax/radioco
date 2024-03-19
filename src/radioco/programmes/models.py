# Radioco - Broadcasting Radio Recording Scheduling system.
# Copyright (C) 2014  Iago Veloso Abalo, Stefan Walluhn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ckeditor.fields import RichTextField

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


if hasattr(settings, 'PROGRAMME_LANGUAGES'):
    PROGRAMME_LANGUAGES = settings.PROGRAMME_LANGUAGES
else:
    PROGRAMME_LANGUAGES = settings.LANGUAGES

PRESENTER = 'PR'
INFORMER = 'IN'
CONTRIBUTOR = 'CO'
NOT_SPECIFIED = 'NO'

ROLES = (
    (NOT_SPECIFIED, _("Not specified")),
    (PRESENTER, _("Presenter")),
    (INFORMER, _("Informer")),
    (CONTRIBUTOR, _("Contributor"))
)


class Programme(models.Model):
    class Meta:
        verbose_name = _('programme')
        verbose_name_plural = _('programmes')
        permissions = (("see_all_programmes", "Can see all programmes"),)

    CATEGORY_CHOICES = (
        ('Arts', _('Arts')),
        ('Business', _('Business')),
        ('Comedy', _('Comedy')),
        ('Education', _('Education')),
        ('Games & Hobbies', _('Games & Hobbies')),
        ('Government & Organizations', _('Government & Organizations')),
        ('Health', _('Health')),
        ('Kids & Family', _('Kids & Family')),
        ('Music', _('Music')),
        ('News & Politics', _('News & Politics')),
        ('Religion & Spirituality', _('Religion & Spirituality')),
        ('Science & Medicine', _('Science & Medicine')),
        ('Society & Culture', _('Society & Culture')),
        ('Sports & Recreation', _('Sports & Recreation')),
        ('Technology', _('Technology')),
        ('TV & Film', _('TV & Film')),
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("name"),
        help_text=_(
            "Please DON'T change this value. It's used to build URL's."))
    announcers = models.ManyToManyField(
        User, blank=True, through='Role', verbose_name=_("announcers"))
    synopsis = RichTextField(blank=True, verbose_name=_("synopsis"))
    photo = models.ImageField(upload_to='photos/',
                              default='defaults/default-programme-photo.jpg',
                              verbose_name=_("photo"))
    language = models.CharField(default=PROGRAMME_LANGUAGES[0][0],
                                verbose_name=_("language"),
                                choices=PROGRAMME_LANGUAGES,
                                max_length=7)
    # XXX ensure not decreasing
    current_season = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("current season"))
    category = models.CharField(blank=True,
                                null=True,
                                max_length=50,
                                choices=CATEGORY_CHOICES,
                                verbose_name=_("category"))
    website = models.URLField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % (self.name)


class EpisodeManager(models.Manager):
    def create_episode(self, date, programme, last_episode=None, episode=None):
        if not last_episode:
            # may also be None
            last_episode = self.last(programme)

        season = programme.current_season
        if last_episode and last_episode.season == season:
            number_in_season = last_episode.number_in_season + 1
        else:
            number_in_season = 1

        if episode:
            episode.programme = programme
            episode.issue_date = date
            episode.season = season
            episode.number_in_season = number_in_season
        else:
            episode = Episode(programme=programme,
                              issue_date=date,
                              season=season,
                              number_in_season=number_in_season)

        with transaction.atomic():
            for role in Role.objects.filter(programme=programme):
                Participant.objects.create(person=role.person,
                                           episode=episode,
                                           role=role.role,
                                           description=role.description)
            episode.save()

        return episode

    def last(self, programme):
        episodes = Episode.objects.filter(programme=programme)
        return episodes.order_by("-season", "-number_in_season").first()

    def unfinished(self, programme, after=None):
        if not after:
            after = timezone.now()

        episodes = Episode.objects.filter(
            Q(programme=programme) &
            (Q(issue_date__gte=after) | Q(issue_date=None)))
        for episode in episodes.order_by("season", "number_in_season"):
            yield episode


class Episode(models.Model):
    class Meta:
        unique_together = (('season', 'number_in_season', 'programme'),)
        verbose_name = _('episode')
        verbose_name_plural = _('episodes')
        permissions = (("see_all_episodes", "Can see all episodes"),)

    objects = EpisodeManager()

    title = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("title"))
    people = models.ManyToManyField(
        User, blank=True, through='Participant', verbose_name=_("people"))
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, verbose_name=_("programme"))
    summary = RichTextField(blank=True, verbose_name=_("summary"))
    issue_date = models.DateTimeField(
        blank=True, null=True, db_index=True, verbose_name=_('issue date'))
    season = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("season"))
    number_in_season = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name=_("No. in season"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"{:d}x{:d} {:s}".format(self.season,
                                        self.number_in_season,
                                        self.title or self.programme.name)


class Participant(models.Model):
    person = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("person"))
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, verbose_name=_("episode"))
    role = models.CharField(default=NOT_SPECIFIED,
                            verbose_name=_("role"),
                            choices=ROLES,
                            max_length=2)
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        unique_together = ('person', 'episode', 'role')
        verbose_name = _('contributor')
        verbose_name_plural = _('contributors')
        permissions = (
            ("see_all_participants", "Can see all participants"),
        )

    def __unicode__(self):
        return str(self.episode) + ": " + self.person.username


class Role(models.Model):
    person = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("person"))
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, verbose_name=_("programme"))
    role = models.CharField(default=NOT_SPECIFIED,
                            verbose_name=_("role"),
                            choices=ROLES,
                            max_length=2)
    description = models.TextField(blank=True, verbose_name=_("description"))
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('person', 'programme', 'role')
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        permissions = (
            ("see_all_roles", "Can see all roles"),
        )

    def __unicode__(self):
        return self.programme.name + ": " + self.person.username


class Podcast(models.Model):
    episode = models.OneToOneField(Episode,
                                   on_delete=models.CASCADE,
                                   primary_key=True,
                                   related_name='podcast')
    url = models.CharField(max_length=2048)
    mime_type = models.CharField(max_length=20)
    length = models.PositiveIntegerField()  # bytes
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def get_absolute_url(self):
        return self.episode.get_absolute_url()
