from django.contrib import admin
from .models import (
    BoardClassChapter,
    ChapterTopic,
    ChapterPrerequisite,
    AdaptiveQuestionOptions,
    AdaptiveQuestion,
    AdaptiveQuestionTopics,
    AdaptiveQuestionPrerequisite
)
from .models import BOARD
from django import forms

class QuestionInline(admin.TabularInline):
    model = AdaptiveQuestion

class ChapterTopicInline(admin.StackedInline):
    model = ChapterTopic

class ChapterPrerequisiteInline(admin.StackedInline):
    model = ChapterPrerequisite
    fk_name = "chapter"
    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super(ChapterPrerequisiteInline, self).get_formset(request, obj, **kwargs)
    #     # queryset = formset.form.base_fields["prerequisite"].queryset
    #     # queryset = queryset.select_related("topic")
    #     formset.form.base_fields["prerequisite"].queryset = ChapterTopic.objects.values_list('topic',flat=True)
    #     return formset

# class ChapterPrerequisiteForm(forms.ModelForm):
#     class Meta:
#         model = ChapterPrerequisite
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super(ChapterPrerequisiteForm, self).__init__(*args, **kwargs)
#         self.fields['chapter'].queryset = BoardClassChapter.objects.values_list('chapter',flat=True)
#         self.fields['prerequisite'].queryset = ChapterTopic.objects.values_list('topic',flat=True)


@admin.register(ChapterPrerequisite)
class ChapterPrerequisiteView(admin.ModelAdmin):
    list_display = ("chapter_name","pre_chapter","topic_name")
    search_fields = ("prerequisite__chapter__chapter","prerequisite__topic")
    list_filter = ("chapter__chapter",)
    def chapter_name(self, x):
        return x.chapter.chapter
    chapter_name.short_description = "For Chapter"

    def pre_chapter(self, x):
        return x.prerequisite.chapter.chapter
    pre_chapter.short_description = "Prerequisite Chapter"

    def topic_name(self, x):
        return x.prerequisite.topic
    topic_name.short_description = "Prerequisite Topic"
    
@admin.register(BoardClassChapter)
class BoardClassChapterView(admin.ModelAdmin):
    list_display = ("board","class_name","subject","chapter_num","chapter","entry_time")
    list_filter = ("board","class_name","subject")
    search_fields = ("chapter",)

    inlines = [
        ChapterTopicInline,
        ChapterPrerequisiteInline
    ]

# class ChapterTopicForm(forms.ModelForm):
#     class Meta:
#         model = ChapterTopic
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super(ChapterTopicForm, self).__init__(*args, **kwargs)
#         self.fields['chapter'].queryset = BoardClassChapter.objects.values_list('chapter',flat=True)

@admin.register(ChapterTopic)
class ChapterTopicView(admin.ModelAdmin):
    list_display = ("chapter_name","topic","entry_time")
    search_fields = ("topic","chapter__chapter")
    list_filter = ("chapter__chapter",)
    # form =  ChapterTopicForm
    
    def chapter_name(self, x):
        return x.chapter.chapter
    chapter_name.short_description = "Chapter Name"

class AdaptiveQuestionOptionsInline(admin.StackedInline):
    model = AdaptiveQuestionOptions
    extra = 0

class AdaptiveQuestionTopicsInline(admin.TabularInline):
    model = AdaptiveQuestionTopics
    extra = 3

class AdaptiveQuestionPrerequisiteInline(admin.TabularInline):
    model = AdaptiveQuestionPrerequisite
    extra = 3

def getBoard(x):
    for i in BOARD:
        if i[0]==x:
            return i[1]
    return "Null"

@admin.register(AdaptiveQuestion)
class AdaptiveQuestionView(admin.ModelAdmin):
    list_display = (
        #"user",
        "board_name",
        "class_name",
        "chapter_name",
        "ques_type",
        "level",
        "status",
        "entry_time")  

    search_fields = ("question","chapter_topic__chapter__chapter")
    list_filter = ("level","status","ques_type","chapter_topic__chapter__board","chapter_topic__chapter__class_name")

    inlines = [
        AdaptiveQuestionTopicsInline,
        AdaptiveQuestionPrerequisiteInline,
        AdaptiveQuestionOptionsInline
    ]  

    def board_name(self,x):
        return getBoard(x.chapter_topic.chapter.board)
    board_name.short_description = "Board"

    def chapter_name(self, x):
        return x.chapter_topic.chapter.chapter
    chapter_name.short_description = "Chapter Name"

    def class_name(self, x):
        return x.chapter_topic.chapter.class_name
    class_name.short_description = "Class"
