"""History manager for undo/redo functionality"""

import numpy as np
from typing import List, Optional, Dict, Any
import copy


class HistoryState:
    """Represents a single state in the history"""
    
    def __init__(self, image: np.ndarray, description: str = "", settings: Optional[Dict] = None):
        """
        Initialize history state.
        
        Args:
            image: Image data
            description: Description of this state
            settings: Dictionary of settings at this state
        """
        self.image = image.copy() if image is not None else None
        self.description = description
        self.settings = settings.copy() if settings else {}
        
    def get_image(self) -> Optional[np.ndarray]:
        """Get image copy"""
        return self.image.copy() if self.image is not None else None


class HistoryManager:
    """Manages undo/redo history for image editing"""
    
    def __init__(self, max_history: int = 50):
        """
        Initialize history manager.
        
        Args:
            max_history: Maximum number of history states to keep
        """
        self.max_history = max_history
        self.history: List[HistoryState] = []
        self.current_index = -1
        
    def add_state(self, image: np.ndarray, description: str = "", settings: Optional[Dict] = None):
        """
        Add a new state to history.
        
        Args:
            image: Current image
            description: Description of the action
            settings: Current settings
        """
        # Remove any states after current index (if we undid and then did a new action)
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        # Add new state
        state = HistoryState(image, description, settings)
        self.history.append(state)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_index += 1
        
        # Always keep current_index within bounds
        self.current_index = len(self.history) - 1
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return self.current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return self.current_index < len(self.history) - 1
    
    def undo(self) -> Optional[HistoryState]:
        """
        Undo to previous state.
        
        Returns:
            Previous history state or None
        """
        if not self.can_undo():
            return None
        
        self.current_index -= 1
        return self.history[self.current_index]
    
    def redo(self) -> Optional[HistoryState]:
        """
        Redo to next state.
        
        Returns:
            Next history state or None
        """
        if not self.can_redo():
            return None
        
        self.current_index += 1
        return self.history[self.current_index]
    
    def get_current_state(self) -> Optional[HistoryState]:
        """Get current state"""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None
    
    def get_history_list(self) -> List[str]:
        """
        Get list of history descriptions.
        
        Returns:
            List of state descriptions
        """
        return [state.description for state in self.history]
    
    def get_current_index(self) -> int:
        """Get current position in history"""
        return self.current_index
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self.current_index = -1
    
    def get_memory_usage(self) -> str:
        """
        Estimate memory usage of history.
        
        Returns:
            Human-readable memory usage string
        """
        total_bytes = 0
        for state in self.history:
            if state.image is not None:
                total_bytes += state.image.nbytes
        
        # Convert to MB
        mb = total_bytes / (1024 * 1024)
        return f"{mb:.2f} MB"
