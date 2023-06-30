import socket
import random
import os
import argparse

import requests
from requests.exceptions import HTTPError

from flask import Flask
from flask import render_template


app = Flask(__name__)

color_codes = {
    "red": "#ef2325",
    "blue": "#0086ea",
    "pink": "#de1b74",
    "darkblue": "#1d1d46"
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

# Get color from Environment variable
COLOR_FROM_ENV = os.environ.get('HEADER_COLOR')
TITLE_FROM_ENV = os.environ.get('HEADER_TITLE')

# Generate a random color
COLOR = random.choice(["red", "blue", "darkblue", "pink"])

def get_joke():
    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get('https://icanhazdadjoke.com/', headers=headers, timeout=5)
        response.raise_for_status()
        json_response = response.json()
        print(f"Received the following joke: {json_response.get('joke')}")
        return json_response.get('joke')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')


@app.route("/")
def main():
    # return 'Hello'
    return render_template(
        'main.html',
        name=socket.gethostname(),
        color=color_codes[COLOR],
        header_title=header_title,
        joke=get_joke()
        )


if __name__ == "__main__":
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    parser.add_argument('--title', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print(
                f"A color was set through environment variable -"
                f" {COLOR_FROM_ENV} "
                f". However, color from command line argument takes precendence."
            )
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    if args.title:
        print("Header from command line argument =" + args.title)
        header_title = args.title
        if TITLE_FROM_ENV:
            print(
                f"A title was set through environment variable -"
                f" {TITLE_FROM_ENV} "
                f". However, title from command line argument takes precendence."
            )
    elif TITLE_FROM_ENV:
        print("No Command line argument. Title from environment variable =" + TITLE_FROM_ENV)
        header_title = TITLE_FROM_ENV
    else:
        print("No command line argument or environment variable. Setting to WWT")
        header_title = "WWT"  # pylint: disable=C0103

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    # Run Flask Application
    app.run(host="0.0.0.0", port=8080)
