#!/usr/bin/env python3

import time
import os
import requests

import speech_recognition as sr
from argparse import ArgumentParser
from urllib.parse import urlparse
from urllib.parse import parse_qs

# global variables
seq = 0


# this is called from the background thread
def callback(recognizer, audio):
    global seq

    print("Callback")
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said: " + text)

        if text == "end program now":
            print("Safe words detected: exiting")
            os._exit(1)

        if real_url:
            print("attempting: " + str(seq))

            params = query_parameters
            params["seq"] = str(seq)
            params["lang"] = lang
            data = text.encode('utf-8')

            print(params)
            print(data)

            req = requests.Request('POST', real_url, data=data, params=params)
            prepared = req.prepare()
            pretty_print_prepared(prepared)
            s = requests.Session()
            resp = s.send(prepared)
            print(resp)
            seq += 1

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def pretty_print_prepared(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        '-----------FINISH----------',
    ))


parser = ArgumentParser()

parser.add_argument("-z", "--zoom", dest="zoom",
                    help="Zoom CC Webhook URL", metavar="ZOOM")

args = parser.parse_args()

zoom_url = args.zoom
lang = "en-US"
query_parameters = {}
real_url = ""

if zoom_url:
    print("Zoom URL: " + zoom_url)
    o = urlparse(zoom_url)
    print(o)
    query_parameters = parse_qs(o.query)
    print(query_parameters)

    real_url = o.scheme + "://" + o.netloc + o.path
else:
    print("Required parameter '--zoom' not set")
    os._exit(1)

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

print("Now waiting for audio input.  Say the safe words of 'end program now' to stop.")

# wait forever
while True:
    time.sleep(0.1)

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)
