#!/usr/bin/python
# suggest.py
"""Purpose-based app suggestions module for archpkg."""

import os
import yaml
import re
from typing import List, Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import logging

console = Console()
logger = logging.getLogger(__name__)

class PurposeSuggester:
    """Handles purpose-based app suggestions."""
    
    def __init__(self, data_file: str = None):
        """Initialize the suggester with a data file.
        
        Args:
            data_file: Path to the YAML file containing purpose mappings
        """
        if data_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(os.path.dirname(current_dir), 'data', 'purpose_mapping.yaml')
        
        self.data_file = data_file
        self.purpose_mappings = self._load_purpose_mappings()
        
    def _load_purpose_mappings(self) -> Dict[str, List[str]]:
        """Load purpose mappings from YAML file.
        
        Returns:
            Dict mapping purposes to lists of applications
        """
        try:
            if not os.path.exists(self.data_file):
                logger.error(f"Purpose mapping file not found: {self.data_file}")
                return {}
                
            with open(self.data_file, 'r', encoding='utf-8') as f:
                mappings = yaml.safe_load(f) or {}
                
            logger.info(f"Loaded {len(mappings)} purpose mappings from {self.data_file}")
            return mappings
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {self.data_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading purpose mappings from {self.data_file}: {e}")
            return {}
    
    def normalize_query(self, query: str) -> str:
        """Normalize user query for better matching.
        
        Args:
            query: User input query
            
        Returns:
            Normalized query string
        """
        phrase_normalized = self._normalize_phrases(query)
        if phrase_normalized != query:
            return phrase_normalized
        
        normalized = query.lower().strip()
        
        stop_words = {'apps', 'for', 'to', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'i', 'want', 'need', 'looking', 'find', 'search', 'get', 'install', 'download'}
        words = [word for word in normalized.split() if word not in stop_words]
        
        return ' '.join(words)
    
    def find_matching_purposes(self, query: str) -> List[Tuple[str, List[str]]]:
        """Find purposes that match the given query.
        
        Args:
            query: User search query
            
        Returns:
            List of (purpose, apps) tuples that match the query
        """
        if not self.purpose_mappings:
            logger.warning("No purpose mappings loaded")
            return []
            
        normalized_query = self.normalize_query(query)
        matches = []
        
        for purpose, apps in self.purpose_mappings.items():
            # Check for exact match
            if normalized_query == purpose.lower():
                matches.append((purpose, apps))
                continue
                
            if normalized_query in purpose.lower():
                matches.append((purpose, apps))
                continue
                
            query_words = set(normalized_query.split())
            purpose_words = set(purpose.lower().split())
            
            if query_words.intersection(purpose_words):
                matches.append((purpose, apps))
                continue
                
            synonyms = self._get_synonyms(normalized_query)
            for synonym in synonyms:
                if synonym in purpose.lower():
                    matches.append((purpose, apps))
                    break
        
        def relevance_score(match):
            purpose, apps = match
            purpose_lower = purpose.lower()
            query_lower = normalized_query.lower()
            
            if query_lower == purpose_lower:
                return 100
            elif query_lower in purpose_lower:
                return 80
            else:
                query_words = set(query_lower.split())
                purpose_words = set(purpose_lower.split())
                return len(query_words.intersection(purpose_words)) * 20
                
        matches.sort(key=relevance_score, reverse=True)
        return matches
    
    def _get_synonyms(self, query: str) -> List[str]:
        """Get synonyms for common terms (enhanced implementation).
        
        Args:
            query: Query string
            
        Returns:
            List of synonym terms
        """
        synonym_map = {
            'edit': ['editing', 'editor', 'modify', 'change', 'cut', 'trim', 'compose'],
            'video': ['videos', 'movie', 'movies', 'film', 'films', 'clip', 'clips', 'recording'],
            'music': ['audio', 'sound', 'songs', 'tunes', 'tracks', 'audio', 'soundtrack'],
            'code': ['coding', 'programming', 'development', 'dev', 'program', 'script', 'software'],
            'office': ['productivity', 'work', 'business', 'documents', 'spreadsheet', 'presentation'],
            'graphics': ['image', 'images', 'photo', 'photos', 'picture', 'pictures', 'design', 'art', 'drawing'],
            'game': ['gaming', 'games', 'play', 'entertainment', 'fun'],
            'browse': ['browsing', 'web', 'internet', 'surf', 'navigate', 'search'],
            'communicate': ['communication', 'chat', 'message', 'talk', 'call', 'voice', 'text'],
            'system': ['system', 'admin', 'administration', 'manage', 'monitor', 'control'],
            'text': ['writing', 'write', 'document', 'documents', 'note', 'notes', 'editor'],
            'media': ['multimedia', 'entertainment', 'playback', 'player', 'streaming'],
            'utility': ['utilities', 'tools', 'tool', 'helper', 'assistant'],
            'app': ['application', 'program', 'software', 'tool'],
            'install': ['setup', 'setup', 'download', 'get'],
            'need': ['want', 'looking', 'find', 'search'],
            'for': ['to', 'that', 'which'],
            'apps': ['applications', 'programs', 'software', 'tools'],
            'to': ['for', 'that', 'which', 'in', 'on'],
            'the': ['a', 'an', 'some'],
            'a': ['an', 'some', 'any'],
            'an': ['a', 'some', 'any']
        }
        
        synonyms = []
        for word in query.split():
            if word in synonym_map:
                synonyms.extend(synonym_map[word])
                
        return synonyms
    
    def _normalize_phrases(self, query: str) -> str:
        """Normalize common phrases to standard purposes.
        
        Args:
            query: User input query
            
        Returns:
            Normalized query string
        """
        phrase_mappings = {
            'edit videos': 'video editing',
            'video editor': 'video editing',
            'video editing software': 'video editing',
            'apps to edit videos': 'video editing',
            'video editing apps': 'video editing',
            'video editing tools': 'video editing',
            'video editing programs': 'video editing',
            
            'office work': 'office',
            'office apps': 'office',
            'office software': 'office',
            'office suite': 'office',
            'productivity apps': 'office',
            'work apps': 'office',
            'business apps': 'office',
            
            'music apps': 'music',
            'music software': 'music',
            'audio apps': 'music',
            'music player': 'music',
            'audio editor': 'music',
            'music production': 'music',
            
            'code editor': 'coding',
            'programming apps': 'coding',
            'development tools': 'coding',
            'coding apps': 'coding',
            'programming tools': 'coding',
            'dev tools': 'coding',
            'software development': 'coding',
            
            'image editor': 'graphics',
            'photo editor': 'graphics',
            'graphics apps': 'graphics',
            'design apps': 'graphics',
            'drawing apps': 'graphics',
            'image editing': 'graphics',
            'photo editing': 'graphics',
            
            'gaming apps': 'gaming',
            'games': 'gaming',
            'game launcher': 'gaming',
            'play games': 'gaming',
            
            'web browser': 'browsing',
            'browser': 'browsing',
            'internet apps': 'browsing',
            'surf the web': 'browsing',
            
            'chat apps': 'communication',
            'messaging apps': 'communication',
            'communication apps': 'communication',
            'voice chat': 'communication',
            'video call': 'communication',
            
            'system tools': 'system',
            'admin tools': 'system',
            'system utilities': 'system',
            'system monitor': 'system',
            
            'text editor': 'text editing',
            'writing apps': 'text editing',
            'note taking': 'text editing',
            'document editor': 'text editing',
            
            'media player': 'media',
            'video player': 'media',
            'music player': 'media',
            'entertainment apps': 'media',
            'streaming apps': 'media',
            
            'utility apps': 'utilities',
            'helper apps': 'utilities',
            'system utilities': 'utilities',
            'command line tools': 'utilities'
        }
        
        query_lower = query.lower().strip()
        
        # Check for exact phrase matches first
        for phrase, purpose in phrase_mappings.items():
            if phrase in query_lower:
                return purpose
        
        return query
    
    def suggest_apps(self, query: str, max_results: int = 10) -> List[Tuple[str, List[str]]]:
        """Get app suggestions for a given purpose query.
        
        Args:
            query: User purpose query
            max_results: Maximum number of purpose categories to return
            
        Returns:
            List of (purpose, apps) tuples
        """
        matches = self.find_matching_purposes(query)
        return matches[:max_results]
    
    def display_suggestions(self, query: str, max_results: int = 5) -> bool:
        """Display app suggestions in a formatted table.
        
        Args:
            query: User purpose query
            max_results: Maximum number of suggestions to display
            
        Returns:
            True if suggestions were found and displayed, False otherwise
        """
        suggestions = self.suggest_apps(query, max_results)
        
        if not suggestions:
            console.print(Panel(
                f"[yellow]No suggestions found for '{query}'.[/yellow]\n\n"
                "[bold cyan]Try these examples:[/bold cyan]\n"
                "- [cyan]archpkg suggest video editing[/cyan]\n"
                "- [cyan]archpkg suggest office[/cyan]\n"
                "- [cyan]archpkg suggest coding[/cyan]\n"
                "- [cyan]archpkg suggest music[/cyan]\n"
                "- [cyan]archpkg suggest graphics[/cyan]\n\n"
                "[bold]Available purposes:[/bold] " + ", ".join(self.purpose_mappings.keys()),
                title="No Suggestions Found",
                border_style="yellow"
            ))
            return False
        
   
        for i, (purpose, apps) in enumerate(suggestions, 1):
            table = Table(title=f"Recommended apps for '{purpose}'")
            table.add_column("Index", style="cyan", no_wrap=True)
            table.add_column("Package Name", style="green")
            table.add_column("Description", style="magenta")
            
            for idx, app in enumerate(apps, 1):
              
                description = self._get_app_description(app)
                table.add_row(str(idx), app, description)
            
            console.print(table)
            
            if i < len(suggestions):
                console.print()  
        
        return True
    
    def _get_app_description(self, app_name: str) -> str:
        """Get a brief description for an app (placeholder implementation).
        
        Args:
            app_name: Name of the application
            
        Returns:
            Brief description of the application
        """
        # This is a placeholder - in a real implementation, you might
        # query package managers for descriptions or maintain a separate
        # description database
        descriptions = {
            'kdenlive': 'Professional video editor',
            'shotcut': 'Free, open-source video editor',
            'openshot': 'Simple video editor',
            'obs-studio': 'Live streaming and recording software',
            'libreoffice-fresh': 'Complete office suite',
            'onlyoffice-bin': 'Office suite with online collaboration',
            'audacity': 'Audio editor and recorder',
            'vlc': 'Media player',
            'lmms': 'Digital audio workstation',
            'vscode': 'Code editor by Microsoft',
            'neovim': 'Vim-based text editor',
            'gimp': 'Image editor',
            'inkscape': 'Vector graphics editor',
            'krita': 'Digital painting application',
            'steam': 'Gaming platform',
            'firefox': 'Web browser',
            'discord': 'Voice and text chat',
            'git': 'Version control system',
            'htop': 'Interactive process viewer',
            'vim': 'Text editor'
        }
        
        return descriptions.get(app_name, 'Application')
    
    def list_available_purposes(self) -> None:
        """Display all available purposes."""
        if not self.purpose_mappings:
            console.print(Panel(
                "[red]No purpose mappings available.[/red]",
                title="Error",
                border_style="red"
            ))
            return
            
        table = Table(title="Available Purposes")
        table.add_column("Purpose", style="green")
        table.add_column("App Count", style="cyan")
        table.add_column("Sample Apps", style="magenta")
        
        for purpose, apps in self.purpose_mappings.items():
            sample_apps = ", ".join(apps[:3])
            if len(apps) > 3:
                sample_apps += "..."
            table.add_row(purpose, str(len(apps)), sample_apps)
        
        console.print(table)


def suggest_apps(query: str, data_file: str = None) -> bool:
    """Convenience function to suggest apps for a given purpose.
    
    Args:
        query: User purpose query
        data_file: Optional path to purpose mapping file
        
    Returns:
        True if suggestions were found and displayed, False otherwise
    """
    suggester = PurposeSuggester(data_file)
    return suggester.display_suggestions(query)


def list_purposes(data_file: str = None) -> None:
    """Convenience function to list all available purposes.
    
    Args:
        data_file: Optional path to purpose mapping file
    """
    suggester = PurposeSuggester(data_file)
    suggester.list_available_purposes()
