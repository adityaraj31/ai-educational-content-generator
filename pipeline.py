from typing import Dict, Any, Tuple
from generator_agent import GeneratorAgent
from reviewer_agent import ReviewerAgent


class ContentPipeline:
    """
    Orchestrates the content generation and review process.
    Handles refinement if content fails review.
    """
    
    def __init__(self, api_key: str):
        """Initialize the pipeline with both agents."""
        self.generator = GeneratorAgent(api_key)
        self.reviewer = ReviewerAgent(api_key)
    
    def generate_content(
        self, 
        grade: int, 
        topic: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """
        Generate and review content, with one refinement pass if needed.
        
        Args:
            grade: The grade level
            topic: The educational topic
            
        Returns:
            Tuple of (initial_content, review_result, refined_content or None)
        """
        # Step 1: Generate initial content
        initial_content = self.generator.generate(grade, topic)
        
        # Step 2: Review the content
        review_result = self.reviewer.review(initial_content, grade, topic)
        
        # Step 3: Refine if needed (one pass only)
        refined_content = None
        if review_result["status"] == "fail" and review_result["feedback"]:
            # Generate refined content with feedback
            refined_content = self.generator.generate(
                grade, 
                topic, 
                feedback=review_result["feedback"]
            )
            
            # Review the refined content
            refined_review = self.reviewer.review(refined_content, grade, topic)
            
            # Return results with refined content and its review
            return (
                initial_content,
                review_result,
                refined_content,
                refined_review
            )
        
        # No refinement needed or done
        return (
            initial_content,
            review_result,
            refined_content,
            None  # No refined review
        )
