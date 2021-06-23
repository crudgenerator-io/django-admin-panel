import operator
from django.db.models import Q
import functools
from django.db.models.fields.related import ForeignKey


from django.contrib.admin.filters import SimpleListFilter



def get_repr_for_lookup(model, filter_expr):
    """
    Get representation for lookup

    stringified_lookup -- example username__icontains
    """
    field, operator, val = filter_expr.split('__')

    negate = False
    if operator.startswith('!'):
        negate = True
        operator = operator[1:]

    if operator == 'icontains':
        operator_repr = 'contains'
    elif operator == 'gte':
        operator_repr = 'greater than'
    elif operator == 'lte':
        operator_repr = 'less than'
    else:
        operator_repr = operator


    if operator == 'is':
        # special handling for boolean
        ret_val = (
            f'{field.replace("_", " ").title()} {operator_repr} {"not" if negate else ""} {val}',
            Q((f"{field}", val == 'True' and not negate)),
            f'{field}__{"!" if negate else ""}{operator}__{val}'
        )
        return ret_val

    ret_val = (
        f'{field.replace("_", " ").title()} {operator_repr} {val}',
        Q((f"{field}__{operator}", val)),
        f'{field}__{"!" if negate else ""}{operator}__{val}'
    )
    if negate:
        ret_val = (
            f'{field.replace("_", " ").title()} not {operator_repr} {val}',
            ~Q((f"{field}__{operator}", val)),
            f'{field}__{"!" if negate else ""}{operator}__{val}'
        )

    if type(getattr(model, field).field) == ForeignKey:
        ret_val = (
            f'{field.replace("_id", "").title()} {"is not" if negate else "is"} {repr(getattr(model, field).field.related_model.objects.get(pk=val))}',
            ret_val[1],
            ret_val[2]
        )

    return ret_val



class AdminListFilter(SimpleListFilter):
    title = 'Filters'
    parameter_name = 'f'

    def __init__(self, request, params, model, model_admin):
        self.lookup_expressions = []
        req_filters = request.GET.get(self.parameter_name)
        if req_filters:
            for filter_expr in req_filters[1:-1].split(','):
                self.lookup_expressions.append(get_repr_for_lookup(model, filter_expr[1:-1]))
        super().__init__(request, params, model, model_admin)

    def queryset(self, request, queryset):
        filter_clause = []
        for lookup in self.lookup_expressions:
            filter_clause.append(lookup[1])
        if not filter_clause:
            return queryset
        return queryset.filter(
            functools.reduce(
                operator.and_,
                filter_clause
            )
        )

    def construct_filter_from_lookup(self, filter_clause, lookup):
        lookup_expr, lookup_val = lookup.split(':')
        if lookup_expr.startswith("!"):
            lookup_expr = lookup_expr[1:]
            return ~Q((f"{lookup_expr}", lookup_val))
        else:
            return Q((f"{lookup_expr}", lookup_val))

    def has_output(self):
        return True

    def expected_parameters(self):
        return self.parameter_name

    def choices(self, changelist):
        return super().choices(changelist)

    def lookups(self, request, model_admin):
        return ((), )
