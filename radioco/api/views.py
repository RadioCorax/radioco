import datetime

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.fields import IsoDateTimeField

from radioco.api import serializers
from radioco.programmes.models import Programme, Episode
from radioco.schedules.models import Slot, Schedule, Transmission


class ProgrammeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Programme.objects.all()
    serializer_class = serializers.ProgrammeSerializer
    lookup_field = 'slug'


class SlotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = serializers.SlotSerializer


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = serializers.EpisodeSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


class TransmissionForm(forms.Form):
    after = IsoDateTimeField(required=False)
    before = IsoDateTimeField(required=False)

    def clean_after(self):
        after = self.cleaned_data.get('after')
        if after is None:
            return timezone.now().replace(day=1)
        return after

    def clean_before(self):
        before = self.cleaned_data.get('before')
        if before is None:
            return self.clean_after() + datetime.timedelta(days=31)
        return before

    def clean(self):
        cleaned_data = super().clean()
        if self.clean_after() > self.clean_before():
            self.add_error('before', 'must be later than after')


class TransmissionViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.TransmissionSerializer

    def list(self, request):
        params = TransmissionForm(request.query_params)
        if not params.is_valid():
            raise ValidationError(params.errors)

        transmissions = Transmission.between(params.cleaned_data.get('after'),
                                             params.cleaned_data.get('before'))

        serializer = self.get_serializer(
            transmissions, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def now(self, request):
        _now = timezone.now()
        transmissions = Transmission.at(_now)
        serializer = self.get_serializer(
            transmissions, many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        pass
