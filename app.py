#!/usr/bin/env python3
"""
🌸 Cute Study Hub - Interactive Web Application ✨
A beautiful, interactive web-based study assistant with real-time features.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import google.generativeai as genai
import openai
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
from urllib.parse import urljoin, urlparse
import re
import textwrap
import asyncio
import aiohttp
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cute_study_hub_secret_key_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize SocketIO for real-time features
socketio = SocketIO(app, cors_allowed_origins="*")

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global storage for user data
user_data = {}

# Data persistence settings
DATA_DIR = 'user_data'
os.makedirs(DATA_DIR, exist_ok=True)

def save_user_data(user_id: str, data: dict):
    """Save user data to JSON file."""
    try:
        file_path = os.path.join(DATA_DIR, f'{user_id}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Data saved for user {user_id}")
    except Exception as e:
        logger.error(f"Error saving data for user {user_id}: {e}")

def load_user_data(user_id: str) -> dict:
    """Load user data from JSON file."""
    try:
        file_path = os.path.join(DATA_DIR, f'{user_id}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Data loaded for user {user_id}")
            return data
        else:
            logger.info(f"No data file found for user {user_id}, creating new")
            return {}
    except Exception as e:
        logger.error(f"Error loading data for user {user_id}: {e}")
        return {}

def backup_user_data():
    """Create backup of all user data."""
    try:
        backup_dir = os.path.join(DATA_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        all_data = {}
        for user_id in user_data:
            all_data[user_id] = user_data[user_id].__dict__
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return None

class InteractiveStudyHub:
    """Interactive study hub with real-time features."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.api_key = None
        self.provider = None
        self.notes = []
        self.events = []
        self.study_groups = []
        self.scraped_content = {}
        self.pdf_content = {}
        self.chat_history = []
        
        # Load existing data
        self.load_data()
    
    def load_data(self):
        """Load user data from persistent storage."""
        try:
            data = load_user_data(self.user_id)
            if data:
                self.api_key = data.get('api_key')
                self.provider = data.get('provider')
                self.notes = data.get('notes', [])
                self.events = data.get('events', [])
                self.study_groups = data.get('study_groups', [])
                self.scraped_content = data.get('scraped_content', {})
                self.pdf_content = data.get('pdf_content', {})
                self.chat_history = data.get('chat_history', [])
                
                # Setup AI if credentials exist
                if self.api_key and self.provider:
                    self.setup_ai(self.api_key, self.provider)
        except Exception as e:
            logger.error(f"Error loading data for user {self.user_id}: {e}")
    
    def save_data(self):
        """Save user data to persistent storage."""
        try:
            data = {
                'user_id': self.user_id,
                'api_key': self.api_key,
                'provider': self.provider,
                'notes': self.notes,
                'events': self.events,
                'study_groups': self.study_groups,
                'scraped_content': self.scraped_content,
                'pdf_content': self.pdf_content,
                'chat_history': self.chat_history,
                'last_updated': datetime.now().isoformat()
            }
            save_user_data(self.user_id, data)
        except Exception as e:
            logger.error(f"Error saving data for user {self.user_id}: {e}")
        
    def setup_ai(self, api_key: str, provider: str):
        """Setup AI client."""
        self.api_key = api_key
        self.provider = provider
        
        try:
            if provider.lower() == "gemini":
                genai.configure(api_key=api_key)
                self.ai_model = genai.GenerativeModel('gemini-2.5-flash')
            elif provider.lower() == "openai":
                openai.api_key = api_key
            
            # Save data after setting up AI
            self.save_data()
            return True
        except Exception as e:
            logger.error(f"Error setting up AI: {e}")
            return False
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\"\']', '', text)
        text = re.sub(r'\.\s*\.', '.', text)
        text = re.sub(r'\s+([.!?])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        return text.strip()
    
    def format_content(self, content: str, content_type: str = "general") -> str:
        """Format content beautifully."""
        if content_type == "summary":
            return self._format_summary(content)
        elif content_type == "mcq":
            return self._format_mcq(content)
        elif content_type == "flashcards":
            return self._format_flashcards(content)
        else:
            return content
    
    def _format_summary(self, content: str) -> str:
        """Format summary content."""
        # Remove all formatting characters
        content = content.replace("**", "").replace("*", "")
        content = content.replace("##", "").replace("#", "")
        content = content.replace("---", "").replace("--", "")
        content = content.replace("__", "").replace("_", "")
        content = content.replace("~~", "").replace("~", "")
        content = content.replace("```", "").replace("`", "")
        content = content.replace("||", "").replace("|", "")
        content = content.replace(">>", "").replace(">", "")
        content = content.replace("<<", "").replace("<", "")
        
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    # Clean the line and add proper spacing
                    clean_line = line.replace('•', '').replace('-', '').replace('*', '').strip()
                    formatted_lines.append(f"    {clean_line}")
                elif line.startswith(('Key', 'Main', 'Important', 'Summary', '🔑')):
                    formatted_lines.append(f"\n🔑 {line}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_mcq(self, content: str) -> str:
        """Format MCQ content."""
        # Remove all formatting characters
        content = content.replace("**", "").replace("*", "")
        content = content.replace("##", "").replace("#", "")
        content = content.replace("---", "").replace("--", "")
        content = content.replace("__", "").replace("_", "")
        content = content.replace("~~", "").replace("~", "")
        content = content.replace("```", "").replace("`", "")
        content = content.replace("||", "").replace("|", "")
        content = content.replace(">>", "").replace(">", "")
        content = content.replace("<<", "").replace("<", "")
        
        lines = content.split('\n')
        formatted_lines = []
        question_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', '?')) or '?' in line:
                    formatted_lines.append(f"\n❓ Question {question_num}:")
                    question_text = line.replace('Q:', '').replace('Question:', '').strip()
                    formatted_lines.append(f"    {question_text}")
                    question_num += 1
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    formatted_lines.append(f"        {line}")
                elif line.startswith(('Answer:', 'Correct:', 'Explanation:')):
                    formatted_lines.append(f"    ✅ {line}")
                else:
                    formatted_lines.append(f"    {line}")
        
        return '\n'.join(formatted_lines)
    
    def _format_flashcards(self, content: str) -> str:
        """Format flashcards content."""
        # Remove all formatting characters
        content = content.replace("**", "").replace("*", "")
        content = content.replace("##", "").replace("#", "")
        content = content.replace("---", "").replace("--", "")
        content = content.replace("__", "").replace("_", "")
        content = content.replace("~~", "").replace("~", "")
        content = content.replace("```", "").replace("`", "")
        content = content.replace("||", "").replace("|", "")
        content = content.replace(">>", "").replace(">", "")
        content = content.replace("<<", "").replace("<", "")
        
        lines = content.split('\n')
        formatted_lines = []
        card_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', 'Front:')) or '?' in line:
                    formatted_lines.append(f"\n🃏 Card {card_num}:")
                    question_text = line.replace('Q:', '').replace('Question:', '').replace('Front:', '').strip()
                    formatted_lines.append(f"    ❓ {question_text}")
                    card_num += 1
                elif line.startswith(('A:', 'Answer:', 'Back:')):
                    answer_text = line.replace('A:', '').replace('Answer:', '').replace('Back:', '').strip()
                    formatted_lines.append(f"    ✅ {answer_text}")
                else:
                    formatted_lines.append(f"    {line}")
        
        return '\n'.join(formatted_lines)
    
    def scrape_website(self, url: str) -> Dict[str, Any]:
        """Scrape website with real-time updates."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            # Extract content
            title = soup.find('title')
            title_text = title.get_text() if title else "No Title"
            
            text_content = soup.get_text()
            cleaned_text = self.clean_text(text_content)
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().strip()
                if href and text and len(text) > 3:
                    absolute_url = urljoin(url, href)
                    links.append({
                        'url': absolute_url,
                        'text': self.clean_text(text)
                    })
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=True):
                src = img['src']
                alt = img.get('alt', '')
                if src:
                    absolute_url = urljoin(url, src)
                    images.append({
                        'url': absolute_url,
                        'alt': self.clean_text(alt)
                    })
            
            result = {
                'url': url,
                'title': self.clean_text(title_text),
                'text': cleaned_text,
                'links': links[:20],
                'images': images[:10],
                'word_count': len(cleaned_text.split()),
                'scraping_successful': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self.scraped_content[url] = result
            return result
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'scraping_successful': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Process PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                full_text = ""
                pages = []
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            cleaned_text = self.clean_text(page_text)
                            pages.append({
                                'page_number': page_num,
                                'text': cleaned_text,
                                'word_count': len(cleaned_text.split())
                            })
                            full_text += cleaned_text + "\n\n"
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num}: {e}")
                
                result = {
                    'file_path': file_path,
                    'file_name': os.path.basename(file_path),
                    'total_pages': len(pdf_reader.pages),
                    'text_content': full_text,
                    'pages': pages,
                    'word_count': len(full_text.split()),
                    'processing_successful': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.pdf_content[file_path] = result
                return result
                
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {e}")
            return {
                'file_path': file_path,
                'error': str(e),
                'processing_successful': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_summary(self, content: str, content_type: str = "general") -> str:
        """Generate AI summary."""
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute and helpful academic tutor. Create an adorable, structured summary with emojis and clear organization. 
                Make it fun to read!
                
                IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like:
                - Asterisks (*) for bold or italic
                - Hashtags (#) for headers
                - Dashes (---) for lines
                - Underscores (_) for emphasis
                - Any markdown formatting
                
                Write in simple, clean text with proper spacing and line breaks only.
                
                Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:
                
                {content[:3000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                summary = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute and helpful academic tutor. Create adorable, structured summaries with emojis and clear organization. Make it fun to read! IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like asterisks (*), hashtags (#), dashes (---), underscores (_), or any markdown formatting. Write in simple, clean text with proper spacing and line breaks only."},
                        {"role": "user", "content": f"Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:\n\n{content[:3000]}"}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                summary = response.choices[0].message.content
            
            return self.format_content(summary, "summary")
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"❌ Error generating summary: {str(e)}"
    
    def generate_mcq(self, content: str, num_questions: int = 5) -> str:
        """Generate MCQ questions."""
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. 
                Make learning enjoyable!
                
                IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like:
                - Asterisks (*) for bold or italic
                - Hashtags (#) for headers
                - Dashes (---) for lines
                - Underscores (_) for emphasis
                - Any markdown formatting
                
                Write in simple, clean text with proper spacing and line breaks only.
                
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
                        {"role": "system", "content": "You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. Make learning enjoyable! IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like asterisks (*), hashtags (#), dashes (---), underscores (_), or any markdown formatting. Write in simple, clean text with proper spacing and line breaks only."},
                        {"role": "user", "content": f"Create {num_questions} fun multiple-choice questions with 4 options each from this content. Include cute explanations and emojis:\n\n{content[:3000]}"}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                mcq = response.choices[0].message.content
            
            return self.format_content(mcq, "mcq")
            
        except Exception as e:
            logger.error(f"Error generating MCQ: {e}")
            return f"❌ Error generating MCQ: {str(e)}"
    
    def generate_flashcards(self, content: str) -> str:
        """Generate flashcards."""
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute study helper! Create adorable flashcards with clear questions and answers. 
                Make learning fun!
                
                IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like:
                - Asterisks (*) for bold or italic
                - Hashtags (#) for headers
                - Dashes (---) for lines
                - Underscores (_) for emphasis
                - Any markdown formatting
                
                Write in simple, clean text with proper spacing and line breaks only.
                
                Create flashcards from this content. Make them cute and educational:
                
                {content[:3000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                flashcards = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute study helper! Create adorable flashcards with clear questions and answers. Make learning fun! IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like asterisks (*), hashtags (#), dashes (---), underscores (_), or any markdown formatting. Write in simple, clean text with proper spacing and line breaks only."},
                        {"role": "user", "content": f"Create flashcards from this content. Make them cute and educational:\n\n{content[:3000]}"}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                flashcards = response.choices[0].message.content
            
            return self.format_content(flashcards, "flashcards")
            
        except Exception as e:
            logger.error(f"Error generating flashcards: {e}")
            return f"❌ Error generating flashcards: {str(e)}"
    
    def chat_with_ai(self, message: str) -> str:
        """Chat with AI assistant."""
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute and helpful AI study companion. Be friendly, encouraging, and helpful with academic topics. 
                Use emojis and make learning fun! 
                
                IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like:
                - Asterisks (*) for bold or italic
                - Hashtags (#) for headers
                - Dashes (---) for lines
                - Underscores (_) for emphasis
                - Any markdown formatting
                
                Write in simple, clean text with proper spacing and line breaks only.
                
                User message: {message}
                """
                
                response = self.ai_model.generate_content(prompt)
                ai_response = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute and helpful AI study companion. Be friendly, encouraging, and helpful with academic topics. Use emojis and make learning fun! IMPORTANT: Use ONLY plain text. Do NOT use any formatting characters like asterisks (*), hashtags (#), dashes (---), underscores (_), or any markdown formatting. Write in simple, clean text with proper spacing and line breaks only."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
            
            # Add to chat history
            self.chat_history.append({
                'user': message,
                'ai': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Save data after adding to chat history
            self.save_data()
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"❌ Error: {str(e)}"
    
    def add_note(self, title: str, content: str, tags: List[str] = None) -> Dict[str, Any]:
        """Add a study note."""
        note = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.notes.append(note)
        self.save_data()  # Save data after adding note
        return note
    
    def add_event(self, title: str, description: str, date: str, duration: int = 60) -> Dict[str, Any]:
        """Add a study event."""
        event = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'date': date,
            'duration': duration,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.events.append(event)
        self.save_data()  # Save data after adding event
        return event
    
    def create_study_group(self, name: str, description: str, members: List[str] = None) -> Dict[str, Any]:
        """Create a study group."""
        group = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'members': members or [],
            'created_at': datetime.now().isoformat()
        }
        self.study_groups.append(group)
        return group

def get_user_hub():
    """Get or create user hub."""
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    
    if user_id not in user_data:
        user_data[user_id] = InteractiveStudyHub(user_id)
    
    return user_data[user_id]


@app.route('/')
def index():
    """Main page."""
    return render_template('final_website.html')

@app.route('/login', methods=['POST'])
def login():
    """Login with API key."""
    data = request.get_json()
    api_key = data.get('api_key')
    provider = data.get('provider', 'gemini')
    
    hub = get_user_hub()
    if hub.setup_ai(api_key, provider):
        return jsonify({'success': True, 'message': 'Login successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid API key or provider'})

@app.route('/scrape', methods=['POST'])
def scrape_website():
    """Scrape website."""
    data = request.get_json()
    url = data.get('url')
    
    hub = get_user_hub()
    result = hub.scrape_website(url)
    
    # Emit real-time update
    socketio.emit('scraping_update', {
        'url': url,
        'status': 'completed',
        'result': result
    }, room=session['user_id'])
    
    return jsonify(result)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """Upload and process PDF."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        hub = get_user_hub()
        result = hub.process_pdf(file_path)
        
        # Emit real-time update
        socketio.emit('pdf_processing_update', {
            'filename': filename,
            'status': 'completed',
            'result': result
        }, room=session['user_id'])
        
        return jsonify(result)
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    """Generate AI summary."""
    data = request.get_json()
    content = data.get('content')
    content_type = data.get('content_type', 'general')
    
    hub = get_user_hub()
    summary = hub.generate_summary(content, content_type)
    
    return jsonify({'summary': summary})

@app.route('/generate_mcq', methods=['POST'])
def generate_mcq():
    """Generate MCQ questions."""
    data = request.get_json()
    content = data.get('content')
    num_questions = data.get('num_questions', 5)
    
    hub = get_user_hub()
    mcq = hub.generate_mcq(content, num_questions)
    
    return jsonify({'mcq': mcq})

@app.route('/generate_flashcards', methods=['POST'])
def generate_flashcards():
    """Generate flashcards."""
    data = request.get_json()
    content = data.get('content')
    
    hub = get_user_hub()
    flashcards = hub.generate_flashcards(content)
    
    return jsonify({'flashcards': flashcards})

@app.route('/chat', methods=['POST'])
def chat():
    """Chat with AI."""
    data = request.get_json()
    message = data.get('message')
    
    hub = get_user_hub()
    response = hub.chat_with_ai(message)
    
    return jsonify({'response': response})

@app.route('/add_note', methods=['POST'])
def add_note():
    """Add study note."""
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags', [])
    
    hub = get_user_hub()
    note = hub.add_note(title, content, tags)
    
    return jsonify({'note': note})

@app.route('/add_event', methods=['POST'])
def add_event():
    """Add study event."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    duration = data.get('duration', 60)
    
    hub = get_user_hub()
    event = hub.add_event(title, description, date, duration)
    
    return jsonify({'event': event})

@app.route('/create_group', methods=['POST'])
def create_group():
    """Create study group."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    members = data.get('members', [])
    
    hub = get_user_hub()
    group = hub.create_study_group(name, description, members)
    
    return jsonify({'group': group})

@app.route('/get_data', methods=['GET'])
def get_data():
    """Get all user data."""
    hub = get_user_hub()
    return jsonify({
        'notes': hub.notes,
        'events': hub.events,
        'study_groups': hub.study_groups,
        'scraped_content': hub.scraped_content,
        'pdf_content': hub.pdf_content,
        'chat_history': hub.chat_history
    })

@app.route('/update_note/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note."""
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags', [])
    
    hub = get_user_hub()
    for note in hub.notes:
        if note['id'] == note_id:
            note['title'] = title
            note['content'] = content
            note['tags'] = tags
            note['updated_at'] = datetime.now().isoformat()
            hub.save_data()  # Save data after updating note
            return jsonify({'success': True, 'note': note})
    
    return jsonify({'success': False, 'message': 'Note not found'})

@app.route('/delete_note/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note."""
    hub = get_user_hub()
    hub.notes = [note for note in hub.notes if note['id'] != note_id]
    hub.save_data()  # Save data after deleting note
    return jsonify({'success': True, 'message': 'Note deleted'})

@app.route('/update_event/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    duration = data.get('duration', 60)
    
    hub = get_user_hub()
    for event in hub.events:
        if event['id'] == event_id:
            event['title'] = title
            event['description'] = description
            event['date'] = date
            event['duration'] = duration
            hub.save_data()  # Save data after updating event
            return jsonify({'success': True, 'event': event})
    
    return jsonify({'success': False, 'message': 'Event not found'})

@app.route('/delete_event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event."""
    hub = get_user_hub()
    hub.events = [event for event in hub.events if event['id'] != event_id]
    hub.save_data()  # Save data after deleting event
    return jsonify({'success': True, 'message': 'Event deleted'})

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    user_id = session.get('user_id')
    if user_id:
        join_room(user_id)
        emit('connected', {'message': 'Connected to Cute Study Hub!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    user_id = session.get('user_id')
    if user_id:
        leave_room(user_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
