import os
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    my_input = os.environ["INPUT_CHANNEL"]

    message_id = f"Hello {my_input}"
    print(f"probando esto estamos {my_input}")
    print(f"::set-output name=message_id::{message_id}")


if __name__ == "__main__":
    main()
