from rest_framework import serializers

from .models import User, Address, Ads, Vehicle


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("street", "city", "country", "phone_number")


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("number_plate", "model", "brand")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    car = VehicleSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "age",
            "car",
            "address",
        )


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = (
            "author",
            "title",
            "description",
            "price_per_km",
            "vehicle",
            "file",
            "created",
        )
