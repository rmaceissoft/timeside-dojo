# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Reiner Marquez

#
# Process a WAV file and gather the following output
# - BPM (Beats Per Minute)
# - Waveform
# - Outputs the audio as an Mp3 at 320kbps bit rate

import logging
import os

from timeside.core import get_processor
from timeside.core.tools.test_samples import samples


OUTPUT_DIR = './output/'

logger = logging.getLogger(__name__)


def process_wav(wavfile):
    # if not os.path.isdir(OUTPUT_DIR):
    #    os.makedirs(OUTPUT_DIR)

    # TODO: set bit rate for mp3 file to 320kbps
    # TODO: calculate BPM
    decoder = get_processor('file_decoder')(wavfile)

    result_dir = os.path.join(OUTPUT_DIR, decoder.sha1)
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

    grapher = get_processor('waveform_simple')()
    analyzer_aubio_temporal = get_processor('aubio_temporal')()
    analyzer_aubio_mfcc = get_processor('aubio_mfcc')()
    encoder = get_processor('mp3_encoder')(os.path.join(result_dir, 'encoded.mp3'))

    pipe = decoder | grapher | analyzer_aubio_temporal | analyzer_aubio_mfcc | encoder
    pipe.run(samplerate=44100)
    grapher.render(os.path.join(result_dir, 'waveform_simple.png'))
    for res_uuid, result in pipe.results.items():
        result_path = os.path.join(result_dir, res_uuid + '.yaml')
        result.to_yaml(result_path)


if __name__ == "__main__":
    # processing all samples files included into timeside
    logger.debug('Start to process all timeside test samples')
    for key in samples.keys():
        logger.debug('Processing %s', key)
        process_wav(samples[key])
