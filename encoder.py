import numpy as np
import soundfile as sf
from config import MAX_FREQ, MIN_FREQ, AMPLITUDE, BYTE_DURATION, START_MARKER, END_MARKER


class Encoder:
    num_freqs = 256  # Number of possible byte values (0-255)

    @staticmethod
    def encode_bytes_to_frequencies(byte_data, min_freq=MIN_FREQ, max_freq=MAX_FREQ):
        frequencies = np.linspace(min_freq, max_freq, Encoder.num_freqs)
        return [frequencies[byte] for byte in byte_data]

    @staticmethod
    def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=AMPLITUDE):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
        return wave

    @staticmethod
    def apply_fade(wave, sample_rate, fade_duration=0.01):
        fade_samples = int(sample_rate * fade_duration)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out
        return wave

    def bytes_to_wav(self, byte_data, output_filename, sample_rate=44100, duration_per_byte=BYTE_DURATION):
        # Add start and end markers to the byte data
        byte_data = bytes([START_MARKER]) + byte_data + bytes([END_MARKER])

        encoded_frequencies = self.encode_bytes_to_frequencies(byte_data)

        audio_data = []
        for freq in encoded_frequencies:
            sine_wave = self.generate_sine_wave(freq, duration_per_byte, sample_rate)
            sine_wave = self.apply_fade(sine_wave, sample_rate)
            audio_data.extend(sine_wave)

        audio_data = np.array(audio_data)

        # Ensure the audio data is in floating-point format
        audio_data = np.float32(audio_data)

        # Write the floating-point audio data to a WAV file using soundfile
        sf.write(output_filename, audio_data, sample_rate, subtype='FLOAT')


# Example usage
if __name__ == "__main__":
    byte_data = b"Hello, World!"
    output_file = "encoded_frequencies.wav"
    encoder = Encoder()
    encoder.bytes_to_wav(byte_data, output_file)
    print(f"Encoded WAV file written to {output_file}")
