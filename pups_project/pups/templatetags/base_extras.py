from django import template

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if urls in request.path:
        return "active"
    return ""