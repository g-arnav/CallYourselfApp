# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

from django.http import HttpResponseRedirect

from django.template import loader

from twilio.rest import Client

# Create your views here.

account_sid = 'ACd94b96428916f0656eaca16d8828ecb4'
auth_token = '04583809efd17c743a5277565f7244e5'

client = Client(account_sid, auth_token)

def redirect(request):
    return HttpResponseRedirect('call')

def call(number):
    message = client.api.account.calls \
        .create(to=number,  # Any phone number
                from_="+19253266295",  # Must be a valid Twilio number
                url="http://twilio.com")
    print(message.sid)

def checkBrowser(userAgentString):
    if 'iPhone' in userAgentString:
        if 'Safari' in userAgentString:
            return 'mobile'
        elif 'Safari' not in userAgentString:
            return 'app'
    else:
        return 'pc'

def checkUserAgentString(request):
    userAgentString = request.META['HTTP_USER_AGENT']
    context = {
        'userAgentString' : userAgentString
    }
    return render(request, 'call/checkUserAgentString.html', context)

def call_request(request):
    isApp = False
    userAgentString = request.META['HTTP_USER_AGENT']
    device = checkBrowser(userAgentString)
    if device == 'app':
        return render(request, 'call/call_request_app.html')
    elif device == 'pc':
        return render(request, 'call/call_request.html')
    elif device == 'mobile':
        return render(request, 'call/call_request_mobile.html')
    else:
        return render(request, 'call/unknown')

def make_call(request):
    phone_number = request.POST['number']
    context = {
    }

    isApp = False
    userAgentString = request.META['HTTP_USER_AGENT']
    device = checkBrowser(userAgentString)

    if device == 'app':
        try:
            call(phone_number)
            return render(request, 'call/call_made_app.html', context)
        except:
            context = {
                'call_error' : True
            }
            return render(request, 'call/call_request_app.html', context)
    elif device == 'pc':
        try:
            call(phone_number)
            return render(request, 'call/call_made.html', context)
        except:
            context = {
                'call_error': True
            }
            return render(request, 'call/call_request.html', context)
    elif device == 'mobile':
        try:
            call(phone_number)
            return render(request, 'call/call_made_mobile.html', context)
        except:
            context = {
                'call_error': True
            }
            return render(request, 'call/call_request_mobile.html', context)
    else:
        return render(request, 'call/unknown')