# Adaptive AI Quiz Game

## Overview

An intelligent quiz game application that dynamically adjusts difficulty based on user performance. The application features a tkinter-based GUI and implements an adaptive learning system that tracks user answers across three difficulty levels (easy, medium, hard). The game promotes users to harder levels when they demonstrate high accuracy and demotes them to easier levels when accuracy drops, creating a personalized learning experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Modular Architecture**: The application follows a component-based design with clear separation of concerns across four main modules:

- `QuizGame`: Main GUI controller and game orchestration
- `QuestionManager`: Question loading and selection logic
- `DifficultyManager`: Adaptive difficulty adjustment algorithm
- `UserProgress`: Statistics tracking and persistence

**GUI Framework**: Uses tkinter for the desktop interface, providing a cross-platform solution with built-in Python support. The interface is designed with responsive layouts using grid geometry management.

**Data Storage**: File-based JSON storage for questions and user statistics, eliminating the need for external database dependencies. Questions are organized in separate files by difficulty level for easy maintenance and expansion.

**Adaptive Learning Algorithm**: Implements a sliding window performance tracker that:
- Monitors the last 5 answers for statistical relevance
- Uses 80% accuracy threshold for promotion to harder levels
- Uses 40% accuracy threshold for demotion to easier levels
- Includes anti-oscillation mechanisms to prevent rapid difficulty changes

**State Management**: Centralized game state tracking including current question, user selections, performance metrics, and session statistics. Progress is persisted between sessions through JSON file storage.

### Design Patterns

**Manager Pattern**: Each major functionality area is encapsulated in its own manager class, promoting code reusability and testability.

**Observer Pattern**: The difficulty manager observes user performance and automatically adjusts game parameters without tight coupling to the GUI layer.

**Data Access Layer**: Question and user data access is abstracted through dedicated manager classes, allowing for easy data source changes in the future.

## External Dependencies

**Standard Library Only**: The application exclusively uses Python's standard library components:
- `tkinter` and `tkinter.ttk` for GUI components
- `json` for data serialization and file I/O
- `os` for file system operations
- `random` for question selection randomization
- `datetime` for timestamp tracking
- `typing` for type hints and code documentation

**File System Dependencies**: Requires read/write access to a local `data/` directory for storing question databases and user progress. The application automatically creates necessary directories and files with default content if they don't exist.

**No Network Dependencies**: Operates entirely offline with no external API calls, web services, or internet connectivity requirements.