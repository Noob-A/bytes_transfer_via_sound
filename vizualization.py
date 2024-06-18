import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf


def plot_spectrogram(wav_filename):
    # Load the audio file
    y, sr = sf.read(wav_filename)

    # Compute the short-time Fourier transform (STFT)
    D = np.abs(librosa.stft(y))

    # Convert the amplitude to decibels
    DB = librosa.amplitude_to_db(D, ref=np.max)

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Display the spectrogram
    librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log')

    # Add a color bar
    plt.colorbar(format='%+2.0f dB')

    # Add labels and title
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')

    # Show the plot
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    output_file = "encoded_frequencies.wav"
    plot_spectrogram(output_file)
