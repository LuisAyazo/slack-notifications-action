import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

# Github block
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

   # deployment to cloud run is success
   deployment_color = "#26C10A"
   deployment_message = "SUCCESS"
else:
   deployment_color = "#FF0000"
   deployment_message = "FAILURE"

print(f"::set-output name=message_id::seguire probando esto")
print(f"j_message: { job_message }")
print(f"j_color: { job_color }")
print(f"j_attachment: { job_attachment}")
print(f"d_message: { deployment_message}")
print(f"d_color: { deployment_color}")
print(f"d_url: { cloud_run_deployment_url }")

client = WebClient(token=slack_token)
message_attachments = [
        {
	        "mrkdwn_in": ["text"],
            "color": f"{deployment_color}",
            "pretext": "_Deployment created for_ *CLIENT-WEB* _branch:_ `v0.0.1` ",
            "author_name": "author_name",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "https://placeimg.com/16/16/people",
            "title": "Link to..",
            "title_link": "https://api.slack.com/",
            "text": ":warning: :sos: Errror in github actions :sos::warning: ",
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
  # if !channel
  response = client.chat_postMessage(
    channel=channel,
    text="Hello from your app! :tada:",
    attachments=message_attachments
  )

  # response = client.conversations_open(users=["UEQM4T18W"])
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"] 

