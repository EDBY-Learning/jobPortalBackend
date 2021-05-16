from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import mixins
from rest_framework.views import APIView
from django.core import serializers as djangoSerializer
from . import serializers as myserializer
from .models import (
    BoardClassChapter,
    ChapterTopic,
    ChapterPrerequisite,
    AdaptiveQuestion,
    AdaptiveQuestionOptions,
    AdaptiveQuestionTopics,
    AdaptiveQuestionPrerequisite)
from django.db.utils import IntegrityError

from utils.operations import update_with_partial

OPERATION_AFTER_LOGIN_PERMISSION = {'create': [IsAuthenticated & IsAdminUser],
                                    'list': [IsAuthenticated & IsAdminUser],
                                    'retrieve': [IsAuthenticated & IsAdminUser],
                                    'update': [IsAuthenticated & IsAdminUser],
                                    'partial_update': [IsAuthenticated & IsAdminUser],
                                    'destroy': [IsAuthenticated & IsAdminUser]}


class BoardClassChapterViewset(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):

    serializer_class = myserializer.BoardClassChapterSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = BoardClassChapter.objects.all()

    # call put with /user/id/
    def update(self, request,  *args, **kwargs):
        return update_with_partial(self, request,  *args, **kwargs)

    # call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ChapterTopicViewset(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = myserializer.ChapterTopicSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = ChapterTopic.objects.all()

    # call put with /user/id/
    def update(self, request,  *args, **kwargs):
        return update_with_partial(self, request,  *args, **kwargs)

    # call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class GetChapterTopicViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = myserializer.GetChapterTopicSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = ChapterTopic.objects.all()


class ChapterPrerequisiteViewset(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):

    serializer_class = myserializer.ChapterPrerequisiteSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = ChapterPrerequisite.objects.all()

    # call put with /user/id/
    def update(self, request,  *args, **kwargs):
        return update_with_partial(self, request,  *args, **kwargs)

    # call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class AdaptiveQuestionViewset(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):

    serializer_class = myserializer.AdaptiveQuestionOptionsSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    queryset = AdaptiveQuestionOptions.objects.all()

    # call put with /user/id/
    def update(self, request,  *args, **kwargs):
        return update_with_partial(self, request,  *args, **kwargs)

    # call patch with /user/id/
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# class QuestionTopicsPrerequisiteViewset(mixins.CreateModelMixin,
#     # mixins.UpdateModelMixin,
#     # mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet):

#     serializer_class = myserializer.QuestionTopicsPrerequisiteSerializer
#     permission_classes = [IsAuthenticated & IsAdminUser]
#     queryset = AdaptiveQuestionTopics

#     #call put with /user/id/
#     def update(self, request,  *args, **kwargs):
#         partial = kwargs.pop('partial', True)
#         instance = None
#         #self.check_object_permissions(request,instance)
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     #call patch with /user/id/
#     def partial_update(self, request, *args, **kwargs):
#        kwargs['partial'] = True
#        return self.update(request, *args, **kwargs)
