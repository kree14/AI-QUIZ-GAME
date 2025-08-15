"""
User Progress Manager for tracking and persisting user statistics
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime

class UserProgress:
    def __init__(self):
        self.data_dir = "data"
        self.stats_file = "user_stats.json"
        self.stats_path = os.path.join(self.data_dir, self.stats_file)
        
        # Ensure data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_stats(self) -> Optional[Dict]:
        """Load user statistics from file"""
        try:
            if os.path.exists(self.stats_path):
                with open(self.stats_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Create initial stats file
                initial_stats = self._get_initial_stats()
                self.save_stats(initial_stats)
                return initial_stats
                
        except Exception as e:
            print(f"Error loading user stats: {str(e)}")
            return None
    
    def save_stats(self, stats: Dict) -> bool:
        """Save user statistics to file"""
        try:
            # Add timestamp
            stats['last_updated'] = datetime.now().isoformat()
            
            # Load existing stats to preserve history
            existing_stats = {}
            if os.path.exists(self.stats_path):
                try:
                    with open(self.stats_path, 'r', encoding='utf-8') as file:
                        existing_stats = json.load(file)
                except:
                    pass
            
            # Update with new stats
            updated_stats = self._merge_stats(existing_stats, stats)
            
            # Save to file
            with open(self.stats_path, 'w', encoding='utf-8') as file:
                json.dump(updated_stats, file, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving user stats: {str(e)}")
            return False
    
    def _get_initial_stats(self) -> Dict:
        """Get initial user statistics"""
        return {
            'current_level': 'easy',
            'questions_answered': 0,
            'correct_answers': 0,
            'total_score': 0,
            'sessions_played': 0,
            'best_accuracy': 0.0,
            'level_statistics': {
                'easy': {'questions': 0, 'correct': 0},
                'medium': {'questions': 0, 'correct': 0},
                'hard': {'questions': 0, 'correct': 0}
            },
            'created_date': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def _merge_stats(self, existing: Dict, new: Dict) -> Dict:
        """Merge new statistics with existing ones"""
        # Start with existing stats
        merged = existing.copy()
        
        # Update basic stats
        merged['current_level'] = new.get('current_level', existing.get('current_level', 'easy'))
        merged['questions_answered'] = existing.get('questions_answered', 0) + new.get('questions_answered', 0)
        merged['correct_answers'] = existing.get('correct_answers', 0) + new.get('correct_answers', 0)
        merged['total_score'] = existing.get('total_score', 0) + new.get('total_score', 0)
        
        # Increment sessions if this is a new session
        if new.get('questions_answered', 0) > 0:
            merged['sessions_played'] = existing.get('sessions_played', 0) + 1
        
        # Update best accuracy
        if merged['questions_answered'] > 0:
            current_accuracy = (merged['correct_answers'] / merged['questions_answered']) * 100
            merged['best_accuracy'] = max(existing.get('best_accuracy', 0), current_accuracy)
        
        # Update level statistics (simplified for now)
        if 'level_statistics' not in merged:
            merged['level_statistics'] = {
                'easy': {'questions': 0, 'correct': 0},
                'medium': {'questions': 0, 'correct': 0},
                'hard': {'questions': 0, 'correct': 0}
            }
        
        # Update timestamp
        merged['last_updated'] = new.get('last_updated', datetime.now().isoformat())
        
        return merged
    
    def get_user_summary(self) -> Dict:
        """Get a summary of user progress"""
        stats = self.load_stats()
        if not stats:
            return {}
        
        summary = {
            'total_questions': stats.get('questions_answered', 0),
            'total_correct': stats.get('correct_answers', 0),
            'overall_accuracy': 0.0,
            'current_level': stats.get('current_level', 'easy'),
            'total_score': stats.get('total_score', 0),
            'sessions_played': stats.get('sessions_played', 0),
            'best_accuracy': stats.get('best_accuracy', 0.0)
        }
        
        if summary['total_questions'] > 0:
            summary['overall_accuracy'] = (summary['total_correct'] / summary['total_questions']) * 100
        
        return summary
    
    def reset_stats(self) -> bool:
        """Reset user statistics to initial state"""
        try:
            initial_stats = self._get_initial_stats()
            return self.save_stats(initial_stats)
        except Exception as e:
            print(f"Error resetting stats: {str(e)}")
            return False
    
    def export_stats(self, filepath: str) -> bool:
        """Export user statistics to a specified file"""
        try:
            stats = self.load_stats()
            if stats:
                with open(filepath, 'w', encoding='utf-8') as file:
                    json.dump(stats, file, indent=2, ensure_ascii=False)
                return True
            return False
        except Exception as e:
            print(f"Error exporting stats: {str(e)}")
            return False
