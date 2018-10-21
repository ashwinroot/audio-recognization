import pyaudio
import wave
from array import array

'''
Audio Recorder 

'''
class AudioRecorder:
    def __init__(self,length_threshold=30):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 15
        self.LENGTH_THRESHOLD = length_threshold

        self.audio = pyaudio.PyAudio()  # instantiate the pyaudio

        # recording prerequisites
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        # starting recording
        self.frames = dict()
        self.frames_details = dict()

    '''Main loop to record n seconds of the audio'''
    # todo : Work on keyboard interrupt for audio
    def record(self,seconds=None):
        record_seconds= self.RECORD_SECONDS if seconds==None else seconds
        new_frames = []
        x=0
        for i in range(0, int(self.RATE / self.CHUNK * record_seconds)):
            data = self.stream.read(self.CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            new_frames.append(data)
            if (vol >= 500):
                new_frames.append(data)
            else:
                if len(new_frames) >= self.LENGTH_THRESHOLD:
                    self.frames[x] = new_frames
                    print(" " + str(x))
                    x = x + 1
                new_frames = []
        self.batch_save()

    def batch_save(self):
        for key, frame in self.frames.items():
            print("Key : " + str(key) + "Frame length" + str(len(frame)))
            self.save_file("Recording/recording" + str(key) + ".wav", frame)

    def save_file(self,filename, frames):
        wavfile = wave.open(filename, 'wb')
        wavfile.setnchannels(self.CHANNELS)
        wavfile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wavfile.setframerate(self.RATE)
        wavfile.writeframes(b''.join(frames))  # append frames recorded to file
        print("Saved " + filename)
        wavfile.close()

    '''
    Closing the audio stream
    '''
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


def main():
    audioRecorder = AudioRecorder()
    audioRecorder.record()


if __name__=="__main__":
    main()