import numpy as np
import soundfile as sf
from config import MAX_FREQ, MIN_FREQ, BYTE_DURATION, START_MARKER, END_MARKER


class Decoder:
    num_freqs = 256  # Number of possible byte values (0-255)

    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def decode_frequencies_from_audio(self, audio_data, sample_rate=44100, duration_per_byte=BYTE_DURATION):
        frequencies = np.linspace(MIN_FREQ, MAX_FREQ, Decoder.num_freqs)

        samples_per_byte = int(sample_rate * duration_per_byte)
        byte_data = []

        for i in range(0, len(audio_data), samples_per_byte):
            segment = audio_data[i:i + samples_per_byte]
            if len(segment) == samples_per_byte:
                spectrum = np.abs(np.fft.fft(segment))
                freqs = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)

                # Consider only positive frequencies
                positive_freqs = freqs[:len(freqs) // 2]
                positive_spectrum = spectrum[:len(spectrum) // 2]

                idx = np.argmax(positive_spectrum)
                dominant_freq = positive_freqs[idx]
                nearest_byte = self.find_nearest(frequencies, dominant_freq)

                if 0 <= nearest_byte < 256:
                    byte_data.append(nearest_byte)

        return byte_data

    def decode_frequencies(self, wav_filename, min_freq=MIN_FREQ, max_freq=MAX_FREQ, sample_rate=44100,
                           duration_per_byte=BYTE_DURATION):
        audio_data, _ = sf.read(wav_filename)
        return self.decode_frequencies_from_audio(audio_data, sample_rate, duration_per_byte)


# Example usage
if __name__ == "__main__":
    output_file = "encoded_frequencies.wav"
    decoder = Decoder()
    decoded_byte_data = decoder.decode_frequencies(output_file)
    print(f"Decoded byte data: {decoded_byte_data}")
