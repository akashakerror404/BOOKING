from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .seriallizer import FitnessClassSerializer, BookingSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
import pytz

logger = logging.getLogger('booking')


class FitnessClassListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get upcoming fitness classes",
        operation_description="Returns a list of upcoming classes. Optional timezone conversion using ?timezone param.",
        manual_parameters=[
            openapi.Parameter(
                'timezone',
                openapi.IN_QUERY,
                description="Timezone string like 'Asia/Kolkata' or 'UTC'",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response("Success", FitnessClassSerializer(many=True)),
            500: "Internal server error"
        }
    )
    def get(self, request):
        try:
            logger.info("Fetching upcoming fitness classes")
            queryset = FitnessClass.objects.filter(date_time__gt=timezone.now())

            tz = request.query_params.get('timezone')
            if tz:
                for obj in queryset:
                    obj.date_time = obj.convert_timezone(tz)

            serializer = FitnessClassSerializer(queryset.order_by('date_time'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Class list error: {e}")
            return Response(
                {"error": "Could not fetch classes"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateBookingView(APIView):
    @swagger_auto_schema(
        operation_summary="Book a fitness class",
        operation_description="Creates a booking. Requires fitness class ID, client name, and email.",
        request_body=BookingSerializer,
        responses={
            201: openapi.Response("Booking created", BookingSerializer),
            400: "Validation failed or already booked",
            500: "Internal server error"
        }
    )
    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            fitness_class = serializer.validated_data['fitness_class']
            client_email = serializer.validated_data['client_email']

            if fitness_class.available_slots <= 0:
                return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)

            if Booking.objects.filter(fitness_class=fitness_class, client_email=client_email).exists():
                return Response({"error": "Already booked"}, status=status.HTTP_400_BAD_REQUEST)

            fitness_class.available_slots -= 1
            fitness_class.save()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Booking error: {e}")
            return Response(
                {"error": "Could not create booking"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClientBookingsView(APIView):
    @swagger_auto_schema(
        operation_summary="Get bookings for a client",
        operation_description="Returns all upcoming bookings for a given client email.",
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="Client email",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response("Success", BookingSerializer(many=True)),
            400: "Missing email",
            500: "Internal server error"
        }
    )
    def get(self, request):
        try:
            email = request.query_params.get('email')
            if not email:
                return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

            bookings = Booking.objects.filter(
                client_email=email,
                fitness_class__date_time__gt=timezone.now()
            ).order_by('fitness_class__date_time')

            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Fetch bookings error: {e}")
            return Response(
                {"error": "Could not fetch bookings"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
