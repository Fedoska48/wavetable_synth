import numpy as np
import scipy.io.wavfile as wav


def interpolate_linearly(wave_table, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wave_table.shape[0]

    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    return truncated_index_weight * wave_table[
        truncated_index] + next_index_weight * wave_table[next_index]


def fade_in_out(signal, fade_length=1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_in, signal[-fade_length:])

    return signal

def sawtooth(x):
    return (x + np.pi) / np.pi % 2 - 1

def main():
    sample_rate = 44100
    # freq = 440
    freq = 220
    time = 3
    # waveform = np.sin
    waveform = sawtooth

    # create wavetable
    wavetable_length = 64
    # allocate wt, wt filled with zeros
    wave_table = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wave_table[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((time * sample_rate,))

    index = 0
    index_increment = freq * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wave_table[int(np.floor(index))]
        output[n] = interpolate_linearly(wave_table, index)
        index += index_increment
        index %= wavetable_length

    output = fade_in_out(output)

    wav.write('saw440hzInterpolatedLinearlyFaded.wav', sample_rate,
              output.astype(np.float32))

    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude


if __name__ == '__main__':
    main()
