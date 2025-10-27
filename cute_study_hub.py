#!/usr/bin/env python3
"""
Cute Study Hub - Python Version
A comprehensive study assistant with AI integration, web scraping, and data preprocessing.
"""

import requests
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import google.generativeai as genai
import openai
from bs4 import BeautifulSoup
import PyPDF2
import io
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CuteStudyHub:
    """Main class for the Cute Study Hub application."""
    
    def __init__(self, api_key: str, provider: str = "gemini"):
        """
        Initialize the Cute Study Hub.
        
        Args:
            api_key (str): API key for the AI service
            provider (str): AI provider ("gemini" or "openai")
        """
        self.api_key = api_key
        self.provider = provider
        self.setup_ai_client()
        self.scraped_content = {}
        self.pdf_content = {}
        self.notes = []
        self.events = []
        self.study_groups = []
        
    def setup_ai_client(self):
        """Setup the AI client based on the provider."""
        try:
            if self.provider.lower() == "gemini":
                genai.configure(api_key=self.api_key)
                self.ai_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("Gemini AI client configured successfully")
            elif self.provider.lower() == "openai":
                openai.api_key = self.api_key
                logger.info("OpenAI client configured successfully")
            else:
                raise ValueError("Invalid provider. Use 'gemini' or 'openai'")
        except Exception as e:
            logger.error(f"Error setting up AI client: {e}")
            raise
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess and clean text content.
        
        Args:
            text (str): Raw text content
            
        Returns:
            str: Cleaned and formatted text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Fix common formatting issues
        text = re.sub(r'\.\s*\.', '.', text)  # Remove double periods
        text = re.sub(r'\s+([.!?])', r'\1', text)  # Remove spaces before punctuation
        
        # Ensure proper sentence spacing
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    def format_content(self, content: str, content_type: str = "general") -> str:
        """
        Format content based on type with proper indentation and structure.
        
        Args:
            content (str): Content to format
            content_type (str): Type of content ("summary", "mcq", "flashcards", "scraped")
            
        Returns:
            str: Formatted content
        """
        if not content:
            return "No content available."
        
        # Preprocess the content
        content = self.preprocess_text(content)
        
        if content_type == "summary":
            return self._format_summary(content)
        elif content_type == "mcq":
            return self._format_mcq(content)
        elif content_type == "flashcards":
            return self._format_flashcards(content)
        elif content_type == "scraped":
            return self._format_scraped_content(content)
        else:
            return self._format_general(content)
    
    def _format_summary(self, content: str) -> str:
        """Format summary content with proper structure."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Add proper indentation for bullet points
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    formatted_lines.append(f"    {line}")
                elif line.startswith(('Key', 'Main', 'Important', 'Summary')):
                    formatted_lines.append(f"\n🔑 {line}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_mcq(self, content: str) -> str:
        """Format MCQ content with proper structure."""
        lines = content.split('\n')
        formatted_lines = []
        question_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', '?')):
                    formatted_lines.append(f"\n❓ Question {question_num}: {line}")
                    question_num += 1
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    formatted_lines.append(f"    {line}")
                elif line.startswith(('Answer:', 'Correct:', 'Explanation:')):
                    formatted_lines.append(f"    ✅ {line}")
                else:
                    formatted_lines.append(f"    {line}")
        
        return '\n'.join(formatted_lines)
    
    def _format_flashcards(self, content: str) -> str:
        """Format flashcards content with proper structure."""
        lines = content.split('\n')
        formatted_lines = []
        card_num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith(('Q:', 'Question:', 'Front:')):
                    formatted_lines.append(f"\n🃏 Card {card_num}:")
                    formatted_lines.append(f"    ❓ {line}")
                    card_num += 1
                elif line.startswith(('A:', 'Answer:', 'Back:')):
                    formatted_lines.append(f"    ✅ {line}")
                else:
                    formatted_lines.append(f"    {line}")
        
        return '\n'.join(formatted_lines)
    
    def _format_scraped_content(self, content: str) -> str:
        """Format scraped content with proper structure."""
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if paragraph:
                # Add paragraph numbering for long content
                if len(paragraphs) > 5:
                    formatted_paragraphs.append(f"📄 Paragraph {i+1}:")
                    formatted_paragraphs.append(f"    {paragraph}")
                else:
                    formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _format_general(self, content: str) -> str:
        """Format general content with proper structure."""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Add proper indentation for sub-items
                if line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                    formatted_lines.append(f"    {line}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def scrape_website(self, url: str, extract_options: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Scrape website content with proper data preprocessing.
        
        Args:
            url (str): URL to scrape
            extract_options (Dict): Options for what to extract
            
        Returns:
            Dict: Processed scraped content
        """
        if extract_options is None:
            extract_options = {
                'text': True,
                'links': True,
                'images': True,
                'titles': True
            }
        
        logger.info(f"Scraping website: {url}")
        
        try:
            # Add headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            scraped_data = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'title': '',
                'text': '',
                'links': [],
                'images': [],
                'metadata': {}
            }
            
            # Extract title
            if extract_options.get('titles', True):
                title_tag = soup.find('title')
                if title_tag:
                    scraped_data['title'] = self.preprocess_text(title_tag.get_text())
            
            # Extract main text content
            if extract_options.get('text', True):
                # Get all text content
                text_content = soup.get_text()
                scraped_data['text'] = self.format_content(text_content, "scraped")
            
            # Extract links
            if extract_options.get('links', True):
                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    text = link.get_text().strip()
                    if href and text:
                        # Convert relative URLs to absolute
                        absolute_url = urljoin(url, href)
                        links.append({
                            'url': absolute_url,
                            'text': self.preprocess_text(text)
                        })
                scraped_data['links'] = links[:20]  # Limit to 20 links
            
            # Extract images
            if extract_options.get('images', True):
                images = []
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    alt = img.get('alt', '')
                    if src:
                        # Convert relative URLs to absolute
                        absolute_url = urljoin(url, src)
                        images.append({
                            'url': absolute_url,
                            'alt': self.preprocess_text(alt)
                        })
                scraped_data['images'] = images[:10]  # Limit to 10 images
            
            # Add metadata
            scraped_data['metadata'] = {
                'content_length': len(scraped_data['text']),
                'links_count': len(scraped_data['links']),
                'images_count': len(scraped_data['images']),
                'scraping_successful': True
            }
            
            # Store the scraped content
            self.scraped_content[url] = scraped_data
            
            logger.info(f"Successfully scraped {url}")
            return scraped_data
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'scraping_successful': False
            }
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'scraping_successful': False
            }
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF file and extract text with proper formatting.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict: Processed PDF content
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                pdf_data = {
                    'file_path': pdf_path,
                    'timestamp': datetime.now().isoformat(),
                    'total_pages': len(pdf_reader.pages),
                    'text_content': '',
                    'pages': [],
                    'metadata': {}
                }
                
                full_text = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            # Preprocess page text
                            processed_text = self.preprocess_text(page_text)
                            pdf_data['pages'].append({
                                'page_number': page_num,
                                'text': processed_text,
                                'word_count': len(processed_text.split())
                            })
                            full_text += processed_text + "\n\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")
                
                # Format the full text content
                pdf_data['text_content'] = self.format_content(full_text, "scraped")
                
                # Add metadata
                pdf_data['metadata'] = {
                    'total_words': len(full_text.split()),
                    'processing_successful': True,
                    'extracted_pages': len(pdf_data['pages'])
                }
                
                # Store the PDF content
                self.pdf_content[pdf_path] = pdf_data
                
                logger.info(f"Successfully processed PDF: {pdf_path}")
                return pdf_data
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return {
                'file_path': pdf_path,
                'error': str(e),
                'processing_successful': False
            }
    
    def generate_summary(self, content: str, content_type: str = "general") -> str:
        """
        Generate AI-powered summary with proper formatting.
        
        Args:
            content (str): Content to summarize
            content_type (str): Type of content
            
        Returns:
            str: Formatted summary
        """
        logger.info(f"Generating summary for {content_type} content")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute and helpful academic tutor. Create an adorable, structured summary with emojis and clear organization. 
                Make it fun to read! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:
                
                {content[:2000]}  # Limit content length
                """
                
                response = self.ai_model.generate_content(prompt)
                summary = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute and helpful academic tutor. Create adorable, structured summaries with emojis and clear organization. Make it fun to read! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Please summarize this {content_type} content in a cute, organized way with emojis and clear sections:\n\n{content[:2000]}"}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                summary = response.choices[0].message.content
            
            # Format the summary
            formatted_summary = self.format_content(summary, "summary")
            logger.info("Summary generated successfully")
            return formatted_summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def generate_mcq(self, content: str, num_questions: int = 5) -> str:
        """
        Generate MCQ questions with proper formatting.
        
        Args:
            content (str): Content to create questions from
            num_questions (int): Number of questions to generate
            
        Returns:
            str: Formatted MCQ questions
        """
        logger.info(f"Generating {num_questions} MCQ questions")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. 
                Make learning enjoyable! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Create {num_questions} fun multiple-choice questions with 4 options each from this content. 
                Include cute explanations and emojis:
                
                {content[:2000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                mcq = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. Make learning enjoyable! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Create {num_questions} fun multiple-choice questions with 4 options each from this content. Include cute explanations and emojis:\n\n{content[:2000]}"}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                mcq = response.choices[0].message.content
            
            # Format the MCQ
            formatted_mcq = self.format_content(mcq, "mcq")
            logger.info("MCQ questions generated successfully")
            return formatted_mcq
            
        except Exception as e:
            logger.error(f"Error generating MCQ: {e}")
            return f"Error generating MCQ: {str(e)}"
    
    def generate_flashcards(self, content: str) -> str:
        """
        Generate flashcards with proper formatting.
        
        Args:
            content (str): Content to create flashcards from
            
        Returns:
            str: Formatted flashcards
        """
        logger.info("Generating flashcards")
        
        try:
            if self.provider.lower() == "gemini":
                prompt = f"""
                You are a cute study helper! Create adorable flashcards with clear questions and answers. 
                Make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only.
                
                Create flashcards from this content. Make them cute and educational:
                
                {content[:2000]}
                """
                
                response = self.ai_model.generate_content(prompt)
                flashcards = response.text
                
            elif self.provider.lower() == "openai":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a cute study helper! Create adorable flashcards with clear questions and answers. Make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only."},
                        {"role": "user", "content": f"Create flashcards from this content. Make them cute and educational:\n\n{content[:2000]}"}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
                flashcards = response.choices[0].message.content
            
            # Format the flashcards
            formatted_flashcards = self.format_content(flashcards, "flashcards")
            logger.info("Flashcards generated successfully")
            return formatted_flashcards
            
        except Exception as e:
            logger.error(f"Error generating flashcards: {e}")
            return f"Error generating flashcards: {str(e)}"
    
    def chat_with_ai(self, message: str) -> str:
        """
        Chat with AI assistant.
        
        Args:
            message (str): User message
            
        Returns:
            str: AI response
        """
        logger.info("Processing chat message")
        
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
            
            logger.info("Chat response generated successfully")
            return ai_response
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"
    
    def save_data(self, filename: str = None):
        """Save all data to a JSON file."""
        if filename is None:
            filename = f"cute_study_hub_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'scraped_content': self.scraped_content,
            'pdf_content': self.pdf_content,
            'notes': self.notes,
            'events': self.events,
            'study_groups': self.study_groups,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to {filename}")
        return filename


def main():
    """Main function to demonstrate the Cute Study Hub."""
    print("🌸 Welcome to Cute Study Hub - Python Version! ✨")
    print("=" * 50)
    
    # Get API configuration
    api_key = input("Enter your API key: ").strip()
    provider = input("Choose provider (gemini/openai): ").strip().lower()
    
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
        print("\n🌸 Cute Study Hub Menu ✨")
        print("1. 🌐 Scrape Website")
        print("2. 📄 Process PDF")
        print("3. 📝 Generate Summary")
        print("4. ❓ Generate MCQ")
        print("5. 🃏 Generate Flashcards")
        print("6. 💬 Chat with AI")
        print("7. 💾 Save Data")
        print("8. 🚪 Exit")
        
        choice = input("\nChoose an option (1-8): ").strip()
        
        if choice == '1':
            url = input("Enter website URL: ").strip()
            if url:
                result = hub.scrape_website(url)
                print("\n📊 Scraping Results:")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Text Length: {len(result.get('text', ''))}")
                print(f"Links Found: {len(result.get('links', []))}")
                print(f"Images Found: {len(result.get('images', []))}")
                print(f"Success: {result.get('scraping_successful', False)}")
        
        elif choice == '2':
            pdf_path = input("Enter PDF file path: ").strip()
            if pdf_path:
                result = hub.process_pdf(pdf_path)
                print("\n📄 PDF Processing Results:")
                print(f"Pages: {result.get('total_pages', 0)}")
                print(f"Words: {result.get('metadata', {}).get('total_words', 0)}")
                print(f"Success: {result.get('processing_successful', False)}")
        
        elif choice == '3':
            content = input("Enter content to summarize: ").strip()
            if content:
                summary = hub.generate_summary(content)
                print("\n📝 Summary:")
                print(summary)
        
        elif choice == '4':
            content = input("Enter content for MCQ: ").strip()
            if content:
                num_q = input("Number of questions (default 5): ").strip()
                num_q = int(num_q) if num_q.isdigit() else 5
                mcq = hub.generate_mcq(content, num_q)
                print("\n❓ MCQ Questions:")
                print(mcq)
        
        elif choice == '5':
            content = input("Enter content for flashcards: ").strip()
            if content:
                flashcards = hub.generate_flashcards(content)
                print("\n🃏 Flashcards:")
                print(flashcards)
        
        elif choice == '6':
            message = input("Enter your message: ").strip()
            if message:
                response = hub.chat_with_ai(message)
                print(f"\n🤖 AI Response: {response}")
        
        elif choice == '7':
            filename = hub.save_data()
            print(f"💾 Data saved to: {filename}")
        
        elif choice == '8':
            print("👋 Goodbye! Thanks for using Cute Study Hub!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
