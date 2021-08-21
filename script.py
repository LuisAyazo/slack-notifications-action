import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

default_channel = "devops-notifications"

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

color = os.environ["INPUT_COLOR"]
print(f"COlor o que lo que {color}")


reason = os.environ['DEPLOYMENT_STATUS']

if 'HealthCheckContainerError' in reason:
    color = "#FF0000"
else:
    color = "#26C10A"

# status = os.environ['INPUT_DEPLOYMENT_STATUS']
print(reason)
# print(status[1])
# print(status['reason'])
# print(status['message'])
print(f"::set-output name=message_id::{reason}")
# slack_token = os.environ["INPUT_CHANNEL_ID"]
# slack_token = os.environ[""]
# slack_token = os.environ["SLACK_API_TOKEN"]
# slack_token = os.environ["SLACK_API_TOKEN"]

# repo_github_action_url = os.environ["GITHUB_SERVER_URL"] + "/" + os.environ["GITHUB_SERVER_URL"] + "/commit/" + os.environ["GITHUB_SHA"]  + "/checks|" + os.Getenv("GITHUB_WORKFLOW")

# print(repo_github_action_url)

client = WebClient(token=slack_token)

message_attachments = [
        {
	        "mrkdwn_in": ["text"],
            "color": f"{color}",
            "pretext": "_Deployment created for_ *CLIENT-WEB* _branch:_ `v0.0.1` ",
            "author_name": "author_name",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "https://placeimg.com/16/16/people",
            "title": "Link to..",
            "title_link": "https://api.slack.com/",
            # "title": "other",
            "text": f"{status} Optional `text` that appears within the attachment",
            "fields": [
                                {
                    "title": "Cloud Run deploy URL",
                    "value": "<http://i.imgur.com/nwo13SM.png|Link to cloud run>",
                    "short": True
                },
                {
                    "title": "Actions URL",
                    "value": "<http://i.imgur.com/nwo13SM.png|Link to github action>",
                    "short": True
                },
                {
                    "title": "Commit",
                    "value": "<http://i.imgur.com/nwo13SM.png|Commit>",
                    "short": True
                },
                {
                    "title": "Status",
                    "value": "SUCCESS",
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

