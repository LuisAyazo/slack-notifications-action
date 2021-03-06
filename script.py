# import logging
# logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError
from jinja2 import Template
from ast import literal_eval

# Github block
github_job = os.environ["GITHUB_JOB"]
github_user = os.environ["GITHUB_ACTOR"] 
github_user_url = f"https://github.com/{ github_user }"
github_event = os.environ["GITHUB_EVENT_NAME"]
github_repo_name = os.environ["GITHUB_REPOSITORY"]
github_branch_tag = '/'.join(os.environ["GITHUB_REF"].split("/")[2:])
github_action_url = os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"]  + "/checks" 
github_commit = os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"]
github_wokflow = os.environ["GITHUB_WORKFLOW"]

# Default Vars block
default_channel = "devops-notifications"

# Input Vars
channel                     =  os.getenv('INPUT_CHANNEL', default_channel)
message_id                  =  os.getenv("INPUT_MESSAGE_ID", '')
job_status                  =  os.getenv("INPUT_JOB_STATUS")
cloud_run_deployment_status =  os.getenv('INPUT_DEPLOYMENT_STATUS', '')

if not "SLACK_API_TOKEN" in os.environ:
    raise Exception('SLACK_API_TOKEN env is missing. Please add it to this action for proper execution.')
slack_token = os.environ["SLACK_API_TOKEN"]

if not "INPUT_JOB_STATUS" in os.environ:
    raise Exception('job_status is missing. Please add it to this action for proper execution.')
job_status = os.environ["INPUT_JOB_STATUS"]

if not "INPUT_DEPLOYMENT_URL" in os.environ:
    raise Exception('deployment_url is missing. check if deployment was executed succefully')
cloud_run_deployment_url = os.environ["INPUT_DEPLOYMENT_URL"]

# if not "SLACK_USER_ID" in os.environ:
#   channel = os.getenv('INPUT_CHANNEL', default_channel)
# else:
#   channel = os.environ["SLACK_USER_ID"]

# Colors block

if cloud_run_deployment_status == "":
    deployment_message = "UNKNOWN"

if job_status == "success" and cloud_run_deployment_status == "True":
    github_job_message = ":white_check_mark: *_Github Action finished succefully_* :white_check_mark:"
    deployment_color = "#0EB70B"
    deployment_message = "SUCCESS"
elif job_status == "success" and cloud_run_deployment_status == "False":
    github_job_message = ":white_check_mark: *_Github Action finished succefully_* :white_check_mark:"
    deployment_message = "FAILURE"
    deployment_color = "#DE1919"
elif job_status == "failure" and cloud_run_deployment_status == "True":
    github_job_message = ":warning::warning: *_Github Action finished with failure_* :warning::warning:"
    deployment_color = "#0EB70B"
    deployment_message = "SUCCESS"
elif job_status == "failure" and cloud_run_deployment_status == "False":
    github_job_message = ":warning::warning: *_Github Action finished with failure_* :warning::warning:"
    deployment_color = "#DE1919"
    deployment_message = "FAILURE"
elif job_status == "cancelled" and cloud_run_deployment_status == "True":
    github_job_message = ":information_source: *_~Github Action has been cancelled~_* :information_source:"
    deployment_color = "#0EB70B"
    deployment_message = "SUCCESS"
elif job_status == "cancelled" and cloud_run_deployment_status == "False":
    github_job_message = ":information_source: *_~Github Action has been cancelled~_* :information_source:"
    deployment_color = "#DE1919"
    deployment_message = "FAILURE"
else:
    github_job_message = f":sos: *_Github Action status:_* { job_status } :sos:" 
    deployment_color = "#D3D3D3"
    deployment_message = "UNKNOWN: CHECK THE URL"


# data fot the template
data = {
    "github_repo_name": os.environ["GITHUB_REPOSITORY"],
    "github_branch_tag": '/'.join(os.environ["GITHUB_REF"].split("/")[2:]),
    "github_user": github_user,
    "github_user_url": github_user_url,
    "github_action_url": os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"]  + "/checks" ,
    "github_wokflow": os.environ["GITHUB_WORKFLOW"],
    "github_commit": os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"],
    "github_job_message": github_job_message,
    "cloud_run_deployment_url": cloud_run_deployment_url,
    "deployment_message": deployment_message,
    "deployment_color": deployment_color,
    "footer_message": "Created by DevOps | Infra Team",
    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
}
                
# Prints Block
print(f"deployment_message: { deployment_message}")
print(f"deployment_color: { deployment_color}")
print(f"deployment_url: { cloud_run_deployment_url }")
print(f"GITHUB_JOB: { github_job }")
print(f"GITHUB_ACTOR: { github_user }")
print(f"GITHUB_EVENT_NAME: { github_event}")
print(f"GITHUB_REF: { github_branch_tag }")

# Slack Block
client = WebClient(token=slack_token)
template = """
[
        {
	        "mrkdwn_in": ["text"],
            # default color if deployment_color is not defined
            "color": "{{ deployment_color | default('#FF0000')}}",
            "pretext": "_Deployment created for_ *{{ github_repo_name }}* _ref:_ `{{ github_branch_tag }}` ",
            "author_name": "{{ github_user }}", 
            "author_link": "{{ github_user_url }}",
            "author_icon": "https://placeimg.com/16/16/people",
            # "title_link": "https://api.slack.com/",
            "text": "{{ github_job_message | default() }}",
            "fields": [

                {
                    "title": "Actions URL",
                    "value": "<{{ github_action_url }}|Github action: {{ github_wokflow }}>",
                    "short": True
                },
                {
                    "title": "Commit",
                    "value": "<{{ github_commit }}|Commit>",
                    "short": True
                },
                {
                    "title": "Cloud Run deploy URL",
                    "value": "<{{ cloud_run_deployment_url | default('')}}|Link to cloud run>",
                    "short": True
                },
                {
                    "title": "Cloud run deployment",
                    "value": "`{{ deployment_message }}`",
                    "short": True
                }
            ],
            # "thumb_url": "http://placekitten.com/g/200/200",
            "footer": "{{ footer_message }}",
            "footer_icon": " {{ footer_icon }}",
        }
    ]
"""


def get_channel_id(channel):
    response = client.conversations_list(
        types="public_channel, private_channel"
    )
    for channel_info in response['channels']:
        if channel_info['name'] == channel:
             return channel_info['id']


json_data = Template(template)
message_attachments = json_data.render(data)
# to avoid repr quote and problem sending attachtments to slack
literal_attachments = literal_eval(message_attachments)

try:
  if not message_id:
    response = client.chat_postMessage(
      channel=channel,
      text="*DevBot Action: Deployment* :tada:",
      attachments=literal_attachments,
      icon_url="http://lorempixel.com/48/48"
    )
    print(f"::set-outut name=message_id::{ response['ts'] }")
  
  else:
    channel_id = get_channel_id(channel)
    if not channel_id:
        raise Exception('Channel not found!')

    response = client.chat_update(
      channel=channel_id,
      ts=message_id,
      attachments=literal_attachments,
      text="*DevBot Action: Deployment update* :tada:",
      icon_url="http://lorempixel.com/48/48"
    )

  # response = client.conversations_open(users=["UEQM4T18W"])
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"] 

