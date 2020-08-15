from json import dumps

from flask import Blueprint, request

from slackr.controllers import workspace

WORKSPACE_ROUTE = Blueprint('workspace', __name__)


@WORKSPACE_ROUTE.route("/workspace/reset", methods=['POST'])
def route_workspace_reset():
    ''' Flask route for /workspace/reset'''
    return dumps(workspace.workspace_reset())
