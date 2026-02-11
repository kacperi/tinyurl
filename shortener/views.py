import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
