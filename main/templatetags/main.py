from django import template
from main.forms import PostSearchForm

register = template.Library()

@register.inclusion_tag('contents/search_form.html')
def create_search_form(request):
    form = PostSearchForm(request.GET)
    return {'form' : form }