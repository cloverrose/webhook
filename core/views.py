# -*- coding:utf-8 -*-

import os
import subprocess
import json
import re
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from webhook.secret import secrets


def get_repo(url):
    """
    >>> repo = get_repo('https://github.com/cloverrose/webhook')
    >>> repo == ('cloverrose', 'webhook')
    True
    """
    ptn = re.compile('https?://github.com/(.+?)/(.+)')
    mo = ptn.match(url)
    if mo is None or len(mo.groups()) != 2:
        return None
    return mo.groups()


def get_branch(ref):
    """
    >>> branch = get_branch('refs/heads/master')
    >>> branch == 'master'
    True
    """
    ptn = re.compile('refs/heads/(.+)')
    mo = ptn.match(ref)
    if mo is None or len(mo.groups()) != 1:
        return None
    return mo.group(1)


@csrf_exempt
def recieve(request):
    if not(request.method == 'POST' and 'payload' in request.POST):
        return HttpResponseBadRequest("error.")

    jobj = json.loads(request.POST['payload'])
    # check repo
    repo_url = jobj['repository']['url']
    print('url [%s]' % repo_url)
    repo = get_repo(repo_url)
    if repo is None:
        return HttpResponse('invalid url')
    print('repo [%s/%s]' % repo)
    if repo not in secrets:
        return HttpResponse('not target repo')

    target = secrets[repo]
    branch = target['branch']
    port = target['port']
    workdir = target['workdir']

    # check branch
    ref = jobj['ref']
    print('ref [%s]' % ref)
    br = get_branch(ref)
    if br is None:
        return HttpResponse('invalid ref')
    print('branch [%s]' % br)
    if br != branch:
        return HttpResponse('not target branch')

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
    print('Done [cd %s]' % workdir)

    # pull repo
    subprocess.call(['git', 'pull', 'origin', branch], cwd=workdir)
    print('Done [git pull origin %s]' % branch)

    # run server
    newenv = os.environ.copy()
    proj_root = workdir.split('/')[-1]
    newenv['DJANGO_SETTINGS_MODULE'] = proj_root + '.settings'
    subprocess.call(
        ['python', 'manage.py', 'runserver', port],
        cwd=workdir, env=newenv)
    print('Done [python manage.py runserver %s]' % port)

    os.chdir(cwd)
    print('Done [cd %s]' % cwd)

    return HttpResponse("ok.")
