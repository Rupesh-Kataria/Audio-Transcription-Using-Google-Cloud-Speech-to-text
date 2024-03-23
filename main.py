import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import queue
import sys

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        # Initialize PyAudio
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        # Open the audio stream
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Put None into the buffer queue to signal the end of data
        self._buff.put(None)
        # Terminate PyAudio
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        # Put audio data into the buffer queue
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Retrieve audio chunks from the buffer queue
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

def listen_print_loop(responses):
   # Process the transcription responses
   for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        print(transcript)


     
def main():
    # Initialize Google Cloud Speech client with service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        'audio.json')
    client = speech.SpeechClient(credentials=credentials)

    language_code = 'en-US'
    # Configure recognition and streaming parameters
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        # Generate streaming recognize requests
        print("Listening...")
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        # Perform streaming speech recognition
        responses = client.streaming_recognize(streaming_config, requests)
        # Process and print transcribed text
        listen_print_loop(responses)

if __name__ == '__main__':
    main()
