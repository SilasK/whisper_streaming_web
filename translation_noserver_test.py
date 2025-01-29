#!/usr/bin/env python3
import sys
import numpy as np
import librosa
from functools import lru_cache
import time
import logging
import threading
import sounddevice as sd
from pathlib import Path

SAMPLING_RATE = 16000
logger = logging.getLogger(__name__)


from src.translation.translation import TranslationPipeline
from src.whisper_streaming.whisper_online import *

@lru_cache(10**6)
def load_audio(fname, target_sr=SAMPLING_RATE):
    """
    Load an audio file and resample it to the target sampling rate.

    Args:
        fname (str): Path to the audio file.
        target_sr (int): Target sampling rate.

    Returns:
        np.ndarray: Audio data.
    """
    audio, sr_native = librosa.load(fname, sr=None, dtype=np.float32)
    if sr_native != target_sr:
        logger.debug(f"Resampling from {sr_native} Hz to {target_sr} Hz.")
        audio = librosa.resample(audio, orig_sr=sr_native, target_sr=target_sr)
    return audio

def play_audio(audio_path, beg=0):
    """
    Play audio from the specified path starting at the given time.

    Args:
        audio_path (str): Path to the audio file.
        beg (float): Start time in seconds.

    Example:
        >>> play_audio('path/to/audio.wav', 5)
    """
    try:
        audio = load_audio(audio_path)
        
        start_sample = int(beg * SAMPLING_RATE)
        if start_sample >= len(audio):
            logger.error("Start time exceeds audio length.")
            return
        logger.debug(f"Playing audio from {audio_path} starting at {beg} seconds.")
        
        
        sd.play(audio[start_sample:], SAMPLING_RATE)
        sd.wait()  # Wait until playback is finished
    except Exception as e:
        logger.error(f"Error playing audio: {e}")


def load_audio_chunk(fname, beg, end):
    audio = load_audio(fname)
    beg_s = int(beg * 16000)
    end_s = int(end * 16000)
    return audio[beg_s:end_s]



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_path",
        type=str,
        default='samples_jfk.wav',
        help="Filename of 16kHz mono channel wav, on which live streaming is simulated.",
    )
    add_shared_args(parser)
    parser.add_argument(
        "--start_at",
        type=float,
        default=0.0,
        help="Start processing audio at this time.",
    )
    parser.add_argument(
        "--offline", action="store_true", default=False, help="Offline mode."
    )
    parser.add_argument(
        "--comp_unaware",
        action="store_true",
        default=False,
        help="Computationally unaware simulation.",
    )

    args = parser.parse_args()

    # reset to store stderr to different file stream, e.g. open(os.devnull,"w")
    logfile = None # sys.stderr

    if args.offline and args.comp_unaware:
        logger.error(
            "No or one option from --offline and --comp_unaware are available, not both. Exiting."
        )
        sys.exit(1)


    set_logging(args, logger,others=["src.whisper_streaming.online_asr","src.translation.translation"])

    audio_path = args.audio_path


    duration = len(load_audio(audio_path)) / SAMPLING_RATE
    logger.info("Audio duration is: %2.2f seconds" % duration)



    asr, online = asr_factory(args, logfile=logfile)
    if args.vac:
        min_chunk = args.vac_chunk_size
    else:
        min_chunk = args.min_chunk_size


## Load translater

    translation_output_folder= Path("translations")
    translation_output_folder.mkdir(exist_ok=True, parents=True)

    translation_pipeline = TranslationPipeline("fr",["en","uk","de"],
                                               output_folder=translation_output_folder
                                   )
    translation_pipeline.start()



    # load the audio into the LRU cache before we start the timer
    a = load_audio_chunk(audio_path, 0, 1)

    # warm up the ASR because the very first transcribe takes much more time than the other
    asr.transcribe(a)

    beg = args.start_at
    start = time.time() - beg

    def output_transcript(o, now=None):
        # output format in stdout is like:
        # 4186.3606 0 1720 Takhle to je
        # - the first three words are:
        #    - emission time from beginning of processing, in milliseconds
        #    - beg and end timestamp of the text segment, as estimated by Whisper model. The timestamps are not accurate, but they're useful anyway
        # - the next words: segment transcript
        if now is None:
            now = time.time() - start
        if o[0] is not None:
            log_string = f"{now*1000:1.0f}, {o[0]*1000:1.0f}-{o[1]*1000:1.0f} ({(now-o[1]):+1.0f}s): {o[2]}"

            logger.debug(
                log_string
            )

            if logfile is not None:
                print(
                    log_string,
                    file=logfile,
                    flush=True,
                )

            translation_pipeline.put_text(o[2])
        else:
            # No text, so no output
            pass

    if args.offline:  ## offline mode processing (for testing/debugging)
        a = load_audio(audio_path)
        online.insert_audio_chunk(a)
        try:
            o = online.process_iter()
        except AssertionError as e:
            logger.error(f"assertion error: {repr(e)}")
        else:
            output_transcript(o)
        now = None
    elif args.comp_unaware:  # computational unaware mode
        end = beg + min_chunk
        while True:
            a = load_audio_chunk(audio_path, beg, end)
            online.insert_audio_chunk(a)
            try:
                o = online.process_iter()
            except AssertionError as e:
                logger.error(f"assertion error: {repr(e)}")
                pass
            else:
                output_transcript(o, now=end)

            logger.debug(f"## last processed {end:.2f}s")

            if end >= duration:
                break

            beg = end

            if end + min_chunk > duration:
                end = duration
            else:
                end += min_chunk
        now = duration

    else:  # online = simultaneous mode

        audio_thread = threading.Thread(target=play_audio,args=(audio_path,beg),daemon=True)
        audio_thread.start()

        end = 0
        while True:
            now = time.time() - start
            if now < end + min_chunk:
                time.sleep(min_chunk + end - now)
            end = time.time() - start
            a = load_audio_chunk(audio_path, beg, end)
            beg = end
            online.insert_audio_chunk(a)

            try:
                o = online.process_iter()
            except AssertionError as e:
                logger.error(f"assertion error: {e}")
                pass
            else:
                output_transcript(o)
            now = time.time() - start
            logger.debug(
                f"## last processed {end:.2f} s, now is {now:.2f}, the latency is {now-end:.2f}"
            )

            if end >= duration:
                break
        now = None

    o = online.finish()
    output_transcript(o, now=now)
