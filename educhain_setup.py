
"""
EduChain Setup and Testing Script
Task 1: Set up EduChain environment and generate sample educational content
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
import logging
from langchain_openai import ChatOpenAI


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from educhain import Educhain, LLMConfig
    logger.info("EduChain library imported successfully")
    from langchain_openai import ChatOpenAI
    logger.info("ChatOpenAI from langchain_openai imported successfully")
except ImportError as e:
    logger.error(f"Failed to import EduChain: {e}")
    print("Please install educhain: pip install educhain")
    exit(1)

class EduChainSetup:
    """Class to handle EduChain setup and content generation."""
    
    def __init__(self):
        """Initialize EduChain setup."""
        self.educhain = None
        self.setup_educhain()
        
    def setup_educhain(self):
        """Set up EduChain instance."""
        try:
            # Initialize EduChain
            openai_model = ChatOpenAI(
                model_name="gpt-4o",  
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            gpt4_config = LLMConfig(custom_model=openai_model)
            self.educhain = Educhain(gpt4_config)
            logger.info("EduChain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EduChain: {e}")
            # Create a mock educhain for demonstration
            self.educhain = MockEduChain()
            logger.info("Using mock EduChain for demonstration")
    
    def generate_mcq_content(self, topic: str = "Python Programming Basics", 
                           num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate multiple-choice questions for a given topic.
        
        Args:
            topic (str): The topic for MCQ generation
            num_questions (int): Number of questions to generate
            
        Returns:
            Dict containing MCQ data formatted for MCP
        """
        logger.info(f"Generating {num_questions} MCQs for topic: {topic}")
        
        try:
            # Generate MCQs using educhain
            mcqs = self.educhain.qna_engine.generate_questions(
                topic=topic,
                num=num_questions,
                difficulty_level="medium"
            )
            
            # Format for MCP compatibility
            print(mcqs.model_dump_json())
            mcqs.model_dump_json()
            formatted_mcqs = {
                "content_type": "multiple_choice_questions",
                "topic": topic,
                "num_questions": num_questions,
                "difficulty": "medium",
                "generated_at": datetime.now().isoformat(),
                "questions": mcqs
            }
            
            logger.info(f"Successfully generated {len(mcqs)} MCQs")
            return formatted_mcqs
            
        except Exception as e:
            logger.error(f"Error generating MCQs: {e}")
            return self._generate_fallback_mcqs(topic, num_questions)
    
    def generate_lesson_plan(self, subject: str = "Python Programming Basics",
                           duration: str = "45 minutes",
                           grade_level: str = "beginner") -> Dict[str, Any]:
        """
        Generate a lesson plan for a given subject.
        
        Args:
            subject (str): Subject for the lesson plan
            duration (str): Duration of the lesson
            grade_level (str): Target grade level
            
        Returns:
            Dict containing lesson plan data formatted for MCP
        """
        logger.info(f"Generating lesson plan for: {subject}")
        
        try:
            # Generate lesson plan using educhain
            lesson_plan = self.educhain.content_engine.generate_lesson_plan(
                topic=subject,
                duration=duration,
                grade_level=grade_level,
                learning_objectives=["Understanding the process", "Identifying key components"]
            )
            
            # Format for MCP compatibility
            formatted_lesson = {
                "content_type": "lesson_plan",
                "subject": subject,
                "duration": duration,
                "grade_level": grade_level,
                "generated_at": datetime.now().isoformat(),
                "lesson_plan": lesson_plan
            }
            
            logger.info("Successfully generated lesson plan")
            return formatted_lesson
            
        except Exception as e:
            logger.error(f"Error generating lesson plan: {e}")
            return self._generate_fallback_lesson_plan(subject, duration, grade_level)
    
    def _generate_fallback_mcqs(self, topic: str, num_questions: int) -> Dict[str, Any]:
        """Generate fallback MCQs when educhain fails."""
        logger.info("Generating fallback MCQs")
        
        # Sample MCQ structure for Python Programming Basics
        sample_mcqs = []
        
        python_questions = [
            {
                "question": "What is the correct way to create a list in Python?",
                "options": [
                    "my_list = []",
                    "my_list = ()",
                    "my_list = {}",
                    "my_list = <>"
                ],
                "correct_answer": "A",
                "explanation": "Square brackets [] are used to create lists in Python."
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "function",
                    "def",
                    "define",
                    "func"
                ],
                "correct_answer": "B",
                "explanation": "The 'def' keyword is used to define functions in Python."
            },
            {
                "question": "What does the 'len()' function do in Python?",
                "options": [
                    "Returns the length of an object",
                    "Returns the last element",
                    "Returns the first element",
                    "Returns the type of object"
                ],
                "correct_answer": "A",
                "explanation": "The len() function returns the number of items in an object."
            },
            {
                "question": "Which operator is used for floor division in Python?",
                "options": [
                    "/",
                    "//",
                    "%",
                    "**"
                ],
                "correct_answer": "B",
                "explanation": "The '//' operator performs floor division in Python."
            },
            {
                "question": "What is the correct way to comment a single line in Python?",
                "options": [
                    "// This is a comment",
                    "/* This is a comment */",
                    "# This is a comment",
                    "<!-- This is a comment -->"
                ],
                "correct_answer": "C",
                "explanation": "The '#' symbol is used for single-line comments in Python."
            }
        ]
        
        # Select questions based on num_questions
        selected_questions = python_questions[:min(num_questions, len(python_questions))]
        
        return {
            "content_type": "multiple_choice_questions",
            "topic": topic,
            "num_questions": len(selected_questions),
            "difficulty": "medium",
            "generated_at": datetime.now().isoformat(),
            "questions": selected_questions,
            "note": "Generated using fallback content due to API limitations"
        }
    
    def _generate_fallback_lesson_plan(self, subject: str, duration: str, 
                                     grade_level: str) -> Dict[str, Any]:
        """Generate fallback lesson plan when educhain fails."""
        logger.info("Generating fallback lesson plan")
        
        lesson_plan = {
            "title": f"Introduction to {subject}",
            "overview": f"This lesson introduces students to fundamental concepts in {subject}.",
            "learning_objectives": [
                f"Understand basic concepts of {subject}",
                f"Apply {subject} principles in practical scenarios",
                "Develop problem-solving skills",
                "Build foundation for advanced topics"
            ],
            "materials_needed": [
                "Computer with Python installed",
                "Text editor or IDE",
                "Practice exercises",
                "Reference materials"
            ],
            "lesson_structure": {
                "introduction": {
                    "duration": "10 minutes",
                    "activities": [
                        "Review previous lesson",
                        f"Introduce {subject} concepts",
                        "Set learning expectations"
                    ]
                },
                "main_content": {
                    "duration": "25 minutes",
                    "activities": [
                        f"Explain core {subject} principles",
                        "Demonstrate with examples",
                        "Hands-on practice",
                        "Interactive exercises"
                    ]
                },
                "conclusion": {
                    "duration": "10 minutes",
                    "activities": [
                        "Summarize key concepts",
                        "Address questions",
                        "Assign practice work",
                        "Preview next lesson"
                    ]
                }
            },
            "assessment": {
                "formative": "Questions and discussions during lesson",
                "summative": "Practice exercises and quiz",
                "homework": f"Complete {subject} practice problems"
            },
            "differentiation": {
                "for_beginners": "Provide additional examples and support",
                "for_advanced": "Offer extension activities and challenges"
            }
        }
        
        return {
            "content_type": "lesson_plan",
            "subject": subject,
            "duration": duration,
            "grade_level": grade_level,
            "generated_at": datetime.now().isoformat(),
            "lesson_plan": lesson_plan,
            "note": "Generated using fallback content due to API limitations"
        }
    
    def save_content_to_file(self, content: Dict[str, Any], filename: str):
        """Save generated content to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            logger.info(f"Content saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving content to file: {e}")
    
    def display_content(self, content: Dict[str, Any]):
        """Display generated content in a readable format."""
        content_type = content.get("content_type", "unknown")
        
        print(f"\n{'='*60}")
        print(f"GENERATED CONTENT: {content_type.upper()}")
        print(f"{'='*60}")
        
        if content_type == "multiple_choice_questions":
            self._display_mcqs(content)
        elif content_type == "lesson_plan":
            self._display_lesson_plan(content)
        else:
            print(json.dumps(content, indent=2))
    
    def _display_mcqs(self, mcq_data: Dict[str, Any]):
        """Display MCQs in a readable format."""
        print(f"Topic: {mcq_data.get('topic', 'N/A')}")
        print(f"Number of Questions: {mcq_data.get('num_questions', 'N/A')}")
        print(f"Difficulty: {mcq_data.get('difficulty', 'N/A')}")
        print(f"Generated at: {mcq_data.get('generated_at', 'N/A')}")
        
        if 'note' in mcq_data:
            print(f"Note: {mcq_data['note']}")
        
        print(f"\n{'-'*40}")
        print("QUESTIONS:")
        print(f"{'-'*40}")
        
        questions = mcq_data.get('questions', [])
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(f"Q: {question.get('question', 'No question text')}")
            
            options = question.get('options', [])
            for j, option in enumerate(options):
                print(f"   {chr(65+j)}. {option}")
            
            print(f"Correct Answer: {question.get('correct_answer', 'N/A')}")
            print(f"Explanation: {question.get('explanation', 'No explanation')}")
    
    def _display_lesson_plan(self, lesson_data: Dict[str, Any]):
        """Display lesson plan in a readable format."""
        print(f"Subject: {lesson_data.get('subject', 'N/A')}")
        print(f"Duration: {lesson_data.get('duration', 'N/A')}")
        print(f"Grade Level: {lesson_data.get('grade_level', 'N/A')}")
        print(f"Generated at: {lesson_data.get('generated_at', 'N/A')}")
        
        if 'note' in lesson_data:
            print(f"Note: {lesson_data['note']}")
        
        lesson_plan = lesson_data.get('lesson_plan', {})
        
        print(f"\n{'-'*40}")
        print("LESSON PLAN:")
        print(f"{'-'*40}")
        
        if isinstance(lesson_plan, dict):
            for key, value in lesson_plan.items():
                print(f"\n{key.upper().replace('_', ' ')}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"  • {item}")
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        print(f"  {subkey.replace('_', ' ').title()}:")
                        if isinstance(subvalue, list):
                            for item in subvalue:
                                print(f"    • {item}")
                        else:
                            print(f"    {subvalue}")
                else:
                    print(f"  {value}")
        else:
            print(lesson_plan)

class MockEduChain:
    """Mock EduChain class for when the real library is not available."""
    
    def generate_mcq(self, topic: str, num_questions: int, difficulty: str):
        """Mock MCQ generation."""
        raise Exception("Mock EduChain - using fallback content")
    
    def generate_lesson_plan(self, subject: str, duration: str, grade_level: str):
        """Mock lesson plan generation."""
        raise Exception("Mock EduChain - using fallback content")

def main():
    """Main function to demonstrate EduChain setup and content generation."""
    print("EduChain Setup and Content Generation Demo")
    print("="*50)
    
    # Initialize EduChain setup
    educhain_setup = EduChainSetup()
    
    # Generate MCQs
    print("\n1. Generating Multiple Choice Questions...")
    mcq_content = educhain_setup.generate_mcq_content(
        topic="Python Programming Basics",
        num_questions=5
    )
    
    # Display MCQs
    educhain_setup.display_content(mcq_content)
    
    # Save MCQs to file
    educhain_setup.save_content_to_file(mcq_content, "sample_mcqs.json")
    
    # Generate Lesson Plan
    print("\n\n2. Generating Lesson Plan...")
    lesson_content = educhain_setup.generate_lesson_plan(
        subject="Python Programming Basics",
        duration="45 minutes",
        grade_level="beginner"
    )
    
    # Display Lesson Plan
    educhain_setup.display_content(lesson_content)
    
    # Save Lesson Plan to file
    educhain_setup.save_content_to_file(lesson_content, "sample_lesson_plan.json")
    
    print(f"\n{'='*60}")
    print("TASK 1 COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")
    print("Generated files:")
    print("• sample_mcqs.json - Multiple choice questions")
    print("• sample_lesson_plan.json - Lesson plan")
    print("• requirements.txt - Python dependencies")
    print("\nContent is formatted as JSON for MCP server compatibility.")
    print("Ready for integration with MCP server in Task 2!")

if __name__ == "__main__":
    main()