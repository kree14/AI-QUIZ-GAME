"""
Difficulty Manager for adaptive AI difficulty adjustment
"""

from typing import List

class DifficultyManager:
    def __init__(self):
        self.current_level = 'easy'
        self.levels = ['easy', 'medium', 'hard']
        self.recent_performance: List[bool] = []  # Track recent answers (True = correct, False = incorrect)
        self.performance_window = 5  # Number of recent answers to consider
        self.promotion_threshold = 0.8  # 80% accuracy to move up
        self.demotion_threshold = 0.4  # Below 40% accuracy to move down
        
    def update_difficulty(self, is_correct: bool):
        """Update difficulty based on the latest answer"""
        # Add the latest result to performance tracking
        self.recent_performance.append(is_correct)
        
        # Keep only the most recent results within the window
        if len(self.recent_performance) > self.performance_window:
            self.recent_performance.pop(0)
        
        # Only adjust difficulty if we have enough data
        if len(self.recent_performance) >= self.performance_window:
            accuracy = sum(self.recent_performance) / len(self.recent_performance)
            
            current_index = self.levels.index(self.current_level)
            
            # Check for promotion (move to harder level)
            if accuracy >= self.promotion_threshold and current_index < len(self.levels) - 1:
                self.current_level = self.levels[current_index + 1]
                self._reset_performance_tracking()
                print(f"Difficulty increased to: {self.current_level}")
            
            # Check for demotion (move to easier level)
            elif accuracy <= self.demotion_threshold and current_index > 0:
                self.current_level = self.levels[current_index - 1]
                self._reset_performance_tracking()
                print(f"Difficulty decreased to: {self.current_level}")
    
    def _reset_performance_tracking(self):
        """Reset performance tracking after level change"""
        # Keep some recent performance to avoid rapid oscillation
        if len(self.recent_performance) > 2:
            self.recent_performance = self.recent_performance[-2:]
        else:
            self.recent_performance = []
    
    def get_current_accuracy(self) -> float:
        """Get current accuracy percentage"""
        if not self.recent_performance:
            return 0.0
        return (sum(self.recent_performance) / len(self.recent_performance)) * 100
    
    def get_difficulty_info(self) -> dict:
        """Get detailed information about current difficulty state"""
        return {
            'current_level': self.current_level,
            'level_index': self.levels.index(self.current_level),
            'total_levels': len(self.levels),
            'recent_accuracy': self.get_current_accuracy(),
            'questions_in_window': len(self.recent_performance),
            'window_size': self.performance_window
        }
    
    def force_level(self, level: str):
        """Force set the difficulty level (for testing or manual adjustment)"""
        if level in self.levels:
            self.current_level = level
            self.recent_performance = []
            print(f"Difficulty manually set to: {self.current_level}")
        else:
            print(f"Invalid difficulty level: {level}")
    
    def reset(self):
        """Reset difficulty manager to initial state"""
        self.current_level = 'easy'
        self.recent_performance = []
        print("Difficulty manager reset to easy level")
    
    def can_promote(self) -> bool:
        """Check if promotion to next level is possible"""
        current_index = self.levels.index(self.current_level)
        return current_index < len(self.levels) - 1
    
    def can_demote(self) -> bool:
        """Check if demotion to previous level is possible"""
        current_index = self.levels.index(self.current_level)
        return current_index > 0
    
    def get_next_level(self) -> str:
        """Get the next difficulty level (for promotion)"""
        current_index = self.levels.index(self.current_level)
        if current_index < len(self.levels) - 1:
            return self.levels[current_index + 1]
        return self.current_level
    
    def get_previous_level(self) -> str:
        """Get the previous difficulty level (for demotion)"""
        current_index = self.levels.index(self.current_level)
        if current_index > 0:
            return self.levels[current_index - 1]
        return self.current_level
