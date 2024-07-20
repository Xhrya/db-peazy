import os
import azure.cognitiveservices.speech as speechsdk
import time

def speech_recognize_continuous_from_file(filepath):
    """Performs continuous speech recognition with input from an audio file"""
    speech_config = speechsdk.SpeechConfig(subscription='71e92aed489343f7ae9838c4b001bab1', region='eastus')
    audio_config = speechsdk.audio.AudioConfig(filename=filepath)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    recognized_text = []

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """Callback that signals to stop continuous recognition upon receiving an event `evt`"""
        ('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for recognizing event"""
        ('RECOGNIZING: {}'.format(evt))

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for recognized event"""
        ('RECOGNIZED: {}'.format(evt))
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text.append(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            ("NOMATCH: Speech could not be recognized.")

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: ('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: ('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: ('CANCELED {}'.format(evt)))
    
    # Stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    # Combine all recognized text into one big string
    all_text = ' '.join(recognized_text)
    print("All Recognized Text: ", all_text)

    return all_text

if __name__ == "__main__":
    speech_recognize_continuous_from_file('Audio-Test.wav')
