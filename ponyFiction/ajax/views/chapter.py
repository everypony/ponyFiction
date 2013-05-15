# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from ponyFiction.models import Story, Chapter
from ponyFiction.utils.misc import unicode_to_int_list
from ponyFiction.views.chapter import ChapterDelete
from ponyFiction.ajax.decorators import ajax_required
from django.utils.decorators import method_decorator

@ajax_required
@login_required
@csrf_protect
def chapter_sort(request, story_id):
    """ Сортировка глав """
    story = get_object_or_404(Story.objects.accessible(user=request.user), pk=story_id)
    if story.editable_by(request.user):
        new_order = unicode_to_int_list(request.POST.getlist('chapters[]'))
        if (not new_order or story.chapter_set.count() != len(new_order)):
                return HttpResponse('Bad request. Incorrect list!', status=400)
        else:
            for new_order_id, chapter_id in enumerate(new_order):
                chapter = Chapter.objects.get(pk=chapter_id)
                chapter.order = new_order_id+1
                chapter.save(update_fields=['order'])
            return HttpResponse('Done')
    else:
        raise PermissionDenied
    
class AjaxChapterDelete(ChapterDelete):
    
    template_name = 'includes/ajax/chapter_ajax_confirm_delete.html'
    
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return ChapterDelete.dispatch(self, request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        parent_response = super(AjaxChapterDelete, self).delete(self, request, *args, **kwargs)
        if parent_response.status_code == 302:
            return HttpResponse(self.chapter_id)
        else:
            return parent_response