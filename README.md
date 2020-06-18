# Xscrbd

A simple application to demonstrate automatic speech to closed captioning in Zoom.

Inspired by [Autosub](https://github.com/agermanidis/autosub) and the need for a cheap and simple CC service.  

## Why?

During the COVID-19 outbreak, my wife transitioned to full time work from home, including giving webinars.  Her work is 
required to have closed captions for all videos and live webinars that she provides.  However, her employer is cheap 
and didn't provide a CC service.

We quickly automated the CC generation for recorded sessions using the Autosub package.  However, we were having
trouble getting existing services connected with Zoom to automate the live CCs.  And the cheapest option that we
could find at the time would run us about $30 a month.  That's not an insurmountable price.  However, with that and
the other services that she was paying for out of pocket, it was starting to add up.

I made a quick survey of the technology behind Autosub and quickly discovered that it simply used Google Speech-to
-text API.  Another search revealed the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) package
.  That package looked like the beginnings of the right solution.  Granting me access to not only Google, but sevreal
other transcription services if I wanted.
 
Finally, I needed to figure out how to get the text to Zoom so they could provide it to the webinar participants
.  Zoom hasn't done a fantastic job in describing this API.  In fact, the only information I could find was an
[outdated support article](https://support.zoom.us/hc/en-us/articles/115002212983-Integrating-a-third-party-closed
-captioning-service).  This was at least enough to work back and build this application.
 
# Installation/Requirements
 
At this point, this application isn't really intended for distribution.  It still uses the hard coded test API token
for Google Speech-to-text.  It is noisy on the shell.  And its hard to install.
  
Most of the difficulties in installing and using this application will revolve around getting PyAudio (a dependency
) installed.  It is very platform dependent.  I had to install C development packages because the PyAudio package
wants to build native support.
 
Use a recent Python 3 (I'm using 3.7.7).
 
Assuming you can get by all that, the rest of the requirements.txt dependencies should be snap.
 
 # Usage
 
First, start your Zoom meeting.  Assuming your account supports CCs, you will see the 'CC' button at the bottom of
your meeting.  Click this and choose the 'Obtain API Token' option.  It will copy a long URL to your clipboard.  The
, run this application with the following:
 
```commandline
$ python __init__.py -z "<URL>"
```

Where '<URL>' is the URL from your clipboard.  It will contain all the meeting and security parameters.  This
application will parse out the required parameters for constructing the CC POST API calls to Zoom.

The application will print a message stating that it is waiting for audio and will also let you know what the 'safe
words' are that will stop the application.  (For some reason, occasionally the application won't detect the first
few seconds of speech.  Eventually it will start working.)

Now, every time you pause speaking, it will send your audio to Google, receive back text, and send that text to Zoom.

To see the CCs in Zoom, you must also click the 'CC' button so that it turns green.  Otherwise, CCs are hidden.
 
 # TODO
 
* Better error handling is still needed.
* Configuration options such as language, API key, and safe words.
* A command line mode to list audio input devices.  An option to choose a specific device. 
* In general, better Python code.