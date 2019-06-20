import pyesiaf
from .splitter import Splitter


SAMPLERATE_DICT = {
    8000: pyesiaf.Rate.RATE_8000,
    16000: pyesiaf.Rate.RATE_16000,
    32000: pyesiaf.Rate.RATE_32000,
    44100: pyesiaf.Rate.RATE_44100,
    48000: pyesiaf.Rate.RATE_48000,
    96000: pyesiaf.Rate.RATE_96000,
}

BITRATE_DICT = {
    'int8': pyesiaf.Bitrate.BIT_INT_8_SIGNED,
    'uint8': pyesiaf.Bitrate.BIT_INT_8_UNSIGNED,
    'int16': pyesiaf.Bitrate.BIT_INT_16_SIGNED,
    'uint16': pyesiaf.Bitrate.BIT_INT_16_UNSIGNED,
    'int24': pyesiaf.Bitrate.BIT_INT_24_SIGNED,
    'uint24': pyesiaf.Bitrate.BIT_INT_24_UNSIGNED,
    'int32': pyesiaf.Bitrate.BIT_INT_32_SIGNED,
    'uint32': pyesiaf.Bitrate.BIT_INT_32_UNSIGNED,
    'float32': pyesiaf.Bitrate.BIT_FLOAT_32,
    'float64': pyesiaf.Bitrate.BIT_FLOAT_64
}

ENDIAN_DICT = {
    'LE': pyesiaf.Endian.LittleEndian,
    'BE': pyesiaf.Endian.BigEndian
}


def create_esiaf_audio_format_from_dict(dict):
    sample_rate = SAMPLERATE_DICT[dict.pop('sample_rate', 16000)]
    bit_rate = BITRATE_DICT[dict.pop('bit_rate', 'int8')]
    endian = ENDIAN_DICT[dict.pop('endian', 'LE')]
    channels = dict.pop('channels', 1)

    esiaf_format = pyesiaf.EsiafAudioFormat()
    esiaf_format.rate = sample_rate
    esiaf_format.bitrate = bit_rate
    esiaf_format.endian = endian
    esiaf_format.channels = channels

    return esiaf_format