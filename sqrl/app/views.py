import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import django.contrib.auth as Auth
from django.views.decorators.csrf import csrf_exempt
from app import AuthManager


@login_required
@csrf_exempt
def index(request):
    return HttpResponse("You have successfully logged in, %s!" % request.user.username)

@csrf_exempt
def login(request):
    qrcodeurl = None
    token = None
    if request.method == "GET":
        print "Creating a new QR code."
        qrcodeurl, token = AuthManager.createNewAuth()
    elif request.method == "POST":
        token = request.POST["token"]
        user = AuthManager.loginAuthenticate(token)
        if user is not None:
            Auth.login(request, user)
            return HttpResponseRedirect("/app/")
        else:
            return HttpResponse("Invalid login.")

    context = RequestContext(request)

    context_dict = {"qrcodeurl": "qrcodes/%s" % qrcodeurl, "token": token}

    return render_to_response("app/login.html", context_dict, context)



@csrf_exempt
def sqrl(request, token):
    success = False
    if request.method != "POST":
        print "Request method not POST."
    elif "idk" not in request.POST or "sig" not in request.POST:
        print "Parameters not present in POST."
    else:
        success = AuthManager.sqrlAuthenticate(token, request.POST["idk"], request.POST["sig"])

    response_dict = {"success": success}

    data = json.dumps(response_dict)
    return HttpResponse(data, mimetype="application/json")
