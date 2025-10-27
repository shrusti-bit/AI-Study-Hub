# AI Study Workspace

Python-based AI-driven productivity platform that transforms study materials into interactive learning tools through automated summarization, quiz generation, intelligent content processing, comprehensive note management, and AI chatbot assistance.

## 🚀 Features

### AI-Powered Tools
- **Content Summarization**: Automated concept summarization with structured output
- **MCQ Generation**: Personalized multiple-choice questions with explanations
- **Flashcard Creation**: Custom flashcards following spaced repetition principles
- **AI Chatbot**: Conversational assistant with persistent chat history
- **Doubt Solver**: AI-powered doubt resolution and concept explanation

### Productivity Features
- **Notes Management**: Rich note-taking with search and organization
- **Meeting Scheduler**: Calendar integration with .ics export and Google Calendar
- **Email Integration**: Quick email composition and sending
- **Study Group Clustering**: AI-powered study group suggestions using k-means
- **Wellness Reminders**: Eye-break and posture reminders

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

## 🚀 Quick Start

1. **Open the app**: Double-click `index.html` or serve via local server
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

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: IndexedDB for client-side persistence
- **AI APIs**: OpenAI Chat Completions, Google Gemini
- **Styling**: Custom CSS with Notion-inspired design
- **Responsive**: Mobile-first design with breakpoints

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
