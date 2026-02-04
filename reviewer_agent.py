from groq import Groq
from typing import Dict, Any, List
import json


class ReviewerAgent:
    """
    Reviews educational content for age-appropriateness,
    conceptual correctness, and clarity.
    """
    
    def __init__(self, api_key: str):
        """Initialize the Reviewer Agent with Groq API key."""
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def review(self, content: Dict[str, Any], grade: int, topic: str) -> Dict[str, Any]:
        """
        Review the generated content.
        
        Args:
            content: The content to review (with 'explanation' and 'mcqs' keys)
            grade: The target grade level
            topic: The educational topic
            
        Returns:
            Dictionary with 'status' (pass/fail) and 'feedback' (list of issues)
        """
        prompt = self._build_review_prompt(content, grade, topic)
        
        # Call Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educational content reviewer. Evaluate content for age-appropriateness, conceptual correctness, and clarity. Return your review in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent evaluation
            max_tokens=1000
        )
        
        # Parse the response
        content_text = response.choices[0].message.content
        
        # Extract JSON from the response
        try:
            start_idx = content_text.find('{')
            end_idx = content_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                result = json.loads(content_text)
            
            # Ensure the result has required fields
            if "status" not in result or "feedback" not in result:
                result = {
                    "status": "fail",
                    "feedback": ["Invalid review format"]
                }
            
            # Normalize status
            if result["status"].lower() not in ["pass", "fail"]:
                result["status"] = "fail"
            else:
                result["status"] = result["status"].lower()
                
        except json.JSONDecodeError:
            # Fallback
            result = {
                "status": "fail",
                "feedback": ["Could not parse review response"]
            }
        
        return result
    
    def _build_review_prompt(self, content: Dict[str, Any], grade: int, topic: str) -> str:
        """Build the prompt for content review."""
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""Review the following educational content for Grade {grade} students about "{topic}".

CONTENT TO REVIEW:
{content_str}

EVALUATION CRITERIA:
1. Age Appropriateness: Is the language and complexity suitable for Grade {grade}?
2. Conceptual Correctness: Are the concepts explained accurately?
3. Clarity: Is the explanation clear and easy to understand?
4. MCQ Quality: 
   - Do questions test the explained concepts?
   - Are options clear and distinct?
   - Is the correct answer actually correct?
   - Are all 4 options provided for each question?

IMPORTANT: Return ONLY a valid JSON object with this exact structure:
{{
  "status": "pass or fail",
  "feedback": [
    "Specific issue 1 (if any)",
    "Specific issue 2 (if any)"
  ]
}}

Rules:
- Return "pass" ONLY if ALL criteria are met with no significant issues
- Return "fail" if there are ANY issues that need correction
- In the feedback array, list specific, actionable issues
- If status is "pass", feedback can be empty or contain minor suggestions
- Be specific about which part of the content has issues (e.g., "Sentence 2", "Question 3")
"""
        
        return prompt
