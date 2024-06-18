import sounddevice as sd
import soundfile as sf
from scipy.signal import butter, lfilter

from config import MAX_FREQ, MIN_FREQ
from decoder import Decoder
from encoder import Encoder


def record_audio(output_filename, duration, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")

    # Save the recorded audio to a WAV file
    sf.write(output_filename, audio_data, sample_rate)
    print(f"Audio recorded and saved to {output_filename}")


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def main():
    output_file = "recorded_audio.wav"
    filtered_output_file = "filtered_audio.wav"
    duration = 10  # Duration to record in seconds

    # Encode and play the message
    byte_data = b"Hello, World!"
    encoder = Encoder()
    encoder_output_file = "encoded_message.wav"
    encoder.bytes_to_wav(byte_data, encoder_output_file)

    # Record audio from the microphone
    record_audio(output_file, duration)

    # Read the recorded audio
    audio_data, sample_rate = sf.read(output_file)

    # Apply bandpass filter to the audio data
    filtered_audio = bandpass_filter(audio_data, MIN_FREQ, MAX_FREQ, sample_rate)

    # Save the filtered audio to a new WAV file
    sf.write(filtered_output_file, filtered_audio, sample_rate)
    print(f"Filtered audio saved to {filtered_output_file}")

    # Decode the filtered audio
    decoder = Decoder()
    try:
        decoded_byte_data = decoder.decode_frequencies(filtered_output_file)
        print(f"Decoded byte data: {bytes(decoded_byte_data)}")


    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
