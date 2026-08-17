"""YouTube helpers: parse a video id from a link and fetch its transcript."""

import re
import sys

# Matches the video id in the common YouTube URL shapes:
# youtu.be/<id>, watch?v=<id>, /embed/<id>, /shorts/<id>, /live/<id>
_ID_PATTERNS = [
    re.compile(r"(?:v=|/embed/|/shorts/|/live/|youtu\.be/)([0-9A-Za-z_-]{11})"),
]


def extract_video_id(url: str) -> str | None:
    """Return the 11-character YouTube video id found in ``url``, or None."""
    url = url.strip()
    for pattern in _ID_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    # Bare id pasted directly.
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url):
        return url
    return None


def fetch_transcript(video_id: str) -> str:
    """Fetch and flatten a video's transcript into a single string of text.

    Works with both the modern (1.x, instance ``.fetch``) and legacy
    (classmethod ``.get_transcript``) youtube-transcript-api APIs.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("The 'youtube-transcript-api' package is not installed.")
        sys.exit(1)

    try:
        api = YouTubeTranscriptApi()
        if hasattr(api, "fetch"):
            fetched = api.fetch(video_id)
            text = " ".join(snippet.text for snippet in fetched)
        else:
            segments = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join(seg["text"] for seg in segments)
    except Exception as e:  # transcripts disabled, none found, network, etc.
        print(f"Could not fetch transcript for this video: {e}")
        sys.exit(1)

    text = text.strip()
    if not text:
        print("The transcript for this video was empty. Exiting.")
        sys.exit(1)
    return text
