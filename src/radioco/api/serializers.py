from radioco.programmes.models import Programme, Episode
from radioco.schedules.models import Slot, Schedule
from rest_framework import serializers


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:programme-detail', lookup_field='slug')

    class Meta:
        model = Programme
        fields = ('name', 'synopsis', 'photo', 'language', 'website',
                  'category', 'created_at', 'updated_at', 'url')


class SlotSerializer(serializers.HyperlinkedModelSerializer):
    programme = serializers.HyperlinkedRelatedField(
        view_name='api:programme-detail', lookup_field='slug', read_only=True)
    name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api:slot-detail')

    class Meta:
        model = Slot
        fields = ('programme', 'name', 'runtime', 'url')

    def get_name(self, slot):
        return str(slot)


class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    programme = serializers.HyperlinkedRelatedField(
        view_name='api:programme-detail', lookup_field='slug', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:episode-detail')

    class Meta:
        model = Episode
        fields = ('programme', 'title', 'summary', 'issue_date', 'season',
                  'number_in_season', 'created_at', 'updated_at', 'url')


class ScheduleSerializer(serializers.ModelSerializer):
    slot = serializers.HyperlinkedRelatedField(
        view_name='api:slot-detail',
        queryset=Slot.objects.all(),
        required=False)
    title = serializers.SerializerMethodField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'title', 'slot', 'start', 'end', 'type', 'source')

    def get_title(self, schedule):
        return schedule.slot.programme.name


class TransmissionSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    type = serializers.CharField(max_length=1)
    programme = ProgrammeSerializer()
    episode = EpisodeSerializer()
    schedule = serializers.PrimaryKeyRelatedField(read_only=True)
