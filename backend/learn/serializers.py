from rest_framework import serializers
from learn.models import Block


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'name', 'order')
