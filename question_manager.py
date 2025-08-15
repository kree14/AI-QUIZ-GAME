"""
Question Manager for handling question loading and selection
"""

import json
import os
import random
from typing import Dict, List, Optional

class QuestionManager:
    def __init__(self):
        self.questions: Dict[str, List[Dict]] = {
            'easy': [],
            'medium': [],
            'hard': []
        }
        self.data_dir = "data"
        
    def load_questions(self) -> bool:
        """Load questions from JSON files"""
        try:
            # Create data directory if it doesn't exist
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            
            # Load questions for each difficulty level
            for level in ['easy', 'medium', 'hard']:
                filename = f"questions_{level}.json"
                filepath = os.path.join(self.data_dir, filename)
                
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as file:
                        questions_data = json.load(file)
                        self.questions[level] = questions_data.get('questions', [])
                else:
                    # Create default questions if file doesn't exist
                    self._create_default_questions(level, filepath)
            
            return True
            
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
            return False
    
    def _create_default_questions(self, level: str, filepath: str):
        """Create default questions for a difficulty level"""
        default_questions = self._get_default_questions(level)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(default_questions, file, indent=2, ensure_ascii=False)
            
            self.questions[level] = default_questions.get('questions', [])
            
        except Exception as e:
            print(f"Error creating default questions for {level}: {str(e)}")
    
    def _get_default_questions(self, level: str) -> Dict:
        """Get default questions for each difficulty level"""
        
        if level == 'easy':
            return {
                "questions": [
                    {
                        "question": "What is the capital of France?",
                        "options": ["London", "Berlin", "Paris", "Madrid"],
                        "correct_answer": "Paris",
                        "difficulty": "easy"
                    },
                    {
                        "question": "What is 2 + 2?",
                        "options": ["3", "4", "5", "6"],
                        "correct_answer": "4",
                        "difficulty": "easy"
                    },
                    {
                        "question": "Which planet is closest to the Sun?",
                        "options": ["Venus", "Earth", "Mercury", "Mars"],
                        "correct_answer": "Mercury",
                        "difficulty": "easy"
                    },
                    {
                        "question": "What color do you get when you mix red and yellow?",
                        "options": ["Green", "Orange", "Purple", "Blue"],
                        "correct_answer": "Orange",
                        "difficulty": "easy"
                    },
                    {
                        "question": "How many days are in a week?",
                        "options": ["5", "6", "7", "8"],
                        "correct_answer": "7",
                        "difficulty": "easy"
                    }
                ]
            }
        
        elif level == 'medium':
            return {
                "questions": [
                    {
                        "question": "Who painted the Mona Lisa?",
                        "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
                        "correct_answer": "Leonardo da Vinci",
                        "difficulty": "medium"
                    },
                    {
                        "question": "What is the square root of 64?",
                        "options": ["6", "7", "8", "9"],
                        "correct_answer": "8",
                        "difficulty": "medium"
                    },
                    {
                        "question": "Which element has the chemical symbol 'O'?",
                        "options": ["Osmium", "Oxygen", "Gold", "Silver"],
                        "correct_answer": "Oxygen",
                        "difficulty": "medium"
                    },
                    {
                        "question": "In which year did World War II end?",
                        "options": ["1944", "1945", "1946", "1947"],
                        "correct_answer": "1945",
                        "difficulty": "medium"
                    },
                    {
                        "question": "What is the largest mammal in the world?",
                        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                        "correct_answer": "Blue Whale",
                        "difficulty": "medium"
                    }
                ]
            }
        
        else:  # hard
            return {
                "questions": [
                    {
                        "question": "What is the time complexity of quicksort in the average case?",
                        "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
                        "correct_answer": "O(n log n)",
                        "difficulty": "hard"
                    },
                    {
                        "question": "Which of these is NOT a fundamental force in physics?",
                        "options": ["Electromagnetic", "Strong nuclear", "Centrifugal", "Gravitational"],
                        "correct_answer": "Centrifugal",
                        "difficulty": "hard"
                    },
                    {
                        "question": "What is the molecular formula for glucose?",
                        "options": ["C₆H₁₂O₆", "C₂H₆O", "H₂SO₄", "NaCl"],
                        "correct_answer": "C₆H₁₂O₆",
                        "difficulty": "hard"
                    },
                    {
                        "question": "In which programming paradigm is 'recursion' most commonly used?",
                        "options": ["Object-oriented", "Functional", "Procedural", "Assembly"],
                        "correct_answer": "Functional",
                        "difficulty": "hard"
                    },
                    {
                        "question": "What is the Heisenberg Uncertainty Principle related to?",
                        "options": ["Thermodynamics", "Quantum mechanics", "Relativity", "Classical mechanics"],
                        "correct_answer": "Quantum mechanics",
                        "difficulty": "hard"
                    }
                ]
            }
    
    def get_random_question(self, difficulty: str) -> Optional[Dict]:
        """Get a random question from the specified difficulty level"""
        if difficulty not in self.questions or not self.questions[difficulty]:
            return None
        
        return random.choice(self.questions[difficulty])
    
    def get_question_count(self, difficulty: str) -> int:
        """Get the number of questions for a difficulty level"""
        return len(self.questions.get(difficulty, []))
    
    def add_question(self, difficulty: str, question_data: Dict) -> bool:
        """Add a new question to the specified difficulty level"""
        try:
            if difficulty not in self.questions:
                return False
            
            # Add to memory
            self.questions[difficulty].append(question_data)
            
            # Save to file
            filename = f"questions_{difficulty}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            questions_data = {"questions": self.questions[difficulty]}
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(questions_data, file, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error adding question: {str(e)}")
            return False
