from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def pagination(context, paginator):
    data = {
        'current_page': 0,
        'has_prev': False,
        'prev_page': None,
        'has_next': False,
        'next_page': None,
        'info': f'{paginator.count} out of {paginator.count}',
        'pages': [i for i in range(0, paginator.num_pages)]
    }

    try:
        data['current_page'] = int(context.request.GET['p'])
    except KeyError:
        pass

    if data['current_page'] < paginator.num_pages - 1:
        data['has_next'] = True
        data['next_page'] = data['current_page'] + 1
    if data['current_page'] > 0:
        data['has_prev'] = True
        data['prev_page'] = data['current_page'] - 1
    if paginator.count > paginator.per_page:
        if paginator.per_page * (data["current_page"] + 1) < paginator.count:
            data['info'] = f'{(data["current_page"] + 1) * paginator.per_page } out of {paginator.count}'
    return data
