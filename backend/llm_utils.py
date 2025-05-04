from typing import List, Dict
from langchain.llms import OpenAI
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class LLMProcessor:
    def __init__(self):
        """
        Initialize the LLM processor with both OpenAI and local model options.
        """
        self.openai_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="gpt-3.5-turbo"
        )
        
        # Initialize local model pipeline
        self.local_model = pipeline(
            "text-generation",
            model="gpt2",
            device=-1  # Use CPU
        )

    def generate_flashcards(self, text: str) -> List[Dict[str, str]]:
        """
        Generate flashcards from input text using the LLM.
        
        Args:
            text (str): Input text to generate flashcards from
            
        Returns:
            List[Dict[str, str]]: List of flashcard dictionaries with 'question' and 'answer'
        """
        try:
            # First try with OpenAI if API key is available
            if os.getenv('OPENAI_API_KEY'):
                prompt = f"""
                Generate flashcards from the following text:
                {text}
                
                Return a JSON array of objects with 'question' and 'answer' keys.
                """
                response = self.openai_client(prompt)
                return response
            
            # Fallback to local model
            prompt = f"Generate flashcards from: {text}"
            response = self.local_model(prompt, max_length=500)[0]['generated_text']
            return response
            
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            raise

# Singleton instance
llm_processor = LLMProcessor()
