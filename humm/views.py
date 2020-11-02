from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Humm
import random
from .form import CreateHumm
from rest_framework.response import Response
from django.utils.http import is_safe_url
from .serializer import HummSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    print(request.user or None)
    # return HttpResponse(f"<h1>Hello {humm_id}</h1>")
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createView(request, *args, **kwargs):
    serializer = HummSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def list_view(request, *args, **kwargs):
    lst = Humm.objects.all()
    serializer = HummSerializer(lst, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def humms_Detail(request, humm_id, *args, **kwargs):
    lst = Humm.objects.filter(id=humm_id)
    if not lst.exists():
        return Response({}, status=404)
    serializer = HummSerializer(lst.first())
    return Response(serializer.data, status=200)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def humms_Delete(request, humm_id, *args, **kwargs):
    lst = Humm.objects.filter(id=humm_id)
    if not lst.exists():
        return Response({}, status=404)
    lst = lst.filter(user=request.user)
    if not lst.exists():
        return Response({"message": "You cant delete the Humm "}, status=401)
    obj = lst.first()

    obj.delete()
    # obj.save()
    return Response({"message": "Humm Removed"}, status=200)


def createView_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = CreateHumm(request.POST or None)
    # print(abc)
    nextUrl = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user  # if anonym user then none
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if nextUrl != None and is_safe_url(nextUrl, ALLOWED_HOSTS):
            return redirect(nextUrl)
        form = CreateHumm()
    if form.errors:
        if request.is_ajax():
            print("error")
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})


def list_view_pure_django(request, *args, **kwargs):
    lst = Humm.objects.all()
    humms = [obj.serialize() for obj in lst]
    data = {
        "response": humms
    }
    return JsonResponse(data)


def humms_Detail_pure_django(request, humm_id, *args, **kwargs):
    """
    REST API VIEW
    consume by Javascript, Swift/Android/Java/IOS
    return json data
    """

    data = {
        "id": humm_id,
        # "content": obj.content,
        # "image_path" : obj.image,
    }
    status = 200
    try:
        obj = Humm.objects.get(id=humm_id)
        data["content"] = obj.content

    except:
        data["message"] = "Not Found"
        status = 404
    # similar to json.dumps content_type='application.json'
    return JsonResponse(data, status=status)
