from django.contrib.admin import AdminSite as DjangoAdminSite
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse
from django.http import Http404
from django.utils.translation import gettext as _
from django.apps import apps

from django.views.i18n import JavaScriptCatalog

class AdminSite(DjangoAdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        models_objects_count = {}
        for k, v in self._registry.items():
            models_objects_count[v.opts.object_name] = v.model.objects.count()
        for app in app_list:
            for model in app['models']:
                model['objects_count'] = models_objects_count[model['object_name']]

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

    def i18n_javascript(self, request, extra_context=None):
        """
        Display the i18n JavaScript that the Django admin requires.

        `extra_context` is unused but present for consistency with the other
        admin views.
        """
        return JavaScriptCatalog.as_view(packages=['admin'])(request)

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])

        for k, v in self._registry.items():
            for model in app_dict['models']:
                if model['name'].lower() == k._meta.verbose_name or model['name'].lower() == k._meta.verbose_name_plural:
                    model['objects_count'] = v.model.objects.count()

        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)




site = AdminSite()
