"""
Main Quiz Game class handling the GUI and game logic
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Dict, List, Optional

from question_manager import QuestionManager
from difficulty_manager import DifficultyManager
from user_progress import UserProgress

class QuizGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.question_manager = QuestionManager()
        self.difficulty_manager = DifficultyManager()
        self.user_progress = UserProgress()
        
        # Game state variables
        self.current_question: Optional[Dict] = None
        self.selected_answer = tk.StringVar()
        self.game_active = False
        self.questions_answered = 0
        self.correct_answers = 0
        
        # Initialize the GUI
        self.setup_gui()
        self.load_initial_data()
        
    def setup_gui(self):
        """Setup the main GUI components"""
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="WENS")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Adaptive AI Quiz Game", 
                               font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=1, column=0, sticky="WE", pady=(0, 20))
        stats_frame.columnconfigure(1, weight=1)
        
        # Statistics labels
        ttk.Label(stats_frame, text="Current Level:").grid(row=0, column=0, sticky=tk.W)
        self.level_label = ttk.Label(stats_frame, text="Easy", font=('Arial', 10, 'bold'))
        self.level_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Questions Answered:").grid(row=1, column=0, sticky=tk.W)
        self.questions_count_label = ttk.Label(stats_frame, text="0")
        self.questions_count_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Accuracy:").grid(row=2, column=0, sticky=tk.W)
        self.accuracy_label = ttk.Label(stats_frame, text="0%")
        self.accuracy_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(stats_frame, text="Score:").grid(row=3, column=0, sticky=tk.W)
        self.score_label = ttk.Label(stats_frame, text="0")
        self.score_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        # Question frame
        self.question_frame = ttk.LabelFrame(main_frame, text="Question", padding="15")
        self.question_frame.grid(row=2, column=0, sticky="WENS", pady=(0, 20))
        self.question_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Question text
        self.question_label = ttk.Label(self.question_frame, text="Click 'Start Quiz' to begin!", 
                                       font=('Arial', 14), wraplength=700, justify=tk.CENTER)
        self.question_label.grid(row=0, column=0, pady=(0, 20))
        
        # Answer options frame
        self.answers_frame = ttk.Frame(self.question_frame)
        self.answers_frame.grid(row=1, column=0, sticky="WE")
        self.answers_frame.columnconfigure(0, weight=1)
        
        # Answer radio buttons (will be created dynamically)
        self.answer_buttons: List[ttk.Radiobutton] = []
        
        # Feedback label
        self.feedback_label = ttk.Label(self.question_frame, text="", 
                                       font=('Arial', 12, 'bold'))
        self.feedback_label.grid(row=2, column=0, pady=(20, 0))
        
        # Control buttons frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, pady=(0, 10))
        
        # Control buttons
        self.start_button = ttk.Button(controls_frame, text="Start Quiz", 
                                      command=self.start_quiz)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.submit_button = ttk.Button(controls_frame, text="Submit Answer", 
                                       command=self.submit_answer, state=tk.DISABLED)
        self.submit_button.grid(row=0, column=1, padx=(0, 10))
        
        self.next_button = ttk.Button(controls_frame, text="Next Question", 
                                     command=self.next_question, state=tk.DISABLED)
        self.next_button.grid(row=0, column=2, padx=(0, 10))
        
        self.reset_button = ttk.Button(controls_frame, text="Reset Game", 
                                      command=self.reset_game)
        self.reset_button.grid(row=0, column=3)
        
    def load_initial_data(self):
        """Load initial game data"""
        try:
            # Load questions
            if not self.question_manager.load_questions():
                messagebox.showerror("Error", "Failed to load questions. Please check the data files.")
                return
            
            # Load user progress
            stats = self.user_progress.load_stats()
            if stats:
                self.difficulty_manager.current_level = stats.get('current_level', 'easy')
                self.update_statistics()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load initial data: {str(e)}")
    
    def start_quiz(self):
        """Start or restart the quiz"""
        self.game_active = True
        self.questions_answered = 0
        self.correct_answers = 0
        
        # Update button states
        self.start_button.configure(state=tk.DISABLED)
        self.submit_button.configure(state=tk.NORMAL)
        
        # Clear feedback
        self.feedback_label.configure(text="")
        
        # Load first question
        self.load_next_question()
        
    def load_next_question(self):
        """Load the next question based on current difficulty"""
        try:
            current_level = self.difficulty_manager.current_level
            self.current_question = self.question_manager.get_random_question(current_level)
            
            if not self.current_question:
                messagebox.showerror("Error", f"No questions available for level: {current_level}")
                self.end_quiz()
                return
            
            # Display the question
            self.display_question()
            
            # Update statistics
            self.update_statistics()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load question: {str(e)}")
            self.end_quiz()
    
    def display_question(self):
        """Display the current question and answer options"""
        if not self.current_question:
            return
        
        # Set question text
        self.question_label.configure(text=self.current_question['question'])
        
        # Clear previous answer buttons
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons.clear()
        
        # Reset selected answer
        self.selected_answer.set("")
        
        # Create new answer buttons
        options = self.current_question['options']
        for i, option in enumerate(options):
            button = ttk.Radiobutton(self.answers_frame, text=option, 
                                   variable=self.selected_answer, value=option)
            button.grid(row=i, column=0, sticky=tk.W, pady=2)
            self.answer_buttons.append(button)
        
        # Enable submit button, disable next button
        self.submit_button.configure(state=tk.NORMAL)
        self.next_button.configure(state=tk.DISABLED)
        
        # Clear feedback
        self.feedback_label.configure(text="")
    
    def submit_answer(self):
        """Submit and check the current answer"""
        if not self.selected_answer.get():
            messagebox.showwarning("Warning", "Please select an answer before submitting.")
            return
        
        if not self.current_question:
            return
        
        # Check if answer is correct
        is_correct = self.selected_answer.get() == self.current_question['correct_answer']
        
        # Update counters
        self.questions_answered += 1
        if is_correct:
            self.correct_answers += 1
        
        # Show feedback
        if is_correct:
            self.feedback_label.configure(text="✓ Correct!", foreground="green")
        else:
            correct_answer = self.current_question['correct_answer']
            self.feedback_label.configure(
                text=f"✗ Incorrect! The correct answer was: {correct_answer}", 
                foreground="red"
            )
        
        # Update difficulty based on performance
        self.difficulty_manager.update_difficulty(is_correct)
        
        # Update statistics
        self.update_statistics()
        
        # Update button states
        self.submit_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.NORMAL)
        
        # Save progress
        self.save_progress()
    
    def next_question(self):
        """Move to the next question"""
        self.load_next_question()
    
    def update_statistics(self):
        """Update the statistics display"""
        # Update level
        level_display = self.difficulty_manager.current_level.capitalize()
        self.level_label.configure(text=level_display)
        
        # Update questions count
        self.questions_count_label.configure(text=str(self.questions_answered))
        
        # Update accuracy
        if self.questions_answered > 0:
            accuracy = (self.correct_answers / self.questions_answered) * 100
            self.accuracy_label.configure(text=f"{accuracy:.1f}%")
        else:
            self.accuracy_label.configure(text="0%")
        
        # Update score (could be more sophisticated)
        score = self.correct_answers * 10
        if self.difficulty_manager.current_level == 'medium':
            score = self.correct_answers * 15
        elif self.difficulty_manager.current_level == 'hard':
            score = self.correct_answers * 20
        
        self.score_label.configure(text=str(score))
    
    def save_progress(self):
        """Save current progress to file"""
        try:
            stats = {
                'current_level': self.difficulty_manager.current_level,
                'questions_answered': self.questions_answered,
                'correct_answers': self.correct_answers,
                'total_score': int(self.score_label.cget('text'))
            }
            self.user_progress.save_stats(stats)
        except Exception as e:
            print(f"Warning: Failed to save progress: {str(e)}")
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game_active = False
        self.questions_answered = 0
        self.correct_answers = 0
        self.difficulty_manager.reset()
        
        # Reset GUI
        self.question_label.configure(text="Click 'Start Quiz' to begin!")
        self.feedback_label.configure(text="")
        
        # Clear answer buttons
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons.clear()
        
        # Reset button states
        self.start_button.configure(state=tk.NORMAL)
        self.submit_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.DISABLED)
        
        # Update statistics
        self.update_statistics()
        
        # Save reset progress
        self.save_progress()
    
    def end_quiz(self):
        """End the current quiz"""
        self.game_active = False
        self.start_button.configure(state=tk.NORMAL)
        self.submit_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.DISABLED)
