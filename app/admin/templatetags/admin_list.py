import datetime

from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (
    display_for_field, display_for_value, get_fields_from_path,
    label_for_field, lookup_field,
)
from django.contrib.admin.views.main import (
    ALL_VAR, ORDER_VAR, PAGE_VAR, SEARCH_VAR,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import Library
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import NoReverseMatch
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import gettext as _

from .base import InclusionAdminNode

from django.urls import reverse
from django.db.models import fields
from django.db.models.fields.related import ForeignKey as foreign_key_field


register = Library()

DOT = '.'

FIELD_TYPE_MAPPER = {
    fields.AutoField: 'number',
    fields.CharField: 'text',
    fields.DateField: 'date',
    fields.TimeField: 'time',
    fields.DateTimeField: 'datetime'
}


def get_js_field_type(field):
    field_type = type(field)
    if field_type in (fields.AutoField, fields.IntegerField, fields.DecimalField):
        return 'number'
    elif field_type in (fields.CharField, fields.EmailField, fields.TextField):
        if field.choices:
            return 'enum'
        return 'text'
    elif field_type == fields.DateField:
        return 'date'
    elif field_type == fields.TimeField:
        return 'time'
    elif field_type == fields.DateTimeField:
        return 'datetime'
    elif field_type == fields.BooleanField:
        return 'boolean'
    elif field_type == fields.files.FileField:
        return 'file'
    elif field_type == foreign_key_field:
        return 'relationship'


@register.simple_tag(name='filter_parameters')
def filter_parameters_tag(cl, attrs):
    """
    returns filter parameters (restricted by list_display fields from model admin) as html <select>
    """
    options = []
    for field_name in cl.list_display:
        if field_name == 'action_checkbox' or field_name == '__str__':
            continue
        field = next(filter(lambda x: x.name == field_name, cl.model._meta.concrete_fields))
        options.append(format_html(f'<option data-type={get_js_field_type(field)} value={field.attname}>{field.verbose_name.title()}</option>'))
    options = '\n'.join(options)
    return format_html(f'<select {attrs}>{options}</select>')


@register.simple_tag(name='sort_parameters')
def sort_parameters_tag(sortable_parameters, attrs):
    """
    returns sort parameters (restricted by sortable fields from model admin) as html <select>
    """
    options = []
    for param in sortable_parameters:
        options.append(format_html(f'<option value={param}>{param.title()}</option>'))
    options = '\n'.join(options)
    return format_html(f'<select {attrs}>{options}</select>')



@register.simple_tag(name='enumerations')
def enumerations_tag(cl, attrs):
    enums = []

    model_enum_fields = list(filter(lambda x: get_js_field_type(x) == 'enum', cl.model._meta.concrete_fields))
    for enum_field in model_enum_fields:
        options = []
        for choice in enum_field.choices:
            options.append(format_html(f'<option value={choice[0]}>{choice[1]}</option>'))
        options = '\n'.join(options)
        enums.append(format_html(f'<select {attrs} data-field={enum_field.attname}>{options}</select>'))

    return enums


def html_sanitize_repr(input_repr):
    return input_repr.replace('<', '&lt;').replace('>', '&gt;')


@register.simple_tag(name='relationships')
def relationships_tag(cl, attrs):
    relationships = []

    model_relationship_fields = list(filter(lambda x: get_js_field_type(x) == 'relationship', cl.model._meta.concrete_fields))
    for model_relationship_field in model_relationship_fields:
        options = []
        for choice in model_relationship_fields[0].related_model.objects.all():
            options.append(format_html(f'<option value={choice.id}>{html_sanitize_repr(repr(choice))}</option>'))
        options = '\n'.join(options)
        relationships.append({
            'widget':format_html(f'<select {attrs} data-field={model_relationship_field.attname}>{options}</select>'),
            'label': model_relationship_field.verbose_name.title()
        })

    return relationships




@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == DOT:
        return '… '
    elif i == cl.page_num:
        return format_html('<span class="this-page">{}</span> ', i + 1)
    else:
        return format_html(
            '<a href="{}"{}>{}</a> ',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else ''),
            i + 1,
        )


def pagination(cl, current_page=0):
    """
    Generate the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range += [
                    *range(0, ON_ENDS), DOT,
                    *range(page_num - ON_EACH_SIDE, page_num + 1),
                ]
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range += [
                    *range(page_num + 1, page_num + ON_EACH_SIDE + 1), DOT,
                    *range(paginator.num_pages - ON_ENDS, paginator.num_pages)
                ]
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page

    data = {
        'current_page': int(current_page or 0),
        'has_prev': False,
        'prev_page': None,
        'has_next': False,
        'next_page': None,
        'info': f'{paginator.count} out of {paginator.count}',
        'pages': [i for i in range(0, paginator.num_pages)]
    }

    if data['current_page'] < paginator.num_pages - 1:
        data['has_next'] = True
        data['next_page'] = cl.get_query_string({PAGE_VAR: data['current_page'] + 1})
    if data['current_page'] > 0:
        data['has_prev'] = True
        data['prev_page'] = cl.get_query_string({PAGE_VAR: data['current_page'] - 1})
    if paginator.count > paginator.per_page:
        if paginator.per_page * (data["current_page"] + 1) < paginator.count:
            begin = data["current_page"] * paginator.per_page
            end = begin + paginator.per_page
            data['info'] = f'{begin + 1} - {end} out of {paginator.count}'

    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
        **data
    }


@register.tag(name='pagination')
def pagination_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=pagination,
        template_name='pagination.html',
        takes_context=False,
    )


def result_headers(cl):
    """
    Generate the list column headers.
    """
    ordering_field_columns = cl.get_ordering_field_columns()
    for i, field_name in enumerate(cl.list_display):
        text, attr = label_for_field(
            field_name, cl.model,
            model_admin=cl.model_admin,
            return_attr=True
        )
        is_field_sortable = cl.sortable_by is None or field_name in cl.sortable_by
        if attr:
            field_name = _coerce_field_name(field_name, i)
            # Potentially not sortable

            # if the field is the action checkbox: no sorting and special class
            if field_name == 'action_checkbox':
                yield {
                    "text": text,
                    "class_attrib": mark_safe(' class="action-checkbox-column"'),
                    "sortable": False,
                }
                continue

            admin_order_field = getattr(attr, "admin_order_field", None)
            # Set ordering for attr that is a property, if defined.
            if isinstance(attr, property) and hasattr(attr, 'fget'):
                admin_order_field = getattr(attr.fget, 'admin_order_field', None)
            if not admin_order_field:
                is_field_sortable = False

        if not is_field_sortable:
            # Not sortable
            yield {
                'text': text,
                'class_attrib': format_html(' class="column-{}"', field_name),
                'sortable': False,
            }
            continue

        # OK, it is sortable if we got this far
        th_classes = ['sortable', 'column-{}'.format(field_name)]
        order_type = ''
        new_order_type = 'asc'
        sort_priority = 0
        # Is it currently being sorted on?
        is_sorted = i in ordering_field_columns
        if is_sorted:
            order_type = ordering_field_columns.get(i).lower()
            sort_priority = list(ordering_field_columns).index(i) + 1
            th_classes.append('sorted %sending' % order_type)
            new_order_type = {'asc': 'desc', 'desc': 'asc'}[order_type]

        # build new ordering param
        o_list_primary = []  # URL for making this field the primary sort
        o_list_remove = []  # URL for removing this field from sort
        o_list_toggle = []  # URL for toggling order type for this field

        def make_qs_param(t, n):
            return ('-' if t == 'desc' else '') + str(n)

        o_list_primary = [make_qs_param(new_order_type, i)]

        yield {
            "text": text,
            "sortable": True,
            "sorted": is_sorted,
            "ascending": order_type == "asc",
            "url_primary": cl.get_query_string({ORDER_VAR: '.'.join(o_list_primary)}),
            "class_attrib": format_html(' class="{}"', ' '.join(th_classes)) if th_classes else '',
        }


def _boolean_icon(field_val):
    icon_url = static('admin/img/icon-%s.svg' % {True: 'yes', False: 'no', None: 'unknown'}[field_val])
    return format_html('<img src="{}" alt="{}">', icon_url, field_val)


def _coerce_field_name(field_name, field_index):
    """
    Coerce a field_name (which may be a callable) to a string.
    """
    if callable(field_name):
        if field_name.__name__ == '<lambda>':
            return 'lambda' + str(field_index)
        else:
            return field_name.__name__
    return field_name


def items_for_result(cl, result, form):
    """
    Generate the actual list of data.
    """

    def link_in_col(is_first, field_name, cl):
        if cl.list_display_links is None:
            return False
        if is_first and not cl.list_display_links:
            return True
        return field_name in cl.list_display_links

    first = True
    pk = cl.lookup_opts.pk.attname
    for field_index, field_name in enumerate(cl.list_display):
        empty_value_display = cl.model_admin.get_empty_value_display()
        row_classes = ['field-%s' % _coerce_field_name(field_name, field_index)]
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(attr, 'empty_value_display', empty_value_display)
            if f is None or f.auto_created:
                if field_name == 'action_checkbox':
                    row_classes = ['action-checkbox']
                boolean = getattr(attr, 'boolean', False)
                result_repr = display_for_value(value, empty_value_display, boolean)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append('nowrap')
            else:
                if isinstance(f.remote_field, models.ManyToOneRel):
                    field_val = getattr(result, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    result_repr = display_for_field(value, f, empty_value_display)
                if isinstance(f, (models.DateField, models.TimeField, models.ForeignKey)):
                    row_classes.append('nowrap')
                elif isinstance(f, (models.BooleanField)):
                    row_classes.append('checkmark-td')
                    if value:
                        row_classes.append('positive')
                    else:
                        row_classes.append('negative')
                elif isinstance(f, models.FileField):
                    row_classes.append('file-td')
        row_class = mark_safe(' class="%s"' % ' '.join(row_classes))
        # If list_display_links not defined, add the link tag to the first field
        if link_in_col(first, field_name, cl):
            table_tag = 'td'
            first = False

            # Display link to the result's change_view if the url exists, else
            # display just the result's representation.
            try:
                url = cl.url_for_result(result)
            except NoReverseMatch:
                link_or_text = result_repr
            else:
                url = add_preserved_filters({'preserved_filters': cl.preserved_filters, 'opts': cl.opts}, url)
                # Convert the pk to something that can be used in Javascript.
                # Problem cases are non-ASCII strings.
                if cl.to_field:
                    attr = str(cl.to_field)
                else:
                    attr = pk
                value = result.serializable_value(attr)
                link_or_text = result_repr
                # format_html(
                #     '<a href="{}"{}>{}</a>',
                #     url,
                #     format_html(
                #         ' data-popup-opener="{}"', value
                #     ) if cl.is_popup else '',
                #     result_repr)

            yield format_html('<{}{}>{}</{}>', table_tag, row_class, link_or_text, table_tag)
        else:
            # By default the fields come from ModelAdmin.list_editable, but if we pull
            # the fields out of the form instead of list_editable custom admins
            # can provide fields on a per request basis
            if (form and field_name in form.fields and not (
                    field_name == cl.model._meta.pk.name and
                    form[cl.model._meta.pk.name].is_hidden)):
                bf = form[field_name]
                result_repr = mark_safe(str(bf.errors) + str(bf))
            yield format_html('<td{}>{}</td>', row_class, result_repr)

    info = (result._meta.app_label, result._meta.model_name)
    admin_url = reverse('admin:%s_%s_change' % info, args=(result.pk,))
    yield format_html(f'<td><a href={admin_url}></a></td>')
    if form and not form[cl.model._meta.pk.name].is_hidden:
        yield format_html('<td>{}</td>', form[cl.model._meta.pk.name])


class ResultList(list):
    """
    Wrapper class used to return items in a list_editable changelist, annotated
    with the form object for error reporting purposes. Needed to maintain
    backwards compatibility with existing admin templates.
    """
    def __init__(self, form, *items):
        self.form = form
        super().__init__(*items)


def results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield ResultList(form, items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield ResultList(None, items_for_result(cl, res, None))


def result_hidden_fields(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            if form[cl.model._meta.pk.name].is_hidden:
                yield mark_safe(form[cl.model._meta.pk.name])


def result_list(cl):
    """
    Display the headers and data list together.
    """
    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    return {
        'cl': cl,
        'result_hidden_fields': list(result_hidden_fields(cl)),
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(cl)),
    }


@register.tag(name='result_list')
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=result_list,
        template_name='change_list_results.html',
        takes_context=False,
    )


def date_hierarchy(cl):
    """
    Display the date hierarchy for date drill-down functionality.
    """
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        field = get_fields_from_path(cl.model, field_name)[-1]
        if isinstance(field, models.DateTimeField):
            dates_or_datetimes = 'datetimes'
            qs_kwargs = {'is_dst': True}
        else:
            dates_or_datetimes = 'dates'
            qs_kwargs = {}
        year_field = '%s__year' % field_name
        month_field = '%s__month' % field_name
        day_field = '%s__day' % field_name
        field_generic = '%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)

        def link(filters):
            return cl.get_query_string(filters, [field_generic])

        if not (year_lookup or month_lookup or day_lookup):
            # select appropriate start level
            date_range = cl.queryset.aggregate(first=models.Min(field_name),
                                               last=models.Max(field_name))
            if date_range['first'] and date_range['last']:
                if dates_or_datetimes == 'datetimes':
                    date_range = {
                        k: timezone.localtime(v) if timezone.is_aware(v) else v
                        for k, v in date_range.items()
                    }
                if date_range['first'].year == date_range['last'].year:
                    year_lookup = date_range['first'].year
                    if date_range['first'].month == date_range['last'].month:
                        month_lookup = date_range['first'].month

        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup, month_field: month_lookup}),
                    'title': capfirst(formats.date_format(day, 'YEAR_MONTH_FORMAT'))
                },
                'choices': [{'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))}]
            }
        elif year_lookup and month_lookup:
            days = getattr(cl.queryset, dates_or_datetimes)(field_name, 'day', **qs_kwargs)
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup}),
                    'title': str(year_lookup)
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}),
                    'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))
                } for day in days]
            }
        elif year_lookup:
            months = getattr(cl.queryset, dates_or_datetimes)(field_name, 'month', **qs_kwargs)
            return {
                'show': True,
                'back': {
                    'link': link({}),
                    'title': _('All dates')
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month.month}),
                    'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
                } for month in months]
            }
        else:
            years = getattr(cl.queryset, dates_or_datetimes)(field_name, 'year', **qs_kwargs)
            return {
                'show': True,
                'back': None,
                'choices': [{
                    'link': link({year_field: str(year.year)}),
                    'title': str(year.year),
                } for year in years]
            }


@register.tag(name='date_hierarchy')
def date_hierarchy_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=date_hierarchy,
        template_name='date_hierarchy.html',
        takes_context=False,
    )


def search_form(cl):
    """
    Display a search form for searching the list.
    """
    return {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }


@register.tag(name='search_form')
def search_form_tag(parser, token):
    return InclusionAdminNode(parser, token, func=search_form, template_name='search_form.html', takes_context=False)


@register.simple_tag
def admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    # filter type, if it's enumeration - choices (aswell as relationship)
    return tpl.render({
        'title': spec.title,
        'spec': spec,
    })


def admin_actions(context):
    """
    Track the number of times the action field has been rendered on the page,
    so we know which value to use.
    """
    context['action_index'] = context.get('action_index', -1) + 1
    return context


@register.tag(name='admin_actions')
def admin_actions_tag(parser, token):
    return InclusionAdminNode(parser, token, func=admin_actions, template_name='actions.html')


@register.tag(name='change_list_object_tools')
def change_list_object_tools_tag(parser, token):
    """Display the row of change list object tools."""
    return InclusionAdminNode(
        parser, token,
        func=lambda context: context,
        template_name='change_list_object_tools.html',
    )
