from django.db import transaction

from radioco.programmes.models import Episode
from radioco.schedules.models import Schedule


def available_dates(programme, after):
    schedules = Schedule.objects.filter(
        slot__programme=programme, type=Schedule.LIVE)

    while True:
        candidates = filter(
            lambda c: c is not None,
            map(lambda s: s.date_after(after, inc=False), schedules))
        try:
            candidate = min(candidates)
        except ValueError:
            break

        # XXX there may be two or more parallel slots
        #       for dates in filter(lambda c: c == candidate, candidates):
        #       yield dates
        yield candidate
        after = candidate


def rearrange_episodes(programme, after):
    episodes = Episode.objects.unfinished(programme, after)
    dates = available_dates(programme, after)

    with transaction.atomic():
        # Further dates and episodes available -> re-order
        while True:
            try:
                date = next(dates)
                episode = next(episodes)
            except StopIteration:
                break

            episode.issue_date = date
            episode.save()

        # No further dates available -> unschedule
        while True:
            try:
                episode = next(episodes)
            except StopIteration:
                break

            episode.issue_date = None
            episode.save()
