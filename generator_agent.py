"""
Generator Agent - Creates educational content for a given grade and topic
"""
import json
from groq import Groq
from typing import Dict, Any


class GeneratorAgent:
    """
    Generates educational content including explanations and MCQs
    tailored to the specified grade level.
    """
    
    def __init__(self, api_key: str):
        """Initialize the Generator Agent with Groq API key."""
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def generate(self, grade: int, topic: str, feedback: list = None) -> Dict[str, Any]:
        """
        Generate educational content for the given grade and topic.
        
        Args:
            grade: The grade level (e.g., 4 for Grade 4)
            topic: The educational topic (e.g., "Types of angles")
            feedback: Optional feedback from reviewer for refinement
            
        Returns:
            Dictionary with 'explanation' and 'mcqs' keys
        """
        # Build the prompt
        prompt = self._build_prompt(grade, topic, feedback)
        
        # Call Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational content creator. Generate age-appropriate educational content in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse the response
        content = response.choices[0].message.content
        
        # Extract JSON from the response
        try:
            # Try to find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                result = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: create structured output
            result = {
                "explanation": content,
                "mcqs": []
            }
        
        return result
    
    def _build_prompt(self, grade: int, topic: str, feedback: list = None) -> str:
        """Build the prompt for content generation."""
        base_prompt = f"""Generate educational content for Grade {grade} students about "{topic}".

IMPORTANT: Return ONLY a valid JSON object with this exact structure:
{{
  "explanation": "A clear, age-appropriate explanation of the concept (3-5 sentences)",
  "mcqs": [
    {{
      "question": "Question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option B"
    }},
    {{
      "question": "Question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option C"
    }},
    {{
      "question": "Question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }}
  ]
}}

Guidelines:
- Use simple vocabulary appropriate for Grade {grade} students
- Keep explanations clear and concise
- Generate exactly 3 MCQs
- Each MCQ must have exactly 4 options
- Questions should test understanding of the explained concepts
- Make sure the answer is one of the provided options (exact text match)"""

        if feedback:
            feedback_text = "\n".join(f"- {fb}" for fb in feedback)
            base_prompt += f"\n\nPREVIOUS FEEDBACK TO ADDRESS:\n{feedback_text}\n\nPlease revise the content addressing all the feedback points above."
        
        return base_prompt
