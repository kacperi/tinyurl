import json
from typing import Any
from urllib.parse import urlparse

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import View

from .models import ShortLink


class CreateShortlinkView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        url = data.get("url")
        if not url:
            return JsonResponse({"error": "Missing url in the request"}, status=400)

        shortlink, _ = ShortLink.objects.get_or_create(
            url=url,
            defaults={"hash": ShortLink(url=url).generate_hash()},
        )

        return JsonResponse({"shortlink": shortlink.hash})


@require_GET
def redirect_to_page(request: HttpRequest, hash: str) -> HttpResponse:
    shortlink_qs = ShortLink.objects.filter(hash=hash)
    if shortlink_qs.exists():
        target_url = shortlink_qs.first().url
    else:
        return render(
            request,
            "invalid_hash.html",
            {"hash": hash},
        )

    parsed_url = urlparse(target_url)
    if not parsed_url.scheme:
        target_url = "https://" + parsed_url.geturl()

    return redirect(target_url)
