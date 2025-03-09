from agno.agent import Agent
from agno.tools.toolkit import Toolkit
from agno.models.google import Gemini
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import re
from agno.utils.log import logger
import os
load_dotenv()

# Create directory for storage if it doesn't exist
os.makedirs("tmp", exist_ok=True)

class Youtube_tool(Toolkit):
    def __init__(self):
        super().__init__(name="yt_tool")
        self.register(self.get_youtube_transcript)

    def get_youtube_transcript(self, video_url: str, language: str = "en") -> str:
        """
        Gets transcript from a YouTube video URL.
        
        Args:
            video_url (str): The YouTube video URL or video ID
            language (str): The language code for captions (default: "en" for English)
            
        Returns:
            str: The transcript text from the YouTube video
        """
        try:
            # Extract video ID
            video_id = self._extract_video_id(video_url)
            
            if not video_id:
                return "Error: Could not extract video ID from the provided URL"
            
            logger.info(f"Getting transcript for YouTube video: {video_id}")
            
            # Get the transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            
            if not transcript_list:
                return f"No {language} captions found for this video."
            
            # Format the transcript
            transcript_text = ""
            for entry in transcript_list:
                transcript_text += f"{entry['text']} "
            
            return transcript_text.strip()
            
        except Exception as e:
            logger.warning(f"Failed to get YouTube transcript: {e}")
            return f"Error: {e}"
    
    def _extract_video_id(self, video_url: str) -> str:
        """
        Extracts the YouTube video ID from various URL formats or returns the ID if directly provided.
        """
        # Check if it's already just the ID (11 characters)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', video_url):
            return video_url
            
        # Try to extract from URL
        youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(youtube_regex, video_url)
        
        if match:
            return match.group(1)
        
        return None


agent = Agent(
    model=Gemini(id='gemini-2.0-flash'),
    # Add persistent storage using SQLite
    storage=SqliteAgentStorage(table_name="youtube_agent_sessions", db_file="tmp/youtube_agent_storage.db"),
    # Include chat history in messages sent to the model
    add_history_to_messages=True,
    # Number of previous responses to include
    num_history_responses=3,
    show_tool_calls=True,
    tools=[Youtube_tool()],
    instructions=[
        'You are a study assistant who can get captions from YouTube videos and help users understand them.',
        'Use the get_youtube_transcript tool whenever a user shares a YouTube URL to get the video transcript.',
        'When calling get_youtube_transcript, just pass the YouTube URL directly as the video_url parameter.',
        'Translate captions from Hindi or other languages to English when needed.',
        'After getting the transcript, summarize the key points of the video content.',
        'You maintain memory of previous conversations and can refer back to them when relevant.'
    ]
)

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("test:app", reload=True)