from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def get_transcript(video_id: str) -> Optional[str]:
    try:
        # For newer versions of youtube-transcript-api
        transcript_api = YouTubeTranscriptApi()
        transcript = transcript_api.fetch(video_id)
        return " ".join(snippet.text for snippet in transcript.snippets)
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Transcript error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    print(get_transcript("liJVSwOiiwg"))

