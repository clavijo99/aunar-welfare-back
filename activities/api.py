from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import permissions, status, mixins, viewsets, parsers
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from activities.serializers import *
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from users import utils
from activities import utils as u



class ActivityViewSet(viewsets.ReadOnlyModelViewSet , viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            queryset = self.filter_queryset(self.get_queryset())

            # Excluir las actividades en las que el usuario ya está inscrito
            queryset = queryset.exclude(students=user)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Manejar el caso cuando el usuario no está autenticado
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


    @extend_schema(
        request=ActivityRegisterUserSerializer
    )
    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            user = User.objects.get(pk=request.data['user_id'])
            if user not in activity.students.all():
                activity.students.add(user)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'El usuario ya se encuentra registrado'}, status=status.HTTP_400_BAD_REQUEST)

        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=ActivityRegisterUserSerializer,
        responses=PointSerializer
    )
    @action(detail=False, methods=['post'])
    def get_points(self, request, pk=None):
        try:
            user = User.objects.get(pk=request.data['user_id'])
            if len(user.participations.all()) > 0:
                points = 0
                for activity in user.participations.all():
                    if activity.date_end is not None and activity.validate :
                        points = points + activity.activity.points
                return Response({'points': points})
            else:
                return Response({'points': 0})
        except User.DoesNotExist:
            return Response({'message': 'Usuario not found'}, status=status)
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=ActivityRegisterUserSerializer,
        responses=ParticipantSerializer
    )
    @action(detail=True, methods=['post'])
    def add_student_participate(self, request, pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            user = User.objects.get(pk=request.data['user_id'])
            now = timezone.now()

            # Comprueba si ya existe una participación activa para el usuario y la actividad
            existing_participation = Participation.objects.filter(user=user, activity=activity,
                                                                  date_end__isnull=True).exists()

            if not existing_participation:
                # Crea una nueva participación
                participation = Participation(user=user, activity=activity)
                participation.save()

                serializer = ParticipantSerializer(participation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Actualiza la participación existente
                participation = Participation.objects.get(user=user, activity=activity, date_end__isnull=True)
                participation.date_end = now
                participation.validate = True
                participation.save()

                # Actualiza los puntos usando F() para evitar problemas de concurrencia
                PointsUser.objects.filter(user=user).update(points=F('points') + activity.points)

                serializer = ParticipantSerializer(participation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Participation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=ActivityRegisterUserSerializer,
        responses=ActivitySerializer(many=True))
    @action(detail=False, methods=['post'])
    def get_my_activities(self, request, pk=None):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(pk=user_id)
            current_date = timezone.now().date()
            activities_student = Activity.objects.filter(students=user)

            # Excluye las actividades en las que el usuario ha participado con fecha de finalización y validez
            activities_not_participated = activities_student.exclude(
                participants__user=user,
                participants__validate=True
            )

            serializer = ActivitySerializer(activities_not_participated, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def get_my_activities_teacher(self, request, pk=None):
        try:
            current_date = datetime.now().date()
            user = User.objects.get(pk=request.data['user_id'])
            if user.type == utils.TEACHER:
                teacher_activities = Activity.objects.filter(
                    teacher=user,
                ).order_by('start_date', 'hour')
                serializer = ActivitySerializer(teacher_activities, many=True)
                return Response( serializer.data)
            else :
                return Response({'message': 'No es un profesor'})
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
