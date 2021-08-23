#!/usr/bin/env python3 


import logging
# logging.basicConfig(level=logging.DEBUG)
import pprint

import os
from slack import WebClient
from slack.errors import SlackApiError
from jinja2 import Template
import json


if not "SLACK_API_TOKEN" in os.environ:
    raise Exception('SLACK_API_TOKEN env is missing. Please add it to this action for proper execution.')
slack_token = os.environ["SLACK_API_TOKEN"]

default_channel = "devops"

channel = os.getenv('INPUT_CHANNEL', default_channel)

message_id =  os.getenv("INPUT_MESSAGE_ID", '')

# if 'INPUT_MESSAGE_ID' in os.environ:
#     message_id = os.environ["INPUT_MESSAGE_ID"]

# message_attachments = Template([
#         {
# 	        "mrkdwn_in": ["text"],
#             "color": "red",
#             "pretext": "preee",
#             "author_name": "luis",
#             "perro": "{{ caca }}",
#             "author_link": "http://flickr.com/bobby/",
#             "author_icon": "https://placeimg.com/16/16/people",
#         }
#     ])
# deployment_color = "brown"
cloud_run_deployment_url = "http://luis.com"

age = 8
# cloud_run_deployment_status = "False"
# cloud_run_deployment_status = os.getenv('DEPLOYMENT_STATUS', '')
# print(cloud_run_deployment_status)
cloud_run_deployment_status = "True"
job_status = "success"

# cloud_run_deployment_status = ""
# job_status = "starting"

message_id="1629743848.000900"





if cloud_run_deployment_status == "":
    deployment_message = "UNKNOWN"

if job_status == "starting" and cloud_run_deployment_status == "":
  github_job_message = ":desert_island: *_Github Action has started_* :desert_island:"
  deployment_color = "#20A9E5"
  json_template = """[
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
                    "value": "...",
                    "short": True
                },
                {
                    "title": "Cloud run deployment",
                    "value": "...",
                    "short": True
                }
            ],
            # "thumb_url": "http://placekitten.com/g/200/200",
            "footer": "{{ footer_message }}",
            "footer_icon": " {{ footer_icon }}",
        }
    ]
"""

else:
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

    json_template = """[
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

   



# print(github_job_message)



# export GITHUB_REF='nose/que/head/master' 
# export GITHUB_REPOSITORY='luis.git'
# export GITHUB_ACTOR='LuisAyazo'
# export GITHUB_SERVER_URL='http://mihija.com/url'
# export GITHUB_SHA='7as87y786asd'
# export GITHUB_WORKFLOW='epaaaaa_colombia'
# export DEPLOYMENT_STATUS='True'
# export SLACK_API_TOKEN=xoxb-498580303680-2366316234864-XjRxHxjCvUI3uJ16QXNlBscd
github_user = os.environ["GITHUB_ACTOR"] 
github_user_url = f"https://github.com/{ github_user }"

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

# print(data['github_user_url'])





j2_template = Template(json_template)

# print(j2_template.render(data))
att = j2_template.render(data)
# att = """
#     {
#         "fallback": "Plain-text summary of the attachment.",
#         "color": "#2eb886",
#         "pretext": "Optional text that appears above the attachment block",
#         "author_name": "Bobby Tables",
#         "author_link": "http://flickr.com/bobby/",
#         "author_icon": "http://flickr.com/icons/bobby.jpg",
#         "title": "Slack API Documentation",
#         "title_link": "https://api.slack.com/",
#         "text": "Optional text that appears within the attachment",
#         "fields": [
#             {
#                 "title": "Priority",
#                 "value": "High",
#                 "short": False
#             }
#         ],
#         "image_url": "http://my-website.com/path/to/image.jpg",
#         "thumb_url": "http://example.com/path/to/thumb.png",
#         "footer": "Slack API",
#         "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#         "ts": 123456789
#     }
# ]"""


# att2 = [
#     {
#         "fallback": "Plain-text summary of the attachment.",
#         "color": "#2eb886",
#         "pretext": "Optional text that appears above the attachment block",
#         "author_name": "Bobby Tables",
#         "author_link": "http://flickr.com/bobby/",
#         "author_icon": "http://flickr.com/icons/bobby.jpg",
#         "title": "Slack API Documentation",
#         "title_link": "https://api.slack.com/",
#         "text": "Optional text that appears within the attachment",
#         "fields": [
#             {
#                 "title": "Priority",
#                 "value": "High",
#                 "short": False
#             }
#         ],
#         "image_url": "http://my-website.com/path/to/image.jpg",
#         "thumb_url": "http://example.com/path/to/thumb.png",
#         "footer": "Slack API",
#         "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#         "ts": 123456789
#     }
# ]
# print(att)
# print(json.loads(json.dumps(att.replace('\n', ''), sort_keys=True, indent=4)))

from string import whitespace

# caca = att.replace('\n', '').replace(" ", "").replace('\\','')

# caca = caca.translate(whitespace)
# def stringToList(string):
#     listRes = list(string.split(" "))
#     return listRes
# # print(type(caca))
# print(type(att2))
# print(type(stringToList(caca)))
# print(repr(stringToList(caca)).replace("\n",r"\n").replace("\t",r"\t"))



# s1 = caca
# s2 = MyStr(stringToList(caca))

from ast import literal_eval

# # a = literal_eval(['{"mrkdwn_in":["text"],"color":"#FF0000","pretext":"_Deploymentcreatedfor_*luis.git*_ref:_`head/master`","author_name":"luisesillo","author_link":"http://flickr.com/bobby/","author_icon":"https://placeimg.com/16/16/people","title":"","text":":information_source:*_~GithubActionhasbeencancelled~_*:information_source:","fields":[{"title":"CloudRundeployURL","value":"<vergaaa|Linktocloudrun>","short":True},{"title":"ActionsURL","value":"<http/mi/url/luis.git/commit/7as87y786asd/checks|Githubaction:epaaaaa_colombia>","short":True},{"title":"Commit","value":"<http/mi/url/luis.git/commit/7as87y786asd|Commit>","short":True},{"title":"Cloudrundeployment","value":"PLEASECHECKURL","short":True}]}'])
literal_attachments = literal_eval(att)

# print("s1: %r" % s1)
# print("s2: %r" % s2)
# print(literal_attachments)
# print(stringToList(str(caca)))
# # print(stringToList(caca.format(', '.join(LL)))
# print("'{}'".format(stringToList(caca)))

client = WebClient(token=slack_token)
# response = client.conversations_members(channel="devops")


def get_channel_id(channel):
    response = client.conversations_list(
        types="public_channel, private_channel"
    )
    for channel_info in response['channels']:
        if channel_info['name'] == channel:
             return channel_info['id']


# channel_id = get_channel_id('devops-notifications')
# if not channel_id:
#     raise Exception('Channel not found!')
print(channel)

try:
  if not message_id:
    print( f"from a : { message_id } ")
    response = client.chat_postMessage(
      channel=channel,
      text="*DevBot Action: Deployment* :tada:",
      attachments=literal_attachments,
    #   attachments=att2,
      icon_url="http://lorempixel.com/48/48"
    )
    print(f"::set-outut name=message_id::{ response['ts'] }")
  else:
    print( f"from b : { message_id } ")
    channel_id = get_channel_id(channel)
    if not channel_id:
        raise Exception('Channel not found!')

    response = client.chat_update(
      channel=channel_id,
      ts=message_id,
      attachments=literal_attachments,
      text="*DevBot Action: Deployment* :tada:",
      icon_url="http://lorempixel.com/48/48"
    )

  # response = client.conversations_open(users=["UEQM4T18W"])
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"] 

