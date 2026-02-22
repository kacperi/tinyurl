import json
from urllib.parse import urlparse

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import ShortLink


@csrf_exempt
@require_POST
def create_shortlink(request: HttpRequest) -> JsonResponse:
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
