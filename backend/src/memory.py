import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from .config.settings import settings

class StudyMemory:
    """
    Custom file-based memory system for multi-agent study sessions.
    Stores session context, agent outputs, and conversation history.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.memory_dir = settings.output_dir / "memory" / session_id
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.context_file = self.memory_dir / "context.json"
        self.agent_outputs_file = self.memory_dir / "agent_outputs.json"
        self.conversation_file = self.memory_dir / "conversation.json"
        
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load existing memory or initialize new session"""
        if self.context_file.exists():
            with open(self.context_file, 'r', encoding='utf-8') as f:
                self.context = json.load(f)
        else:
            self.context = {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "topic": "",
                "notes": "",
                "metadata": {}
            }
            self._save_context()
        
        if self.agent_outputs_file.exists():
            with open(self.agent_outputs_file, 'r', encoding='utf-8') as f:
                self.agent_outputs = json.load(f)
        else:
            self.agent_outputs = []
            self._save_agent_outputs()
        
        if self.conversation_file.exists():
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                self.conversation = json.load(f)
        else:
            self.conversation = []
            self._save_conversation()
    
    def _save_context(self):
        """Persist context to disk"""
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
    
    def _save_agent_outputs(self):
        """Persist agent outputs to disk"""
        with open(self.agent_outputs_file, 'w', encoding='utf-8') as f:
            json.dump(self.agent_outputs, f, indent=2, ensure_ascii=False)
    
    def _save_conversation(self):
        """Persist conversation history to disk"""
        with open(self.conversation_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation, f, indent=2, ensure_ascii=False)
    
    def set_session_context(self, topic: str, notes: str, metadata: Optional[Dict] = None):
        """Set the session context (topic, notes, metadata)"""
        self.context["topic"] = topic
        self.context["notes"] = notes
        if metadata:
            self.context["metadata"].update(metadata)
        self._save_context()
    
    def add_agent_output(self, agent_name: str, task: str, output: str):
        """Store output from a specific agent"""
        entry = {
            "agent": agent_name,
            "task": task,
            "output": output,
            "timestamp": datetime.now().isoformat()
        }
        self.agent_outputs.append(entry)
        self._save_agent_outputs()
    
    def get_agent_outputs(self, agent_name: Optional[str] = None) -> List[Dict]:
        """Retrieve outputs from a specific agent or all agents"""
        if agent_name:
            return [o for o in self.agent_outputs if o["agent"] == agent_name]
        return self.agent_outputs
    
    def add_conversation_turn(self, role: str, content: str):
        """Add a conversation turn (user or assistant)"""
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation.append(entry)
        self._save_conversation()
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Retrieve conversation history"""
        if last_n:
            return self.conversation[-last_n:]
        return self.conversation
    
    def get_context_summary(self) -> str:
        """Generate a text summary of the current context"""
        return f"""
Session ID: {self.session_id}
Topic: {self.context.get('topic', 'N/A')}
Created: {self.context.get('created_at', 'N/A')}
Agent Outputs: {len(self.agent_outputs)} tasks completed
Conversation Turns: {len(self.conversation)}
        """.strip()
    
    def search_outputs(self, keyword: str) -> List[Dict]:
        """Search agent outputs for a specific keyword"""
        results = []
        for output in self.agent_outputs:
            if keyword.lower() in output["output"].lower():
                results.append(output)
        return results
    
    def clear_session(self):
        """Clear all session data"""
        self.agent_outputs = []
        self.conversation = []
        self.context["metadata"] = {}
        self._save_context()
        self._save_agent_outputs()
        self._save_conversation()
