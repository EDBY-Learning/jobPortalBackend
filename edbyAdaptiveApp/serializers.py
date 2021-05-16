from .models import (
    BoardClassChapter,
    ChapterTopic,
    ChapterPrerequisite,
    AdaptiveQuestion,
    AdaptiveQuestionOptions,
    AdaptiveQuestionTopics,
    AdaptiveQuestionPrerequisite
)
from django.contrib.auth.models import User
from rest_framework import serializers
import re
from django.db.utils import IntegrityError
# from django.core.exceptions import Exception

class BoardClassChapterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = BoardClassChapter
        fields = "__all__"
        required_fields = "__all__"

class ChapterTopicSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    board_class_chapter_id = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = ChapterTopic
        fields = ('id','board_class_chapter_id','topic')
        required_fields = ('board_class_chapter_id','topic')
    
    def create(self,validated_data):
        try:
            chapter = BoardClassChapter.objects.get(id=validated_data.pop("board_class_chapter_id"))
        except Exception as e:
            raise serializers.ValidationError("Wrong chapter Id selected!It does not Exist")
        topic,created = ChapterTopic.objects.get_or_create(chapter=chapter,**validated_data)
        return topic

    def update(self,instance,validated_data):   
        temp = validated_data.pop("board_class_chapter_id")
        topic,created = ChapterTopic.objects.update_or_create(id=instance.id,defaults=validated_data)
        return topic

class GetChapterTopicSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    chapter = BoardClassChapterSerializer(read_only=True)
    class Meta:
        model = ChapterTopic
        fields = "__all__"

class ChapterPrerequisiteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    chapter_id = serializers.CharField(required=True)
    prerequisite_id = serializers.CharField(required=True)
    class Meta:
        model = ChapterPrerequisite
        fields = ('id','chapter_id','prerequisite_id')
    
    def validate_prerequisite_id(self,prerequisite_id):
        return [prerequisite.strip() for prerequisite in prerequisite_id.split(",")]
    
    def get_data(self,ch_id,pre_id):
        try:
            chapter = BoardClassChapter.objects.get(id=ch_id)
        except Exception as e:
            raise serializers.ValidationError("Wrong chapter Id selected!It does not Exist")
        try:
            prerequisite = ChapterTopic.objects.get(id=pre_id)
        except Exception as e:
            raise serializers.ValidationError("Wrong Prerequisite Topic Id selected!It does not Exist")
        
        return chapter,prerequisite

    def create(self,validated_data):
        ch_id = validated_data.pop("chapter_id")
        pre_ids = validated_data.pop("prerequisite_id",[])
        for pre_id in pre_ids:
            chapter,prerequisite = self.get_data(ch_id,pre_id)
            ch_prerequisite,created = ChapterPrerequisite.objects.get_or_create(chapter=chapter,prerequisite=prerequisite)
        return ch_prerequisite

    def update(self,instance,validated_data):   
        chapter,prerequisite = self.get_data(validated_data)
        ch_prerequisite,created = ChapterTopic.objects.update_or_create(
            id=instance.id,
            defaults={
                chapter:chapter,
                prerequisite:prerequisite
        })
        return ch_prerequisite      

class AdaptiveQuestionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = AdaptiveQuestion
        fields = "__all__"

class AdaptiveQuestionOptionsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    question = AdaptiveQuestionSerializer(required=True)
    topics_ids = serializers.CharField(required=True,write_only=True)
    prerequisite_ids = serializers.CharField(required=False,write_only=True)
    class Meta:
        model = AdaptiveQuestionOptions
        fields = ("id","question","option_a","option_b","option_c","option_d","topics_ids","prerequisite_ids")
    
    def create_topic_pre(self,question,topic_data,prerequisite_data):
        AdaptiveQuestionPrerequisite.objects.filter(question=question).delete()
        AdaptiveQuestionTopics.objects.filter(question=question).delete()
        # print(topic_data,prerequisite_data)
        for topic_id in topic_data:
            try:
                topic = ChapterTopic.objects.get(id=topic_id)
            except Exception as e:
                raise serializers.ValidationError("Wrong Topic Id selected!It does not Exist "+topic_id)
            saved = AdaptiveQuestionTopics.objects.get_or_create(
                question=question,
                topic=topic)
        for prerequisite_id in prerequisite_data:#:
            try:
                prerequisite = ChapterTopic.objects.get(id=prerequisite_id)
            except Exception as e:
                raise serializers.ValidationError("Wrong Prerequisite Id selected!It does not Exist "+prerequisite_id)
            saved = AdaptiveQuestionPrerequisite.objects.get_or_create(
                question=question,
                prerequisite=prerequisite)

    def validate_topics_ids(self,topics_ids):
        return [topic.strip() for topic in topics_ids.split(",")]
    
    def validate_prerequisite_ids(self,prerequisite_ids):
        return [prerequisite.strip() for prerequisite in prerequisite_ids.split(",")]


    def create(self,validated_data):
        question = AdaptiveQuestion.objects.create(**validated_data.pop("question"))
        self.create_topic_pre(question,validated_data.pop("topics_ids",[]),validated_data.pop("prerequisite_ids",[]))
        options = AdaptiveQuestionOptions.objects.create(question=question,**validated_data)
        return options

    def update(self,instance,validated_data):
        question,created = AdaptiveQuestion.objects.update_or_create(
            id=instance.question.id,
            defaults=validated_data.pop("question")
        )
        self.create_topic_pre(question,validated_data.pop("topics_ids",[]),validated_data.pop("prerequisite_ids",[]))
        options,created = AdaptiveQuestionOptions.objects.update_or_create(
            id=instance.id,
            defaults=validated_data
        )
        return options 

# class QuestionTopicsPrerequisiteSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)
#     question_id = serializers.CharField(required=True,write_only=True)
#     topics_ids = serializers.CharField(required=True,write_only=True)
#     prerequisite_ids = serializers.CharField(required=False,write_only=True)
    
#     class Meta:
#         fields = ("id","question_id","topics_ids","prerequisite_ids")

#     def validate(self,data):
#         if data['question_id'].strip()=="":
#             raise serializers.ValidationError("Question Id required")
#         return data

#     def validate_topics_ids(self,topics_ids):
#         return [topic.strip() for topic in topics_ids.split(",")]
    
#     def validate_prerequisite_ids(self,prerequisite_ids):
#         return [prerequisite.strip() for prerequisite in prerequisite_ids.split(",")]

#     def create_topic_pre(self,question,validated_data):
#         AdaptiveQuestionPrerequisite.objects.filter(question=question).delete()
#         AdaptiveQuestionTopics.objects.filter(question=question).delete()
#         print(validated_data)
#         for topic_id in validated_data.pop("topics_ids",[]):
#             try:
#                 topic = ChapterTopic.objects.get(id=topic_id)
#             except Exception as e:
#                 raise serializers.ValidationError("Wrong Topic Id selected!It does not Exist "+topic_id)
#             saved = AdaptiveQuestionTopics.objects.get_or_create(
#                 question=question,
#                 topic=topic)
#         for prerequisite_id in validated_data.pop("prerequisite_ids",[]):
#             try:
#                 prerequisite = ChapterTopic.objects.get(id=prerequisite_id)
#             except Exception as e:
#                 raise serializers.ValidationError("Wrong Prerequisite Id selected!It does not Exist "+prerequisite_id)
#             saved = AdaptiveQuestionPrerequisite.objects.get_or_create(
#                 question=question,
#                 prerequisite=prerequisite)

#     def create(self,validated_data):
#         try:
#             question = AdaptiveQuestion.objects.get(id=validated_data["question_id"])
#         except Exception as e:
#             raise serializers.ValidationError("Wrong Question Id selected!It does not Exist "+validated_data["question_id"])
#         self.create_topic_pre(question,validated_data)
#         return "Added Topics and Prerequisite"

#     # def update(self,instance,validated_data):
#     #     self.create(validated_data)