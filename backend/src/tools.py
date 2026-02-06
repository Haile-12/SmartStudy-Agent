import arxiv
from pathlib import Path
from crewai.tools import BaseTool

class AcademicSearchTool(BaseTool):
    """Search academic resources for study materials"""
    name: str = "Academic Resource Search"
    description: str = "Search arXiv for academic papers related to study topics. Input: research topic string."
    
    def _run(self, query: str) -> str:
        """Search arXiv for relevant papers"""
        try:
            # Simple query sanitization
            clean_query = " ".join(query.split()[:5])  # Limit to first 5 words
            
            client = arxiv.Client()
            search = arxiv.Search(
                query=clean_query,
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for i, paper in enumerate(client.results(search)):
                authors = ", ".join(str(a) for a in paper.authors[:2])
                results.append(
                    f"{i+1}. **{paper.title}**\n"
                    f"   Authors: {authors}\n"
                    f"   URL: {paper.entry_id}\n"
                    f"   Published: {paper.published.strftime('%Y-%m-%d')}\n"
                )
            
            if not results:
                return f"No academic resources found for: {clean_query}\nSuggestion: Try broader terms like 'machine learning' instead of specific algorithms"
            
            return "📚 **Recommended Academic Resources**:\n\n" + "\n".join(results)
        except Exception as e:
            return f"Search error: {str(e)}. Try simpler search terms."

class FileHandlerTool(BaseTool):
    """Handle reading/writing study materials securely"""
    name: str = "Study Material Handler"
    description: str = "Read or write files. Usage: action='write', filename='notes.txt', content='...' OR action='read', filename='notes.txt'"
    output_dir: str = "./outputs/materials"
    
    def _run(self, action: str, filename: str, content: str = None) -> str:
        """Dispatch file operation"""
        try:
            # Ensure output directory exists before any operation
            out_path = Path(self.output_dir).resolve()
            out_path.mkdir(parents=True, exist_ok=True)
            
            clean_filename = self._sanitize(filename)
            action = action.lower().strip()
            
            if action == "write":
                if not content:
                    return "Error: Content is required for write action"
                return self._write_file(clean_filename, content, out_path)
            elif action == "read":
                return self._read_file(clean_filename, out_path)
            else:
                return f"Error: Unsupported action '{action}'. Use 'write' or 'read'"
        except Exception as e:
            return f"File operation error: {str(e)}"
    
    def _sanitize(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        safe = "".join(c for c in filename if c.isalnum() or c in "._- ")
        return safe.strip().replace(" ", "_") or "untitled"
    
    def _get_safe_path(self, filename: str, base_dir: Path) -> Path:
        """Get safe path within output directory"""
        filepath = (base_dir / filename).resolve()
        if not str(filepath).startswith(str(base_dir)):
            raise ValueError("Path traversal attempt blocked")
        return filepath
    
    def _write_file(self, filename: str, content: str, base_dir: Path) -> str:
        """Write content to file"""
        try:
            filepath = self._get_safe_path(filename, base_dir)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✓ Saved {len(content)} characters to {filename}"
        except Exception as e:
            return f"Write error: {str(e)}"
    
    def _read_file(self, filename: str, base_dir: Path) -> str:
        """Read file content"""
        try:
            filepath = self._get_safe_path(filename, base_dir)
            if not filepath.exists():
                return f"Error: File not found: {filename}"
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            preview = content[:500] + "..." if len(content) > 500 else content
            return f"📄 {filename} ({len(content)} chars):\n{preview}"
        except Exception as e:
            return f"Read error: {str(e)}"
