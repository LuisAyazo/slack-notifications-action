import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

# Github block
github_job = os.environ["GITHUB_JOB"]
github_user = os.environ["GITHUB_ACTOR"] 
github_event = os.environ["GITHUB_EVENT_NAME"]
github_repo_name = os.environ["GITHUB_REPOSITORY"]
github_branch_tag = '/'.join(os.environ["GITHUB_REF"].split("/")[2:])
github_action_url = os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"]  + "/checks" 
github_commit = os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_REPOSITORY"] + "/commit/" + os.environ["GITHUB_SHA"]
github_wokflow = os.environ["GITHUB_WORKFLOW"]

# Default Vars block
default_channel = "devops-notifications"
job_attachment = [] 
job_message = ""
job_color = ""

# Input Vars
if not "SLACK_API_TOKEN" in os.environ:
    raise Exception('SLACK_API_TOKEN env is missing. Please add it to this action for proper execution.')
slack_token = os.environ["SLACK_API_TOKEN"]

if not "INPUT_DEPLOYMENT_URL" in os.environ:
    raise Exception('deployment_url is missing. check if deployment was executed succefully')
cloud_run_deployment_url = os.environ["INPUT_DEPLOYMENT_URL"]

if not "SLACK_USER_ID" in os.environ:
  channel = os.getenv('INPUT_CHANNEL', default_channel)
else:
  channel = os.environ["SLACK_USER_ID"]

if 'INPUT_MESSAGE_ID' in os.environ:
    message_id = os.environ["INPUT_MESSAGE_ID"]


def test():
  return '"text": ":warning::warning: `Errror in github actions` :warning::warning:",'
# Colors block
status = os.environ['DEPLOYMENT_STATUS']
job_status = os.environ["INPUT_JOB_STATUS"]
print(f"Job Status: {job_status}")

if job_status == "success" and status == "True":
    deployment_color = "#26C10A"
    deployment_message = "SUCCESS"

elif job_status == "failure" and status == "True":
   # Job is failure in some step
   job_attachment = "jobATTCH"
   job_message = "Github Action Failure"
   job_color = "#FF0000"
   def test():
     return '"text": ":warning::warning: `Errror in github actions` :warning::warning:",'
 
   # deployment to cloud run is success
   deployment_color = "#26C10A"
   deployment_message = "SUCCESS"
else:
   #  job_status = cancelled
   deployment_color = "#FF0000"
   deployment_message = "FAILURE"
                
# Prints Block
print(f"j_message: { job_message }")
print(f"j_color: { job_color }")
print(f"j_attachment: { job_attachment}")
print(f"d_message: { deployment_message}")
print(f"d_color: { deployment_color}")
print(f"d_url: { cloud_run_deployment_url }")
print(f"GITHUB_JOB: { github_job }")
print(f"GITHUB_ACTOR: { github_user }")
print(f"GITHUB_EVENT_NAME: { github_event}")
print(f"GITHUB_REF: { github_branch_tag }")



# Slack Block
client = WebClient(token=slack_token)
message_attachments = [
        {
	        "mrkdwn_in": ["text"],
            "color": f"{deployment_color}",
            "pretext": f"_Deployment created for_ *{ github_repo_name }* _ref:_ `{ github_branch_tag}` ",
            "author_name": f"{ github_user }",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "https://placeimg.com/16/16/people",
            # "title": "Link to..",
            # "title_link": "https://api.slack.com/",
            test
            if job_message: 
            "fields": [
                {
                    "title": "Cloud Run deploy URL",
                    "value": f"<{ cloud_run_deployment_url }|Link to cloud run>",
                    "short": True
                },
                {
                    "title": "Actions URL",
                    "value": f"<{ github_action_url }|Github action: { github_wokflow }>",
                    "short": True
                },
                {
                    "title": "Commit",
                    "value": f"<{ github_commit }|Commit>",
                    "short": True
                },
                {
                    "title": "Status",
                    "value": f"{deployment_message}",
                    "short": True
                }
            ],
            # "thumb_url": "http://placekitten.com/g/200/200",
            "footer": "Created by DevOps | Infra Team",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            # "ts": 123456789
        }
    ]

try:
  if not message_id:
    response = client.chat_postMessage(
      channel=channel,
      text="Hello im your DevBot! :tada:",
      attachments=message_attachments,
      icon_url="http://lorempixel.com/48/48"
    )
    print(f"::set-outut name=message_id::{ response['ts'] }")
  
  else:
    response = client.chat_update(
      channel=channel,
      ts=message_id,
      text="updates from your DevBot! :tada:",
      icon_url="http://lorempixel.com/48/48"

    )

  # response = client.conversations_open(users=["UEQM4T18W"])
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"] 

