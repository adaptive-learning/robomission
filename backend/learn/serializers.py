from rest_framework import serializers
from learn.models import Block


class BlockSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_blank=False, max_length=256)
    order = serializers.IntegerField(min_value=0, max_value=10000)

    def create(self, validated_data):
        """Create and return a new `Block` instance, given the validated data.
        """
        return Block.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing `Block` instance, given the validated data.
        """
        instance.title = validated_data.get('name', instance.name)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
