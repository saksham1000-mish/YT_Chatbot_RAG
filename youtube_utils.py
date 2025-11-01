from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def get_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=['en'], preserve_formatting=True)
        return " ".join(snippet.text for snippet in transcript_list)
    except TranscriptsDisabled:
        return "Transcript is disabled for this video."


