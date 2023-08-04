import socket
import random
import os
import argparse
import dbm

import requests
from requests.exceptions import HTTPError

from flask import Flask, request, render_template, abort


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
    # Validate Operational State
    if db[b'mode'] == b'on':
        # return 'Hello'
        return render_template(
            'main.html',
            name=socket.gethostname(),
            color=color_codes[COLOR],
            header_title=header_title,
            joke=get_joke()
            )

    abort(404)

@app.route("/state", methods=['GET', 'POST'])
def state():
    # Handle State Changes
    if request.method == 'POST':
        if request.form['state_button'] == 'ON':
            # Set Flask Operational State
            db[b'mode']  = b'on'
        elif request.form['state_button'] == 'OFF':
            # Set Flask Operational State
            db[b'mode']  = b'off'

    # Capture Current State
    if db[b'mode'] == b'on':
        current_state = "ON"
    elif db[b'mode'] == b'off':
        current_state = "OFF"

    # Render Page
    return render_template(
        'state.html',
        name=socket.gethostname(),
        color=color_codes[COLOR],
        header_title=header_title,
        state=current_state
        )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template(
        '404.html',
        name=socket.gethostname(),
        description=e
        ), 404


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

    # Open database and create if necessary
    with dbm.open('cache', 'c') as db:
        # Set Flask Operational State
        db[b'mode']  = b'on'
        # Run Flask Application
        app.run(host="0.0.0.0", port=8080)
