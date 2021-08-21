import os
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    my_input = os.environ["INPUT_CHANNEL"]
    webhook = os.environ["SLACK_WEBHOOK"]
    
    print(f" WEBHOOK FROM SLACK: {webhook}")

    message_id = f"Hello {my_input}"
    print(f"probando esto estamos {my_input}")
    print(f"::set-output name=message_id::{webhook}")


    
    myobj = {'event_name': 'Test from custom github action'}

    x = requests.post(webhook, data = myobj)

    print(x.text)

if __name__ == "__main__":
    main()
