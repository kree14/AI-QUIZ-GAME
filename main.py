#!/usr/bin/env python3
"""
Main entry point for the Adaptive AI Quiz Game
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from quiz_game import QuizGame

def main():
    """Main function to start the quiz game"""
    try:
        # Create the main window
        root = tk.Tk()
        root.title("Adaptive AI Quiz Game")
        root.geometry("800x600")
        root.resizable(True, True)
        
        # Center the window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (800 // 2)
        y = (root.winfo_screenheight() // 2) - (600 // 2)
        root.geometry(f"800x600+{x}+{y}")
        
        # Create and start the quiz game
        game = QuizGame(root)
        
        # Start the main event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the quiz game: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
