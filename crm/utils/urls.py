from django.shortcuts import reverse


def reverse_url(request, name, *args, **kwargs):
    base_url = reverse(name, args=args, kwargs=kwargs)
    params = request.GET.urlencode()
    if not params:
        return base_url
    return'{}?{}'.format(base_url, params)

