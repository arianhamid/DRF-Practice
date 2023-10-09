from rest_framework import serializers
from watchlist_app.models import Movie

# validator for name field


def UppercaseValidator(value):
    print(value.islower())
    if value.islower():
        raise serializers.ValidationError('Name must be uppercase.')
    return value


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # Individual fields on a serializer can include validators, by declaring them on the field instance
    name = serializers.CharField(validators=[UppercaseValidator])
    description = serializers.CharField()
    published = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.published = validated_data.get(
            'published', instance.published)
        instance.save()
        return instance

# Field-level validation
    def validate_name(self, value):
        """
        Check that the movie name length is more than 3 characters.
        """
        if len(value) < 3:
            raise serializers.ValidationError("movie name is too short!!")
        return value

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    # Object-level validation
    def validate(self, data):
        """
        Check that the name and description fields are different.
        """
        if data['name'] == data['description']:
            raise serializers.ValidationError(
                "name and description fields must be different")
        return data
