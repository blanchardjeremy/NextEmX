from django import http
from django import template
from django.conf import settings
from django.views.generic import TemplateView
from routeshout import RouteShoutAPI

def error500(request, template_name='500.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'STATIC_URL': settings.STATIC_URL,
    })
    return http.HttpResponseServerError(t.render(context))

def error404(request, template_name='404.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'STATIC_URL': settings.STATIC_URL,
    })
    return http.HttpResponseNotFound(t.render(context))


class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        api = RouteShoutAPI('e85e22cceb19cc296077fd21489ce9cf')
        a = api.agencies_getList()
        r = api.routes_getList('ltd')
        return context
