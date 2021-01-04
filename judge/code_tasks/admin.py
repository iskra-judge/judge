from django.contrib import admin

from judge.code_tasks.models import CodeSubmissionType, CodeTask, TaskTest, CodeTaskCategory, Difficulty


class TaskTestInlineAdmin(admin.StackedInline):
    model = TaskTest


class CodeTaskAdmin(admin.ModelAdmin):
    inlines = (TaskTestInlineAdmin,)
    list_display = ('id', 'name')
    readonly_fields = ('description_html',)

    def preview(self, obj):
        return obj.description_html


class CodeTaskInlineAdmin(admin.StackedInline):
    model = CodeTask
    fields = ('name', 'id')
    readonly_fields = ('name', 'id')
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class CodeTaskInlineManyToManyRelationsAdmin(admin.StackedInline):
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CodeTaskForCatagoriesInlineAdmin(CodeTaskInlineManyToManyRelationsAdmin):
    model = CodeTask.categories.through


class DifficultyAdmin(admin.ModelAdmin):
    inlines = (CodeTaskInlineAdmin,)


class CodeTaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code_tasks_count')
    inlines = (CodeTaskForCatagoriesInlineAdmin,)

    def code_tasks_count(self, obj):
        return obj.codetask_set.count()


class CodeTaskForSubmissionTypesInlineAdmin(CodeTaskInlineManyToManyRelationsAdmin):
    model = CodeTask.code_submission_types.through


class CodeSubmissionTypeAdmin(admin.ModelAdmin):
    inlines = (CodeTaskForSubmissionTypesInlineAdmin,)


admin.site.register(CodeSubmissionType, CodeSubmissionTypeAdmin)
admin.site.register(CodeTask, CodeTaskAdmin)
admin.site.register(CodeTaskCategory, CodeTaskCategoryAdmin)
admin.site.register(Difficulty, DifficultyAdmin)
