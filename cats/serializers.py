from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = (
            'id',
            'name',
        )


class CatSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField(
    #     read_only=True,
    # )
    achievements = AchievementSerializer(
        # read_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'color',
            'birth_year',
            'owner',
            'achievements',
        )

    def create(self, validated_data: dict):
        # Уберем спосок достижений из словаря validated_data и сохраним его
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat

        achievements = validated_data.pop('achievements')

        # создание нового котика
        cat = Cat.objects.create(**validated_data)

        # для каждого достижения
        for achievment in achievements:
            # создание новой записи или полчение существующего экземляра из базы данных
            current_achievment, status = Achievement.objects.get_or_create(
                **achievment)
            # Ссылка на каждое достижение во всппомогательную таблицу с указанием
            # к каком котику она относится
            AchievementCat.objects.create(
                achievement=current_achievment,
                cat=cat
            )

        return cat


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Owner
        fields = (
            'first_name',
            'last_name',
            'cats',
        )
