# -*- coding:utf-8 -*-

import os
import subprocess
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from webhook.secret import port, workdir, repos


@csrf_exempt
def recieve(request):
    if not(request.method == 'POST' and 'payload' in request.POST):
        return HttpResponseBadRequest("error.")

    jobj = json.loads(request.POST['payload'])
    # check repo
    repo = jobj['repository']['url']
    print('repo [%s]' % repo)
    if repo not in repos:
        return HttpResponse('not target repo')

    # modified master branch?
    ref = jobj['ref']
    print('branch [%s]' % ref)
    if ref != 'refs/heads/master':
        return HttpResponse("not master branch.")

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
    proj_root = workdir.split('/')[-1]
    newenv['DJANGO_SETTINGS_MODULE'] = proj_root + '.settings'
    subprocess.call(
        ['python', 'manage.py', 'runserver', '0.0.0.0:' + port],
        cwd=workdir, env=newenv)
    print('Done [runserver]')
    
    os.chdir(cwd)

    return HttpResponse("ok.")
