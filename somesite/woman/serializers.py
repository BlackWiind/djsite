from rest_framework import serializers

from woman.models import Woman


class WomanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Woman
        fields = ('title', 'cat_id')