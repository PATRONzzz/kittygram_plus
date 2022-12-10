import datetime as dt

import webcolors
from rest_framework import serializers

from .models import CHOICES, Achievement, AchievementCat, Cat, Owner


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как
    # есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название

    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код
            # в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError(
                'Для этого цвета нет имени'
            )
        # Возвращаем данные в новом формате
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = (
            'id',
            'achievement_name',
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
    age = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'color',
            'birth_year',
            'owner',
            'achievements',
            'age',
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
            # создание новой записи или полчение существующего экземляра из
            # базы данных
            current_achievment, status = Achievement.objects.get_or_create(
                **achievment)
            # Ссылка на каждое достижение во всппомогательную таблицу с
            # указанием к каком котику она относится
            AchievementCat.objects.create(
                achievement=current_achievment,
                cat=cat
            )

        return cat

    def get_age(salf, obj):
        return dt.datetime.now().year - obj.birth_year


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
