from os import listdir
from os import path
from os.path import isfile, join

import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self,path=None):
        self.base_path = "Recording"
        self.onlyfiles = [f for f in listdir(self.base_path) if isfile(join(self.base_path, f))]

    def recoginize(self):
        for file in self.onlyfiles:
            AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), str(self.base_path)+"/"+file)
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)

            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))



def main():
    speech = SpeechRecognizer()
    speech.recoginize()

if __name__=="__main__":
    main()