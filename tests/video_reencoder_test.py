import src.video_reencoder as vr
import pytest
import sys

def test_vr_reencode_valid_name():
    reencoder = vr.Video_reencoder()

    reencoder.reencode('videos')