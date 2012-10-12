# -*- coding:utf-8 -*-

import os
import subprocess
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from webhook.secret import port, workdir


@csrf_exempt
def recieve(request):
    if not(request.method == 'POST' and 'payload' in request.POST):
        return HttpResponseBadRequest("error.")

    # kill server
    p = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    all_process = p.stdout.read()
    p.stdout.close()
    server_process = [x for x in all_process.split('\n') if port in x]
    for pid in [x.split(' ')[0] for x in server_process]:
        subprocess.call(['kill', pid])
        print('Done [kill %s]' % pid)

    cwd = os.getcwdu()
    os.chdir(workdir)

    # pull repo
    subprocess.call(['git', 'pull', 'origin', 'master'], cwd=workdir)
    print('Done [git pull origin master]')

    # run server
    newenv = os.environ.copy()
    newenv['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    subprocess.call(
        ['python', 'manage.py', 'runserver', '0.0.0.0:' + port],
        cwd=workdir, env=newenv)
    print('Done [runserver]')
    
    os.chdir(cwd)

    return HttpResponse("ok.")
