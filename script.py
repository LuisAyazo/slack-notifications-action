import os
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    my_input = os.environ["INPUT_CHANNEL"]
    webhook = os.environ["SLACK_WEBHOOK"]
    
    print(f" WEBHOOK FROM SLACK: {webhook}")

    message_id = f"Hello {my_input}"
    print(f"probando esto estamos {my_input}")
    print(f"::set-output name=message_id::{webhook}")

    webhook_url = webhook
    slack_data = {'text': "Sup! Test from custom github action :spaghetti:"}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    

if __name__ == "__main__":
    main()
