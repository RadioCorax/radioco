import datetime

from pytz.exceptions import NonExistentTimeError
from recurrence import Recurrence
from recurrence.fields import RecurrenceField

from django.utils import timezone


"""
Wrappers to deal with various date/time issues in origin Recurrence
implementation.
 """


class RecurrenceFieldWrapper(RecurrenceField):
    def to_python(self, value):
        recurrence = super(RecurrenceFieldWrapper, self).to_python(value)
        return RecurrenceWrapper(recurrence)


class RecurrenceWrapper(Recurrence):
    def __init__(self, recurrence):
        # hacky workaround, remove after upstream bug is solved
        # https://github.com/django-recurrence/django-recurrence/issues/94
        def fix_date(rdate):
            return datetime.datetime.combine(
                rdate,
                datetime.time(recurrence.dtstart.hour,
                              recurrence.dtstart.minute,
                              recurrence.dtstart.second,
                              recurrence.dtstart.microsecond,
                              recurrence.dtstart.tzinfo))

        rdates = [fix_date(dt) for dt in recurrence.rdates]
        exdates = [fix_date(dt) for dt in recurrence.exdates]

        dtstart = recurrence.dtstart
        if dtstart and timezone.is_aware(dtstart):
            dtstart = timezone.make_naive(dtstart)

        super(RecurrenceWrapper, self).__init__(
            dtstart=dtstart,
            dtend=recurrence.dtend,
            rrules=recurrence.rrules,
            exrules=recurrence.exrules,
            rdates=rdates,
            exdates=exdates,
            include_dtstart=recurrence.include_dtstart)

    def before(self, dt, **kwargs):
        if timezone.is_aware(dt):
            dt = timezone.make_naive(dt)

        _dt = super(RecurrenceWrapper, self).before(dt, **kwargs)
        if _dt:
            return timezone.make_aware(_dt)
        return None


    def after(self, dt, **kwargs):
        if timezone.is_aware(dt):
            dt = timezone.make_naive(dt)

        _dt = super(RecurrenceWrapper, self).after(dt, **kwargs)
        if _dt:
            return timezone.make_aware(_dt)
        return None


    def between(self, after, before, **kwargs):
        if timezone.is_aware(after):
            after = timezone.make_naive(after)

        if timezone.is_aware(before):
            before = timezone.make_naive(before)

        for dt in super(
                RecurrenceWrapper, self).between(after, before, **kwargs):
            try:
                yield timezone.make_aware(dt)
            except NonExistentTimeError:
                pass
