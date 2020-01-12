import pyaudio
import wave, audioop, math

class Ambient_Noise:
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 0.5
    WAVE_OUTPUT_FILENAME = "output.wav"

    frames = []

    p = pyaudio.PyAudio()

    def read(self):
        stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        # print("* recording")

        self.frames = []
        sum = [0, 0.0]
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            rms = audioop.rms(data,2)
            decibel = 20 * math.log10(rms)
            sum[0] += 1
            sum[1] += decibel
            # print(decibel)
            self.frames.append(data)

        # print("* done recording")

        stream.stop_stream()
        stream.close()
        return(sum[1] / sum[0])
    def __del__(self):
        self.p.terminate()

    def save(self):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

recorder = Ambient_Noise()

print(recorder.read())
    