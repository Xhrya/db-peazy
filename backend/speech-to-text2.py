import os
import azure.cognitiveservices.speech as speechsdk
import time

def recognize_from_microphone(audio_input):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    #speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config = speechsdk.SpeechConfig(subscription='71e92aed489343f7ae9838c4b001bab1', region='eastus')
    speech_config.speech_recognition_language="en-US"

    #audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_input)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    '''
    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    '''
    done = False
    output = ""
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: format(evt.result.text))
    def handle_recognized(evt):
        nonlocal output
        output += format(evt.result.text) + " "  # Append recognized text to the output string

    speech_recognizer.recognized.connect(handle_recognized)
    #speech_recognizer.recognized.connect(lambda evt: print(format(evt.result.text)))

    '''
    all_results = []
    output = ""
    def handle_final_result(evt):
        all_results.append(evt)
        output += evt
        print(all_results)
    
    speech_recognizer.recognized.connect(lambda evt: handle_final_result(format(evt.result.text)))
    '''

    speech_recognizer.session_started.connect(lambda evt: format(evt))
    speech_recognizer.session_stopped.connect(lambda evt:format(evt))
    speech_recognizer.canceled.connect(lambda evt: format(evt))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    
    print(output)

recognize_from_microphone("Audio-Test.wav")
