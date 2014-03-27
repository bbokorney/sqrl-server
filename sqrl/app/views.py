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
        qrcodeurl = AuthManager.getNewSession()
    else:
        print "Id is %s" % id
        if AuthManager.claimSession(id):
            return HttpResponseRedirect("/app")
        else:
            return HttpResponseRedirect("/app/login/")

    context = RequestContext(request)

    context_dict = {"qrcodeurl": "qrcodes/%s" % qrcodeurl}

    return render_to_response("app/login.html", context_dict, context)
