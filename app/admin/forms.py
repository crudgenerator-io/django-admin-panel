from django.forms import Media as DjangoMedia
from django.utils.html import format_html


class Media(DjangoMedia):
    def render_js(self):
        return [
            format_html(
                '<script src="{}" defer></script>',
                self.absolute_path(path)
            ) for path in self._js
        ]

    def __add__(self, other):
        combined = Media()
        combined._css_lists = self._css_lists + other._css_lists
        combined._js_lists = self._js_lists + other._js_lists
        return combined
