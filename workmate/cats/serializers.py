from rest_framework import serializers
from .models import Cat, Breed, Rating


class CatSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cat
        fields = [
            'id', 'name', 'color', 'description', 'breed',
            'age_in_months', 'birth_date', 'average_rating'
        ]
        read_only_fields = ['author']

    def get_age_in_months(self, obj):
        return obj.age_in_months


class CatGetSerializer(CatSerializer):
    breed = serializers.StringRelatedField()


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'cat', 'user', 'score', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        cat = validated_data['cat']
        score = validated_data['score']

        rating, created = Rating.objects.update_or_create(
            cat=cat,
            user=user,
            defaults={'score': score}
        )
        return rating
