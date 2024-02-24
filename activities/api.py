from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import permissions, status, mixins, viewsets, parsers
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from activities.serializers import *
from datetime import datetime



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
        request=ActivityRegisterUserSerializer
    )
    @action(detail=False, methods=['post'])
    def get_points(self, request, pk=None):
        try:
            user = User.objects.get(pk=request.data['user_id'])
            if len(user.participations.all()) > 0:
                points = 0
                for activity in user.participations.all():
                    points = points + activity.points
                return Response({'points': points})
            else:
                return Response({'points': 0})
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=ActivityRegisterUserSerializer
    )
    @action(detail=True, methods=['post'])
    def add_student_participate(self, request, pk=None):
        try:
            activity = Activity.objects.get(pk=pk)
            user = User.objects.get(pk=request.data['user_id'])
            if user not in activity.participants.all():
                ##TODO: crear un part...
                participation = Participation(user=user, activity=activity)
                participation.save()
                ##activity.participants.add(participation)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'El usuario ya se encuentra registrado'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=ActivityRegisterUserSerializer
    )
    @action(detail=False, methods=['post'])
    def get_my_activities(self, request, pk=None):
        try:
            user = User.objects.get(pk=request.data['user_id'])
            current_day = datetime.now().strftime('%A').lower()
            user_activities = user.activities_participated.all()
            user_activities_today = user_activities.filter(
                activities_schedule__day=current_day
            ).order_by('activities_schedule__hour')
            serializer = ActivitySerializer(user_activities_today, many=True)
            return Response({ 'activities': serializer .data})
        except Activity.DoesNotExist:
            return Response({'message': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
