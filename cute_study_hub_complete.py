#!/usr/bin/env python3
"""
🌸 Cute Study Hub - Complete Python Application ✨
A comprehensive study assistant with perfect data preprocessing and beautiful formatting.
"""

import requests
import json
import re
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import google.generativeai as genai
import openai
from bs4 import BeautifulSoup
import PyPDF2
import io
from urllib.parse import urljoin, urlparse
import logging
from pathlib import Path
import textwrap
from dataclasses import dataclass
import asyncio
import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cute_study_hub.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class StudyNote:
    """Data class for study notes."""
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class StudyEvent:
    """Data class for study events."""
    id: str
    title: str
    description: str
    date: datetime
    duration: int  # in minutes
    completed: bool

@dataclass
class StudyGroup:
    """Data class for study groups."""
    id: str
    name: str
    description: str
    members: List[str]
    created_at: datetime

class AdvancedTextProcessor:
    """Advanced text processing and formatting utilities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\"\']', '', text)
        
        # Fix common formatting issues
        text = re.sub(r'\.\s*\.', '.', text)
        text = re.sub(r'\s+([.!?])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    @staticmethod
    def extract_key_phrases(text: str, max_phrases: int = 10) -> List[str]:
        """Extract key phrases from text."""
        # Simple key phrase extraction
        sentences = text.split('.')
        phrases = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and len(sentence) < 100:
                phrases.append(sentence)
                if len(phrases) >= max_phrases:
                    break
        
        return phrases
    
    @staticmethod
    def format_summary(content: str, max_width: int = 80) -> str:
        """Format summary content with beautiful structure."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    wrapped = textwrap.fill(line, width=max_width, initial_indent='    ', subsequent_indent='    ')
                    formatted_lines.append(wrapped)
                elif line.startswith(('Key', 'Main', 'Important', 'Summary', '🔑')):
                    formatted_lines.append(f"\n🔑 {line}")
                elif line.startswith(('📊', '📈', '📉')):
                    formatted_lines.append(f"\n{line}")
                else:
                    wrapped = textwrap.fill(line, width=max_width)
                    formatted_lines.append(wrapped)
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def format_mcq(content: str, max_width: int = 80) -> str:
        """Format MCQ content with beautiful structure."""
        lines = content.split('\n')
        formatted_lines = []
        question_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', '?')) or '?' in line:
                    formatted_lines.append(f"\n❓ Question {question_num}:")
                    question_text = line.replace('Q:', '').replace('Question:', '').strip()
                    wrapped = textwrap.fill(question_text, width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
                    question_num += 1
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    wrapped = textwrap.fill(line, width=max_width, initial_indent='        ')
                    formatted_lines.append(wrapped)
                elif line.startswith(('Answer:', 'Correct:', 'Explanation:')):
                    wrapped = textwrap.fill(f"✅ {line}", width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
                else:
                    wrapped = textwrap.fill(line, width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def format_flashcards(content: str, max_width: int = 80) -> str:
        """Format flashcards content with beautiful structure."""
        lines = content.split('\n')
        formatted_lines = []
        card_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', 'Front:')) or '?' in line:
                    formatted_lines.append(f"\n🃏 Card {card_num}:")
                    question_text = line.replace('Q:', '').replace('Question:', '').replace('Front:', '').strip()
                    wrapped = textwrap.fill(f"❓ {question_text}", width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
                    card_num += 1
                elif line.startswith(('A:', 'Answer:', 'Back:')):
                    answer_text = line.replace('A:', '').replace('Answer:', '').replace('Back:', '').strip()
                    wrapped = textwrap.fill(f"✅ {answer_text}", width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
                else:
                    wrapped = textwrap.fill(line, width=max_width, initial_indent='    ')
                    formatted_lines.append(wrapped)
        
        return '\n'.join(formatted_lines)

class WebScraper:
    """Advanced web scraping with perfect data preprocessing."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_website(self, url: str, extract_options: Dict[str, bool] = None) -> Dict[str, Any]:
        """Scrape website with perfect data preprocessing."""
        if extract_options is None:
            extract_options = {
                'text': True,
                'links': True,
                'images': True,
                'titles': True,
                'metadata': True
            }
        
        logger.info(f"🌐 Scraping website: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            scraped_data = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'title': '',
                'text': '',
                'links': [],
                'images': [],
                'metadata': {},
                'key_phrases': [],
                'word_count': 0,
                'scraping_successful': True
            }
            
            # Extract title
            if extract_options.get('titles', True):
                title_tag = soup.find('title')
                if title_tag:
                    scraped_data['title'] = AdvancedTextProcessor.clean_text(title_tag.get_text())
            
            # Extract main text content
            if extract_options.get('text', True):
                # Get all text content
                text_content = soup.get_text()
                cleaned_text = AdvancedTextProcessor.clean_text(text_content)
                scraped_data['text'] = cleaned_text
                scraped_data['word_count'] = len(cleaned_text.split())
                
                # Extract key phrases
                scraped_data['key_phrases'] = AdvancedTextProcessor.extract_key_phrases(cleaned_text)
            
            # Extract links
            if extract_options.get('links', True):
                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    text = link.get_text().strip()
                    if href and text and len(text) > 3:
                        absolute_url = urljoin(url, href)
                        links.append({
                            'url': absolute_url,
                            'text': AdvancedTextProcessor.clean_text(text),
                            'domain': urlparse(absolute_url).netloc
                        })
                scraped_data['links'] = links[:20]  # Limit to 20 links
            
            # Extract images
            if extract_options.get('images', True):
                images = []
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    alt = img.get('alt', '')
                    if src:
                        absolute_url = urljoin(url, src)
                        images.append({
                            'url': absolute_url,
                            'alt': AdvancedTextProcessor.clean_text(alt),
                            'domain': urlparse(absolute_url).netloc
                        })
                scraped_data['images'] = images[:10]  # Limit to 10 images
            
            # Add metadata
            scraped_data['metadata'] = {
                'content_length': len(scraped_data['text']),
                'links_count': len(scraped_data['links']),
                'images_count': len(scraped_data['images']),
                'key_phrases_count': len(scraped_data['key_phrases']),
                'scraping_successful': True,
                'response_time': response.elapsed.total_seconds()
            }
            
            logger.info(f"✅ Successfully scraped {url}")
            return scraped_data
            
        except Exception as e:
            logger.error(f"❌ Error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'scraping_successful': False,
                'timestamp': datetime.now().isoformat()
            }

class PDFProcessor:
    """Advanced PDF processing with perfect data preprocessing."""
    
    def __init__(self):
        self.processed_pdfs = {}
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF with perfect data preprocessing."""
        logger.info(f"📄 Processing PDF: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                pdf_data = {
                    'file_path': pdf_path,
                    'file_name': os.path.basename(pdf_path),
                    'timestamp': datetime.now().isoformat(),
                    'total_pages': len(pdf_reader.pages),
                    'text_content': '',
                    'pages': [],
                    'key_phrases': [],
                    'word_count': 0,
                    'processing_successful': True,
                    'metadata': {}
                }
                
                full_text = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            # Clean and process page text
                            cleaned_text = AdvancedTextProcessor.clean_text(page_text)
                            
                            pdf_data['pages'].append({
                                'page_number': page_num,
                                'text': cleaned_text,
                                'word_count': len(cleaned_text.split()),
                                'char_count': len(cleaned_text)
                            })
                            
                            full_text += cleaned_text + "\n\n"
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Error extracting text from page {page_num}: {e}")
                
                # Process full text
                pdf_data['text_content'] = full_text
                pdf_data['word_count'] = len(full_text.split())
                pdf_data['key_phrases'] = AdvancedTextProcessor.extract_key_phrases(full_text)
                
                # Add metadata
                pdf_data['metadata'] = {
                    'total_words': pdf_data['word_count'],
                    'total_characters': len(full_text),
                    'average_words_per_page': pdf_data['word_count'] / max(pdf_data['total_pages'], 1),
                    'processing_successful': True,
                    'extracted_pages': len(pdf_data['pages'])
                }
                
                # Store the processed PDF
                self.processed_pdfs[pdf_path] = pdf_data
                
                logger.info(f"✅ Successfully processed PDF: {pdf_path}")
                return pdf_data
                
        except Exception as e:
            logger.error(f"❌ Error processing PDF {pdf_path}: {e}")
            return {
                'file_path': pdf_path,
                'error': str(e),
                'processing_successful': False,
                'timestamp': datetime.now().isoformat()
            }

class AIAssistant:
    """Advanced AI assistant with perfect response formatting."""
    
    def __init__(self, api_key: str, provider: str = "gemini"):
        self.api_key = api_key
        self.provider = provider
        self.setup_ai_client()
    
    def setup_ai_client(self):
        """Setup the AI client."""
        try:
            if self.provider.lower() == "gemini":
                genai.configure(api_key=self.api_key)
                self.ai_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini AI client configured")
            elif self.provider.lower() == "openai":
                openai.api_key = self.api_key
                logger.info("✅ OpenAI client configured")
            else:
                raise ValueError("Invalid provider. Use 'gemini' or 'openai'")
        except Exception as e:
            logger.error(f"❌ Error setting up AI client: {e}")
            raise
    
    def generate_summary(self, content: str, content_type: str = "general") -> str:
        """Generate beautifully formatted summary."""
        logger.info(f"📝 Generating summary for {content_type} content")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute and helpful academic tutor. Create an adorable, structured summary with emojis and clear organization. 
                Make it fun to read! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:
                
                {content[:3000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                summary = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute and helpful academic tutor. Create adorable, structured summaries with emojis and clear organization. Make it fun to read! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:\n\n{content[:3000]}"}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                summary = response.choices[0].message.content
            
            # Format the summary beautifully
            formatted_summary = AdvancedTextProcessor.format_summary(summary)
            logger.info("✅ Summary generated successfully")
            return formatted_summary
            
        except Exception as e:
            logger.error(f"❌ Error generating summary: {e}")
            return f"❌ Error generating summary: {str(e)}"
    
    def generate_mcq(self, content: str, num_questions: int = 5) -> str:
        """Generate beautifully formatted MCQ questions."""
        logger.info(f"❓ Generating {num_questions} MCQ questions")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. 
                Make learning enjoyable! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Create {num_questions} fun multiple-choice questions with 4 options each from this content. 
                Include cute explanations and emojis:
                
                {content[:3000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                mcq = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. Make learning enjoyable! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Create {num_questions} fun multiple-choice questions with 4 options each from this content. Include cute explanations and emojis:\n\n{content[:3000]}"}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                mcq = response.choices[0].message.content
            
            # Format the MCQ beautifully
            formatted_mcq = AdvancedTextProcessor.format_mcq(mcq)
            logger.info("✅ MCQ questions generated successfully")
            return formatted_mcq
            
        except Exception as e:
            logger.error(f"❌ Error generating MCQ: {e}")
            return f"❌ Error generating MCQ: {str(e)}"
    
    def generate_flashcards(self, content: str) -> str:
        """Generate beautifully formatted flashcards."""
        logger.info("🃏 Generating flashcards")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute study helper! Create adorable flashcards with clear questions and answers. 
                Make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Create flashcards from this content. Make them cute and educational:
                
                {content[:3000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                flashcards = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute study helper! Create adorable flashcards with clear questions and answers. Make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Create flashcards from this content. Make them cute and educational:\n\n{content[:3000]}"}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                flashcards = response.choices[0].message.content
            
            # Format the flashcards beautifully
            formatted_flashcards = AdvancedTextProcessor.format_flashcards(flashcards)
            logger.info("✅ Flashcards generated successfully")
            return formatted_flashcards
            
        except Exception as e:
            logger.error(f"❌ Error generating flashcards: {e}")
            return f"❌ Error generating flashcards: {str(e)}"
    
    def chat_with_ai(self, message: str) -> str:
        """Chat with AI assistant."""
        logger.info("💬 Processing chat message")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute and helpful AI study companion. Be friendly, encouraging, and helpful with academic topics. 
                Use emojis and make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                User message: {message}
                """
                
                response = self.ai_model.generate_content(prompt)
                ai_response = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute and helpful AI study companion. Be friendly, encouraging, and helpful with academic topics. Use emojis and make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
            
            logger.info("✅ Chat response generated successfully")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error in chat: {e}")
            return f"❌ Error: {str(e)}"

class CuteStudyHub:
    """Complete Cute Study Hub application with all functionalities."""
    
    def __init__(self, api_key: str, provider: str = "gemini"):
        """Initialize the Cute Study Hub."""
        self.api_key = api_key
        self.provider = provider
        
        # Initialize components
        self.ai_assistant = AIAssistant(api_key, provider)
        self.web_scraper = WebScraper()
        self.pdf_processor = PDFProcessor()
        
        # Data storage
        self.notes = []
        self.events = []
        self.study_groups = []
        self.scraped_content = {}
        self.pdf_content = {}
        
        logger.info("🌸 Cute Study Hub initialized successfully!")
    
    def scrape_website(self, url: str, extract_options: Dict[str, bool] = None) -> Dict[str, Any]:
        """Scrape website with perfect preprocessing."""
        result = self.web_scraper.scrape_website(url, extract_options)
        if result.get('scraping_successful', False):
            self.scraped_content[url] = result
        return result
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Process PDF with perfect preprocessing."""
        result = self.pdf_processor.process_pdf(pdf_path)
        if result.get('processing_successful', False):
            self.pdf_content[pdf_path] = result
        return result
    
    def generate_summary(self, content: str, content_type: str = "general") -> str:
        """Generate beautifully formatted summary."""
        return self.ai_assistant.generate_summary(content, content_type)
    
    def generate_mcq(self, content: str, num_questions: int = 5) -> str:
        """Generate beautifully formatted MCQ questions."""
        return self.ai_assistant.generate_mcq(content, num_questions)
    
    def generate_flashcards(self, content: str) -> str:
        """Generate beautifully formatted flashcards."""
        return self.ai_assistant.generate_flashcards(content)
    
    def chat_with_ai(self, message: str) -> str:
        """Chat with AI assistant."""
        return self.ai_assistant.chat_with_ai(message)
    
    def add_note(self, title: str, content: str, tags: List[str] = None) -> StudyNote:
        """Add a new study note."""
        note = StudyNote(
            id=f"note_{len(self.notes) + 1}",
            title=title,
            content=content,
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.notes.append(note)
        logger.info(f"📝 Note added: {title}")
        return note
    
    def add_event(self, title: str, description: str, date: datetime, duration: int = 60) -> StudyEvent:
        """Add a new study event."""
        event = StudyEvent(
            id=f"event_{len(self.events) + 1}",
            title=title,
            description=description,
            date=date,
            duration=duration,
            completed=False
        )
        self.events.append(event)
        logger.info(f"📅 Event added: {title}")
        return event
    
    def create_study_group(self, name: str, description: str, members: List[str] = None) -> StudyGroup:
        """Create a new study group."""
        group = StudyGroup(
            id=f"group_{len(self.study_groups) + 1}",
            name=name,
            description=description,
            members=members or [],
            created_at=datetime.now()
        )
        self.study_groups.append(group)
        logger.info(f"👥 Study group created: {name}")
        return group
    
    def save_data(self, filename: str = None) -> str:
        """Save all data to JSON file."""
        if filename is None:
            filename = f"cute_study_hub_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'notes': [
                {
                    'id': note.id,
                    'title': note.title,
                    'content': note.content,
                    'tags': note.tags,
                    'created_at': note.created_at.isoformat(),
                    'updated_at': note.updated_at.isoformat()
                } for note in self.notes
            ],
            'events': [
                {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'date': event.date.isoformat(),
                    'duration': event.duration,
                    'completed': event.completed
                } for event in self.events
            ],
            'study_groups': [
                {
                    'id': group.id,
                    'name': group.name,
                    'description': group.description,
                    'members': group.members,
                    'created_at': group.created_at.isoformat()
                } for group in self.study_groups
            ],
            'scraped_content': self.scraped_content,
            'pdf_content': self.pdf_content,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Data saved to {filename}")
        return filename
    
    def load_data(self, filename: str):
        """Load data from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load notes
            self.notes = []
            for note_data in data.get('notes', []):
                note = StudyNote(
                    id=note_data['id'],
                    title=note_data['title'],
                    content=note_data['content'],
                    tags=note_data['tags'],
                    created_at=datetime.fromisoformat(note_data['created_at']),
                    updated_at=datetime.fromisoformat(note_data['updated_at'])
                )
                self.notes.append(note)
            
            # Load events
            self.events = []
            for event_data in data.get('events', []):
                event = StudyEvent(
                    id=event_data['id'],
                    title=event_data['title'],
                    description=event_data['description'],
                    date=datetime.fromisoformat(event_data['date']),
                    duration=event_data['duration'],
                    completed=event_data['completed']
                )
                self.events.append(event)
            
            # Load study groups
            self.study_groups = []
            for group_data in data.get('study_groups', []):
                group = StudyGroup(
                    id=group_data['id'],
                    name=group_data['name'],
                    description=group_data['description'],
                    members=group_data['members'],
                    created_at=datetime.fromisoformat(group_data['created_at'])
                )
                self.study_groups.append(group)
            
            # Load scraped content and PDF content
            self.scraped_content = data.get('scraped_content', {})
            self.pdf_content = data.get('pdf_content', {})
            
            logger.info(f"📂 Data loaded from {filename}")
            
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")

def print_banner():
    """Print the cute banner."""
    banner = """
    🌸✨ Cute Study Hub - Complete Python Application ✨🌸
    =====================================================
    🎯 Advanced AI-Powered Study Assistant
    📚 Perfect Data Preprocessing & Beautiful Formatting
    🌐 Web Scraping | 📄 PDF Processing | 🤖 AI Assistant
    =====================================================
    """
    print(banner)

def print_menu():
    """Print the interactive menu."""
    menu = """
    🌸 Cute Study Hub Menu ✨
    ========================
    1. 🌐 Scrape Website
    2. 📄 Process PDF
    3. 📝 Generate Summary
    4. ❓ Generate MCQ
    5. 🃏 Generate Flashcards
    6. 💬 Chat with AI
    7. 📝 Add Note
    8. 📅 Add Event
    9. 👥 Create Study Group
    10. 💾 Save Data
    11. 📂 Load Data
    12. 📊 View Statistics
    13. 🚪 Exit
    """
    print(menu)

def print_statistics(hub: CuteStudyHub):
    """Print statistics."""
    stats = f"""
    📊 Cute Study Hub Statistics
    ===========================
    📝 Notes: {len(hub.notes)}
    📅 Events: {len(hub.events)}
    👥 Study Groups: {len(hub.study_groups)}
    🌐 Scraped Websites: {len(hub.scraped_content)}
    📄 Processed PDFs: {len(hub.pdf_content)}
    ===========================
    """
    print(stats)

def main():
    """Main function with interactive menu."""
    print_banner()
    
    # Get API configuration
    api_key = input("🔑 Enter your API key: ").strip()
    provider = input("🤖 Choose provider (gemini/openai): ").strip().lower()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    if provider not in ['gemini', 'openai']:
        print("❌ Invalid provider! Using Gemini as default.")
        provider = 'gemini'
    
    # Initialize the hub
    try:
        hub = CuteStudyHub(api_key, provider)
        print("✅ Cute Study Hub initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing hub: {e}")
        return
    
    # Interactive menu
    while True:
        print_menu()
        choice = input("🎯 Choose an option (1-13): ").strip()
        
        if choice == '1':
            url = input("🌐 Enter website URL: ").strip()
            if url:
                print("🔄 Scraping website...")
                result = hub.scrape_website(url)
                if result.get('scraping_successful', False):
                    print(f"✅ Successfully scraped: {result['title']}")
                    print(f"📊 Content: {result['word_count']} words")
                    print(f"🔗 Links: {len(result['links'])}")
                    print(f"🖼️ Images: {len(result['images'])}")
                else:
                    print(f"❌ Scraping failed: {result.get('error', 'Unknown error')}")
        
        elif choice == '2':
            pdf_path = input("📄 Enter PDF file path: ").strip()
            if pdf_path and os.path.exists(pdf_path):
                print("🔄 Processing PDF...")
                result = hub.process_pdf(pdf_path)
                if result.get('processing_successful', False):
                    print(f"✅ Successfully processed: {result['file_name']}")
                    print(f"📊 Pages: {result['total_pages']}")
                    print(f"📝 Words: {result['word_count']}")
                else:
                    print(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            else:
                print("❌ PDF file not found!")
        
        elif choice == '3':
            content = input("📝 Enter content to summarize: ").strip()
            if content:
                print("🔄 Generating summary...")
                summary = hub.generate_summary(content)
                print("\n📝 Generated Summary:")
                print("=" * 50)
                print(summary)
                print("=" * 50)
        
        elif choice == '4':
            content = input("❓ Enter content for MCQ: ").strip()
            if content:
                num_q = input("Number of questions (default 5): ").strip()
                num_q = int(num_q) if num_q.isdigit() else 5
                print("🔄 Generating MCQ questions...")
                mcq = hub.generate_mcq(content, num_q)
                print("\n❓ Generated MCQ Questions:")
                print("=" * 50)
                print(mcq)
                print("=" * 50)
        
        elif choice == '5':
            content = input("🃏 Enter content for flashcards: ").strip()
            if content:
                print("🔄 Generating flashcards...")
                flashcards = hub.generate_flashcards(content)
                print("\n🃏 Generated Flashcards:")
                print("=" * 50)
                print(flashcards)
                print("=" * 50)
        
        elif choice == '6':
            message = input("💬 Enter your message: ").strip()
            if message:
                print("🔄 Processing message...")
                response = hub.chat_with_ai(message)
                print(f"\n🤖 AI Response:")
                print("=" * 50)
                print(response)
                print("=" * 50)
        
        elif choice == '7':
            title = input("📝 Note title: ").strip()
            if title:
                content = input("📝 Note content: ").strip()
                tags = input("🏷️ Tags (comma-separated): ").strip().split(',')
                tags = [tag.strip() for tag in tags if tag.strip()]
                hub.add_note(title, content, tags)
                print("✅ Note added successfully!")
        
        elif choice == '8':
            title = input("📅 Event title: ").strip()
            if title:
                description = input("📅 Event description: ").strip()
                date_str = input("📅 Event date (YYYY-MM-DD HH:MM): ").strip()
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    duration = int(input("⏰ Duration (minutes): ").strip() or "60")
                    hub.add_event(title, description, date, duration)
                    print("✅ Event added successfully!")
                except ValueError:
                    print("❌ Invalid date format!")
        
        elif choice == '9':
            name = input("👥 Group name: ").strip()
            if name:
                description = input("👥 Group description: ").strip()
                members = input("👥 Members (comma-separated): ").strip().split(',')
                members = [member.strip() for member in members if member.strip()]
                hub.create_study_group(name, description, members)
                print("✅ Study group created successfully!")
        
        elif choice == '10':
            filename = hub.save_data()
            print(f"💾 Data saved to: {filename}")
        
        elif choice == '11':
            filename = input("📂 Enter filename to load: ").strip()
            if filename and os.path.exists(filename):
                hub.load_data(filename)
                print("✅ Data loaded successfully!")
            else:
                print("❌ File not found!")
        
        elif choice == '12':
            print_statistics(hub)
        
        elif choice == '13':
            print("👋 Goodbye! Thanks for using Cute Study Hub!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")
        
        input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    main()
