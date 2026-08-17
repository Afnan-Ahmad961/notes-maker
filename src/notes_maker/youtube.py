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


# Preferred transcript languages, in order. If none of these exist we fall back
# to whatever language the video actually has (Hindi, Urdu, etc.) — Gemini is
# instructed to produce the notes in English regardless of the source language.
_PREFERRED_LANGS = ["en", "en-US", "en-GB"]


def _flatten(fetched) -> str:
    """Join transcript snippets into one string, across old/new API return types."""
    parts = []
    for snippet in fetched:
        if hasattr(snippet, "text"):  # modern FetchedTranscript snippet objects
            parts.append(snippet.text)
        elif isinstance(snippet, dict):  # legacy list-of-dicts
            parts.append(snippet.get("text", ""))
    return " ".join(p for p in parts if p)


def _pick_transcript(transcript_list):
    """Choose an English transcript if available, else the first available one."""
    try:
        return transcript_list.find_transcript(_PREFERRED_LANGS)
    except Exception:
        pass
    for transcript in transcript_list:  # first available, any language
        return transcript
    return None


def fetch_transcript(video_id: str) -> str:
    """Fetch and flatten a video's transcript into a single string of text.

    Picks an English transcript when present, otherwise falls back to any
    available language. Works with both the modern (1.x, instance ``.list``)
    and legacy (classmethod ``.list_transcripts``/``.get_transcript``) APIs.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("The 'youtube-transcript-api' package is not installed.")
        sys.exit(1)

    try:
        api = YouTubeTranscriptApi()
        if hasattr(api, "list"):  # modern 1.x API
            transcript_list = api.list(video_id)
        elif hasattr(YouTubeTranscriptApi, "list_transcripts"):  # legacy API
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        else:  # very old API — only English is reachable
            transcript_list = None

        if transcript_list is not None:
            transcript = _pick_transcript(transcript_list)
            if transcript is None:
                print("No transcript is available for this video. Exiting.")
                sys.exit(1)
            text = _flatten(transcript.fetch())
        else:
            text = _flatten(YouTubeTranscriptApi.get_transcript(video_id))
    except SystemExit:
        raise
    except Exception as e:  # transcripts disabled, none found, network, etc.
        print(f"Could not fetch transcript for this video: {e}")
        sys.exit(1)

    text = text.strip()
    if not text:
        print("The transcript for this video was empty. Exiting.")
        sys.exit(1)
    return text
