from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from app import AuthManager

def authenticated():
    return AuthManager.authenticate()

def index(request):
    if not authenticated():
        return HttpResponseRedirect("login")
    else:
        return HttpResponse("Successfully logged in!")

def login(request, id=None):
    qrcodeurl = None
    if id is None:
        print "Creating a new QR code."
    else:
        qrcodeurl = "qrcodes/%s" % id
        print "Id is %s" % id

    context = RequestContext(request)

    context_dict = {"qrcodeurl": qrcodeurl}

    return render_to_response("app/login.html", context_dict, context)
