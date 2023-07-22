from typing import Callable, Optional

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse

from django_htmx_components.types import ComponentContext, RenderedComponent


class HtmxComponent:
    def __init__(
        self,
        fn: Callable[[HttpRequest, ...], ComponentContext],
        namespace: str,
        scope: str,
        name: str,
    ):
        self.fn = fn
        self.template_name = "/".join([namespace, scope, name]) + ".html"
        self.name = name
        self.url = reverse(
            "htmx:component", kwargs={"scope": scope, "component": name}
        )

    def render(self, request: HttpRequest, params):
        context = self.fn(request, params)
        return RenderedComponent(
            render_to_string(
                self.template_name, context={**context.params, **{"self_url": self.url}}
            ),
            context.trigger,
        )
