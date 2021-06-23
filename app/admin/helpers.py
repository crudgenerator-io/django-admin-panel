import json

from django.template.defaultfilters import capfirst
from django.utils.translation import gettext
from django.contrib.admin.helpers import InlineAdminFormSet as DjangoInlineAdminFormSet


class InlineAdminFormSet(DjangoInlineAdminFormSet):
    """
    A data extension of an default inline formset for use in the admin system.
    """
    def inline_formset_data(self):
        verbose_name = self.opts.verbose_name
        return json.dumps({
            'name': '#%s' % self.formset.prefix,
            'options': {
                'prefix': self.formset.prefix,
                'addText': gettext('Add another %(verbose_name)s') % {
                    'verbose_name': capfirst(verbose_name),
                },
                'deleteText': gettext('Remove'),
            },
            'plural': str(self.opts.opts.auto_created._meta.verbose_name_plural).capitalize()
        })
