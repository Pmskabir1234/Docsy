import re
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeTranscriptApiException
from langchain_core.documents import Document
from pydantic import ValidationError

api = YouTubeTranscriptApi()


class YoutubeTranscript:

    def _get_video_id(self, url: str) -> str | dict:
        """Extracting the video id from the given url"""
        if not isinstance(url, str):
            return {}
        pattern = r'(?:v=|\/embed\/|\/shorts\/|youtu\.be\/|\/v\/|^)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        mark = url.find("v=")
        if mark != -1 and len(url) >= mark + 13:
            return url[mark+2:mark+13]
        return {}

    def get_transcript(self, url: str | dict) -> dict | list[Document]:
        v_id = self._get_video_id(url)
        if isinstance(v_id, dict) or not v_id:
            return {"error": "video not found!"}
        try:
            transcripts_list = api.list(v_id)
            transcript = [transcript.fetch() for transcript in transcripts_list if transcript.language_code.startswith("en")]

            if len(transcript) >= 1:
                documents = [
                    Document(
                        page_content=snippet.text,
                        metadata={
                            "source": url if isinstance(url, str) else f"https://www.youtube.com/watch?v={v_id}",
                            "start_time": snippet.start,
                            "duration": snippet.duration
                        }
                    ) for snippet in transcript[-1]
                ]
                return documents
            return {"error": "english caption not found!"}

        except (YouTubeTranscriptApiException, ValidationError) as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=P26AE7NLx4Q"
    t = YoutubeTranscript()
    a = t.get_transcript(url)
    print(a[0] if isinstance(a, list) and len(a) > 0 else a)






