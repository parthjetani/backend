import json

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
)

from .models import User, Vehicle, Ads, Address
from .serializers import (
    UserSerializer,
    VehicleSerializer,
    AdsSerializer,
)


# Create your views here.
class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        body = request.data
        vehicle_validated_data = body.pop("vehicle", None)
        address_validated_data = body.pop("address", None)
        user_password = body.pop("password", None)

        user = User.objects.create(**body)
        user.set_password(user_password)
        user.save()

        try:
            Address.objects.create(user=user, **address_validated_data)
        except:
            return HttpResponse(
                json.dumps({"success": False, "message": "Address data needed"}),
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            Vehicle.objects.create(user=user, **vehicle_validated_data)
        except:
            return HttpResponse(
                json.dumps({"success": False, "message": "Vehicle data needed"}),
                status=HTTP_400_BAD_REQUEST,
            )

        return HttpResponse(
            json.dumps(
                {"success": True, "message": "User and Vehicle created successfully"}
            ),
            status=HTTP_201_CREATED,
        )


class UpdateUserViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        instance = User.objects.get(id=pk)
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                json.dumps({"success": True, "message": "User updated successfully"}),
                status=HTTP_200_OK,
            )
        return HttpResponse(
            json.dumps({"success": False, "message": "Something went wrong"}),
            status=HTTP_400_BAD_REQUEST,
        )


class UpdateVehicleViewSet(viewsets.ViewSet):
    serializer_class = VehicleSerializer

    def update(self, request, pk=None):
        instance = Vehicle.objects.get(id=pk)
        serializer = VehicleSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                json.dumps(
                    {"success": True, "message": "Vehicle updated successfully"}
                ),
                status=HTTP_200_OK,
            )
        return HttpResponse(
            json.dumps({"success": False, "message": "Something went wrong"}),
            status=HTTP_400_BAD_REQUEST,
        )


class AdsViewSet(ListAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response = []
        for data in serializer.data:
            author = User.objects.get(id=data.pop("author")[0])
            vehicle = Vehicle.objects.get(id=data.pop("vehicle")[0])
            data["full_name"] = author.first_name + " " + author.last_name
            data["brand"] = vehicle.brand
            data["model"] = vehicle.model
            response.append(data)
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        author_id = data.pop("author", None)[0]
        vehicle_id = data.pop("vehicle", None)[0]
        file = data.pop("file")[0]
        title = data.pop("title")[0]
        description = data.pop("description")[0]
        price_per_km = data.pop("price_per_km")[0]

        if not author_id:
            return HttpResponse(
                json.dumps({"success": False, "message": "author_id needed"}),
                status=HTTP_400_BAD_REQUEST,
            )

        if not vehicle_id:
            return HttpResponse(
                json.dumps({"success": False, "message": "vehicle_id needed"}),
                status=HTTP_400_BAD_REQUEST,
            )

        author = User.objects.get(id=author_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)

        try:
            instance = Ads.objects.create(
                file=file,
                title=title,
                description=description,
                price_per_km=price_per_km,
            )
            instance.vehicle.add(vehicle)
            instance.author.add(author)
        except Exception as e:
            return HttpResponse(
                json.dumps({"success": False, "message": e}),
                status=HTTP_400_BAD_REQUEST,
            )

        return HttpResponse(
            json.dumps({"success": True, "message": "Ads created successfully"}),
            status=HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                json.dumps({"success": True, "message": "Ads updated successfully"}),
                status=HTTP_200_OK,
            )
        return HttpResponse(
            json.dumps({"success": False, "message": "Something went wrong"}),
            status=HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return HttpResponse(
            json.dumps({"success": True, "message": "Ads deleted successfully"}),
            status=HTTP_204_NO_CONTENT,
        )
