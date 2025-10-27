# AI Study Workspace

Python-based AI-driven productivity platform that transforms study materials into interactive learning tools through automated summarization, quiz generation, intelligent content processing, comprehensive note management,web and PDF scraping and AI chatbot assistance.

## 📋 Project Overview

This comprehensive study workspace combines the power of artificial intelligence with modern web technologies to create an all-in-one learning platform. The application processes various content sources (websites, PDFs, text input) and transforms them into interactive learning materials through advanced AI processing.

### Key Capabilities:
- **Content Ingestion**: Scrape websites, process PDFs, and handle text input
- **AI Processing**: Generate summaries, quizzes, flashcards, and provide chat assistance
- **Data Management**: Persistent storage with search and organization features
- **Real-time Features**: Live updates, progress indicators, and instant feedback
- **Cross-platform**: Works on desktop and mobile devices with responsive design

### Target Users:
- Students and researchers needing efficient study tools
- Educators creating interactive learning materials
- Professionals requiring content summarization and analysis
- Anyone looking to enhance their learning productivity

## 🚀 Features

### AI-Powered Tools
- **Content Summarization**: Automated concept summarization with structured output and beautiful formatting
- **MCQ Generation**: Personalized multiple-choice questions with explanations and cute emojis
- **Flashcard Creation**: Custom flashcards following spaced repetition principles with organized Q&A pairs
- **AI Chatbot**: Conversational assistant with persistent chat history and real-time responses
- **Doubt Solver**: AI-powered doubt resolution and concept explanation with academic focus

### Web Scraping & Content Processing
- **Advanced Web Scraping**: Extract content from any website with intelligent data preprocessing
- **Perfect Data Cleaning**: Remove noise, fix formatting issues, and normalize text content
- **Link & Image Extraction**: Process and categorize all media elements from scraped pages
- **Metadata Collection**: Comprehensive data about scraped content including word counts and timestamps
- **Real-time Scraping**: Live progress indicators and instant feedback during scraping process
- **Content Validation**: Automatic validation and error handling for scraped data

### PDF Processing & Document Analysis
- **PDF Text Extraction**: Extract and process text from PDF files with page-by-page analysis
- **Advanced PDF Parsing**: Handle complex PDF layouts and formatting with PyPDF2
- **Content Preprocessing**: Clean and format extracted text for optimal AI processing
- **Page-by-Page Analysis**: Individual page processing with word count and content validation
- **File Management**: Secure file uploads with automatic processing and storage
- **Multi-format Support**: Support for various PDF types and document structures

### Productivity Features
- **Notes Management**: Rich note-taking with search, organization, and tagging system
- **Meeting Scheduler**: Calendar integration with .ics export and Google Calendar sync
- **Email Integration**: Quick email composition and sending functionality
- **Study Group Clustering**: AI-powered study group suggestions using k-means clustering
- **Wellness Reminders**: Eye-break and posture reminders for healthy study habits

### Professional UI
- **Notion-like Design**: Clean, modern interface with sidebar navigation
- **Responsive Layout**: Works on desktop and mobile devices
- **Dark/Light Theme**: Professional color scheme with excellent contrast
- **Database Integration**: IndexedDB for persistent data storage

## 🗄️ Database Schema

The app uses IndexedDB with the following stores:
- **notes**: User notes with title, content, and timestamps
- **meetings**: Scheduled meetings with dates and durations
- **chatHistory**: Persistent chat conversations
- **studyGroups**: Generated study group suggestions

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-study-workspace.git
cd ai-study-workspace
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
- Open your browser and go to `http://localhost:5001`
- The application will load with a beautiful, responsive interface

### Step 5: Configure AI APIs
1. **Get API Keys**:
   - OpenAI: Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Google Gemini: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Configure in App**:
   - Select your preferred AI provider (OpenAI or Gemini)
   - Enter your API key
   - Click "Login" to start using AI features

## 🚀 Quick Start

1. **Open the app**: Navigate to `http://localhost:5001` in your browser
2. **Configure API**: Select provider (OpenAI/Gemini) and enter your API key
3. **Start using**: Navigate sections via sidebar, all data persists automatically

## 🔧 API Configuration

### OpenAI
- Uses Chat Completions API (`gpt-4o-mini` by default)
- Key stored in browser localStorage

### Gemini
- Uses Generative Language API (`gemini-1.5-flash` by default)
- Key stored in browser localStorage

## 📱 Usage

### AI Assistant
- Paste content and generate summaries, MCQs, or flashcards
- Chat with AI for questions and discussions
- All conversations are saved to database

### Notes
- Create, edit, and delete notes
- Search functionality across all notes
- Automatic timestamping and organization

### Meetings
- Schedule meetings with date/time
- Export to .ics format
- Open in Google Calendar
- All meetings stored in database

### Study Groups
- Enter member names and topics
- AI clustering algorithm suggests optimal groups
- Save group configurations

### Wellness
- Toggle eye-break reminders (20-20-20 rule)
- Posture reminders
- Doubt-solving with AI assistance

## 🛠️ Technical Stack

### Backend & AI Integration
- **Python Flask**: Web framework for API endpoints and server-side processing
- **Flask-SocketIO**: Real-time communication and live updates
- **OpenAI API**: GPT-3.5-turbo and GPT-4 integration for AI functionalities
- **Google Gemini API**: Alternative AI provider with gemini-2.5-flash model
- **PyPDF2**: Advanced PDF text extraction and processing
- **BeautifulSoup4**: Web scraping and HTML content parsing
- **Requests**: HTTP library for web scraping and API calls

### Frontend & User Interface
- **HTML5**: Semantic markup with modern web standards
- **CSS3**: Advanced styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Modern JavaScript with async/await and fetch API
- **IndexedDB**: Client-side database for persistent data storage
- **WebSocket**: Real-time communication for live updates

### Data Processing & Storage
- **JSON**: Data serialization and configuration management
- **UUID**: Unique identifier generation for data entities
- **Text Processing**: Advanced regex and string manipulation
- **File Management**: Secure file uploads and processing
- **Data Validation**: Comprehensive input validation and error handling

### Development & Deployment
- **Flask Development Server**: Local development and testing
- **CORS Support**: Cross-origin resource sharing for web integration
- **Logging**: Comprehensive logging system for debugging
- **Error Handling**: Robust error management and user feedback

## 🔒 Security & Privacy

- All data stored locally in your browser
- API keys stored in localStorage (browser-only)
- No server-side data transmission
- For production: implement backend proxy for API keys

## 🚀 Future Enhancements

### Server-Side Integration
- Django REST Framework for backend API
- PostgreSQL for advanced data management
- User authentication and multi-user support

### AI/ML Features
- spaCy for advanced NLP processing
- BERT for semantic search
- Pandas for data analysis
- Custom ML models for personalized learning

### Design & Collaboration
- Figma integration for design workflows
- Git integration for version control
- Real-time collaboration features
- Advanced note formatting and templates

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

This is a static application. For enhancements:
1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the browser console for errors
- Ensure API keys are valid and have sufficient credits
- Verify IndexedDB is supported in your browser
