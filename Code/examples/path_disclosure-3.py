# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from cuckoo.common.config import config
from cuckoo.core.submit import SubmitManager
from cuckoo.web.bin.utils import api_post, JsonSerialize, json_error_response

submit_manager = SubmitManager()

def defaults():
    machinery = config("cuckoo:cuckoo:machinery")

    if config("routing:vpn:enabled"):
        vpns = config("routing:vpn:vpns")
    else:
        vpns = []

    return {
        "machine": config("%s:%s:machines" % (machinery, machinery)),
        "package": None,
        "priority": 2,
        "timeout": config("cuckoo:timeouts:default"),
        "routing": {
            "route": config("routing:routing:route"),
            "inetsim": config("routing:inetsim:enabled"),
            "tor": config("routing:tor:enabled"),
            "vpns": vpns,
        },
        "options": {
            "enable-services": False,
            "enforce-timeout": False,
            "full-memory-dump": config("cuckoo:cuckoo:memory_dump"),
            "no-injection": False,
            "process-memory-dump": True,
            "simulated-human-interaction": True,
        },
    }

class SubmissionApi(object):
    @staticmethod
    @csrf_exempt
    @require_http_methods(["POST"])
    def presubmit(request):
        files = request.FILES.getlist("files[]")
        data = []

        if files:
            for f in files:
                data.append({
                    "name": f.name,
                    "data": f.file,
                })

            submit_id = submit_manager.pre(submit_type="files", data=data)
            return redirect("submission/pre", submit_id=submit_id)
        else:
            body = json.loads(request.body)
            submit_type = body["type"]

            if submit_type != "strings":
                return json_error_response("type not \"strings\"")

            submit_id = submit_manager.pre(
                submit_type=submit_type, data=body["data"].split("\n")
            )

            return JsonResponse({
                "status": True,
                "submit_id": submit_id,
            }, encoder=JsonSerialize)

    @api_post
    def get_files(request, body):
        submit_id = body.get("submit_id", 0)
        password = body.get("password", None)
        astree = body.get("astree", True)

        data = submit_manager.get_files(
            submit_id=submit_id,
            password=password,
            astree=astree
        )

        return JsonResponse({
            "status": True,
            "data": data,
            "defaults": defaults(),
        }, encoder=JsonSerialize)

    @api_post
    def submit(request, body):
        submit_id = body.pop("submit_id", None)
        submit_manager.submit(
            submit_id=submit_id, config=body
        )
        return JsonResponse({
            "status": True,
            "submit_id": submit_id,
        }, encoder=JsonSerialize)
