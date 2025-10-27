// Global variables
let currentUser = null;
let extractedPdfText = '';
let scrapedWebsiteContent = '';
let currentAction = null; // Track current action to fix button issues

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌸 Cute Study Hub initialized! ✨');
    startClock();
    loadUserData();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // PDF input handler
    const pdfInput = document.getElementById('pdfInput');
    if (pdfInput) {
        pdfInput.addEventListener('change', handlePdfUpload);
    }
    
    // Drag and drop for PDF
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('drop', handleDrop);
    }
}

// Login function
function login() {
    const apiKey = document.getElementById('apiKey').value.trim();
    const provider = document.getElementById('apiProvider').value;
    
    if (!apiKey) {
        showNotification('Please enter your API key! 🔑', 'warning');
        return;
    }
    
    currentUser = { apiKey, provider };
    localStorage.setItem('cuteStudyHub_user', JSON.stringify(currentUser));
    
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';
    
    showNotification('Welcome to Cute Study Hub! ✨', 'success');
}

// Logout function
function logout() {
    currentUser = null;
    localStorage.removeItem('cuteStudyHub_user');
    
    document.getElementById('loginScreen').style.display = 'block';
    document.getElementById('mainApp').style.display = 'none';
    
    showNotification('Logged out successfully! 👋', 'info');
}

// Load user data
function loadUserData() {
    const saved = localStorage.getItem('cuteStudyHub_user');
    if (saved) {
        currentUser = JSON.parse(saved);
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('mainApp').style.display = 'block';
    }
}

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Clear all outputs when switching sections
    clearAllOutputs();
}

// Clear all outputs
function clearAllOutputs() {
    const outputs = ['summaryOutput', 'mcqOutput', 'flashcardsOutput', 'scrapedContent', 'pdfContent', 'chatLog'];
    outputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = '';
        }
    });
}

// AI Assistant Functions
async function generateSummary() {
    const inputText = document.getElementById('inputText');
    const summaryOutput = document.getElementById('summaryOutput');
    
    if (!inputText.value.trim()) {
        showNotification('Please enter some content first! 💭', 'warning');
        return;
    }
    
    // Clear other outputs
    document.getElementById('mcqOutput').textContent = '';
    document.getElementById('flashcardsOutput').textContent = '';
    
    try {
        summaryOutput.innerHTML = '<div class="loading"></div> Creating adorable summary... ✨';
        currentAction = 'summary';
        
        const prompt = [
            { role: 'system', content: 'You are a cute and helpful academic tutor. Create adorable, structured summaries with emojis and clear organization. Make it fun to read! Do not use asterisk symbols (*) for formatting. Use plain text only.' },
            { role: 'user', content: `Summarize this content in a cute, organized way with emojis and clear sections. Do not use asterisk symbols (*) for formatting:\n\n${inputText.value}` }
        ];
        
        const result = await callLLM(prompt, { max_tokens: 4000, temperature: 0.7 });
        
        if (result && result.trim()) {
            summaryOutput.innerHTML = result.replace(/\n/g, '<br>');
            showNotification('Summary created successfully! ✨', 'success');
        } else {
            summaryOutput.textContent = 'No summary was generated. Please try again.';
        }
    } catch (err) {
        summaryOutput.textContent = `Error: ${err.message}`;
        showNotification('Failed to generate summary. Please check your API key.', 'error');
    }
}

async function generateMCQs() {
    const inputText = document.getElementById('inputText');
    const mcqOutput = document.getElementById('mcqOutput');
    
    if (!inputText.value.trim()) {
        showNotification('Please enter some content first! 💭', 'warning');
        return;
    }
    
    // Clear other outputs
    document.getElementById('summaryOutput').textContent = '';
    document.getElementById('flashcardsOutput').textContent = '';
    
    try {
        mcqOutput.innerHTML = '<div class="loading"></div> Creating fun MCQs... ❓✨';
        currentAction = 'mcq';
        
        const prompt = [
            { role: 'system', content: 'You are a fun quiz creator! Make engaging MCQs with cute explanations and emojis. Make learning enjoyable! Do not use asterisk symbols (*) for formatting. Use plain text only.' },
            { role: 'user', content: `Create 5 fun multiple-choice questions with 4 options each from this content. Include cute explanations and emojis. Do not use asterisk symbols (*) for formatting:\n\n${inputText.value}` }
        ];
        
        const result = await callLLM(prompt, { max_tokens: 4000, temperature: 0.7 });
        
        if (result && result.trim()) {
            mcqOutput.innerHTML = result.replace(/\n/g, '<br>');
            showNotification('MCQs created successfully! ✨', 'success');
        } else {
            mcqOutput.textContent = 'No MCQs were generated. Please try again.';
        }
    } catch (err) {
        mcqOutput.textContent = `Error: ${err.message}`;
        showNotification('Failed to generate MCQs. Please check your API key.', 'error');
    }
}

async function generateFlashcards() {
    const inputText = document.getElementById('inputText');
    const flashcardsOutput = document.getElementById('flashcardsOutput');
    
    if (!inputText.value.trim()) {
        showNotification('Please enter some content first! 💭', 'warning');
        return;
    }
    
    // Clear other outputs
    document.getElementById('summaryOutput').textContent = '';
    document.getElementById('mcqOutput').textContent = '';
    
    try {
        flashcardsOutput.innerHTML = '<div class="loading"></div> Creating cute flashcards... 🃏✨';
        currentAction = 'flashcards';
        
        const prompt = [
            { role: 'system', content: 'You are a cute study helper! Create adorable flashcards with clear questions and answers. Make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only.' },
            { role: 'user', content: `Create flashcards from this content. Make them cute and educational. Do not use asterisk symbols (*) for formatting:\n\n${inputText.value}` }
        ];
        
        const result = await callLLM(prompt, { max_tokens: 4000, temperature: 0.7 });
        
        if (result && result.trim()) {
            flashcardsOutput.innerHTML = result.replace(/\n/g, '<br>');
            showNotification('Flashcards created successfully! 🃏✨', 'success');
        } else {
            flashcardsOutput.textContent = 'No flashcards were generated. Please try again.';
        }
    } catch (err) {
        flashcardsOutput.textContent = `Error: ${err.message}`;
        showNotification('Failed to generate flashcards. Please check your API key.', 'error');
    }
}

// Web Scraper - Using backend endpoint
async function scrapeWebsite() {
    const urlInput = document.getElementById('scrapeUrl');
    const scrapedContent = document.getElementById('scrapedContent');
    
    if (!urlInput.value.trim()) {
        showNotification('Please enter a URL! 🌐', 'warning');
        return;
    }
    
    try {
        scrapedContent.innerHTML = '<div class="loading"></div> Scraping website... 🕷️✨';
        
        const url = urlInput.value.trim();
        
        // Use the backend Flask endpoint for scraping
        const response = await fetch('/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url
            })
        });
        
        const result = await response.json();
        
        if (result.scraping_successful) {
            scrapedWebsiteContent = result.text;
            scrapedContent.innerHTML = `
                <h3>✅ Website Scraped Successfully!</h3>
                <p><strong>Title:</strong> ${result.title}</p>
                <p><strong>URL:</strong> ${result.url}</p>
                <p><strong>Word Count:</strong> ${result.word_count}</p>
                <p><strong>Links Found:</strong> ${result.links ? result.links.length : 0}</p>
                <p><strong>Images Found:</strong> ${result.images ? result.images.length : 0}</p>
                <hr>
                <h4>Content Preview:</h4>
                <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background: #f9f9f9;">
                    ${result.text.substring(0, 2000)}${result.text.length > 2000 ? '...' : ''}
                </div>
            `;
            showNotification('Website scraped successfully! ✨', 'success');
        } else {
            scrapedContent.innerHTML = `
                <h3>❌ Scraping Failed</h3>
                <p><strong>Error:</strong> ${result.error || 'Unknown error'}</p>
                <p><strong>URL:</strong> ${result.url}</p>
            `;
            showNotification('Failed to scrape website. Please try a different URL.', 'error');
        }
    } catch (err) {
        scrapedContent.innerHTML = `
            <h3>❌ Error</h3>
            <p><strong>Error:</strong> ${err.message}</p>
        `;
        showNotification('Failed to scrape website.', 'error');
    }
}

// PDF Magic - Optimized for speed
function handlePdfUpload(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        processPDF(file);
    } else {
        showNotification('Please select a valid PDF file! 📄', 'warning');
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.style.background = 'linear-gradient(145deg, #fff0f5, #ffe4e1)';
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.style.background = 'linear-gradient(145deg, #ffffff, #f8f8f8)';
    
    const files = event.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
        processPDF(files[0]);
    }
}

async function processPDF(file) {
    try {
        const pdfContent = document.getElementById('pdfContent');
        const pdfActions = document.getElementById('pdfActions');
        
        pdfContent.innerHTML = '<div class="loading"></div> Processing PDF... 📄✨';
        
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
        
        let fullText = '';
        const maxPages = Math.min(pdf.numPages, 10); // Limit to 10 pages for speed
        
        for (let i = 1; i <= maxPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');
            fullText += pageText + '\n\n';
        }
        
        extractedPdfText = fullText;
        
        pdfContent.innerHTML = `✅ PDF processed successfully!<br><br>${fullText.substring(0, 1500)}...`;
        pdfActions.style.display = 'block';
        
        showNotification('PDF processed successfully! ✨', 'success');
    } catch (error) {
        document.getElementById('pdfContent').textContent = 'Error processing PDF: ' + error.message;
        showNotification('Error processing PDF! 📄', 'error');
    }
}

function showQuestionInput() {
    const question = prompt('Ask a question about your PDF: 💭');
    if (question) {
        answerPdfQuestion(question);
    }
}

async function answerPdfQuestion(question) {
    if (!extractedPdfText) {
        showNotification('Please upload a PDF first! 📄', 'warning');
        return;
    }
    
    try {
        const pdfContent = document.getElementById('pdfContent');
        pdfContent.innerHTML += '<br><br><div class="loading"></div> Thinking... 🤔';
        
        const prompt = [
            { role: 'system', content: 'You are a helpful AI assistant. Answer questions based on the provided PDF content. Be accurate and helpful.' },
            { role: 'user', content: `PDF Content:\n${extractedPdfText}\n\nQuestion: ${question}` }
        ];
        
        const result = await callLLM(prompt, { max_tokens: 3000, temperature: 0.7 });
        pdfContent.innerHTML = pdfContent.innerHTML.replace('<div class="loading"></div> Thinking... 🤔', '');
        pdfContent.innerHTML += `<br><br><strong>Q: ${question}</strong><br>${result}`;
    } catch (err) {
        showNotification('Error answering question: ' + err.message, 'error');
    }
}

async function summarizePdf() {
    if (!extractedPdfText) {
        showNotification('Please upload a PDF first! 📄', 'warning');
        return;
    }
    
    try {
        const pdfContent = document.getElementById('pdfContent');
        pdfContent.innerHTML += '<br><br><div class="loading"></div> Creating summary... 📄✨';
        
        const prompt = [
            { role: 'system', content: 'You are a helpful AI assistant. Create a comprehensive summary of the provided PDF content.' },
            { role: 'user', content: `Please summarize this PDF content:\n\n${extractedPdfText}` }
        ];
        
        const result = await callLLM(prompt, { max_tokens: 3000, temperature: 0.7 });
        pdfContent.innerHTML = pdfContent.innerHTML.replace('<div class="loading"></div> Creating summary... 📄✨', '');
        pdfContent.innerHTML += `<br><br><strong>PDF Summary:</strong><br>${result}`;
    } catch (err) {
        showNotification('Error summarizing PDF: ' + err.message, 'error');
    }
}

// Notes
function showAddNoteModal() {
    const title = prompt('Note title: 📝');
    if (title) {
        const content = prompt('Note content: 💭');
        if (content) {
            addNote(title, content);
        }
    }
}

function addNote(title, content) {
    const notesGrid = document.getElementById('notesGrid');
    const noteElement = document.createElement('div');
    noteElement.className = 'note-card';
    noteElement.innerHTML = `
        <h3>${title}</h3>
        <p>${content}</p>
        <button onclick="deleteNote(this)" class="btn-cute-3d">Delete</button>
    `;
    notesGrid.appendChild(noteElement);
    showNotification('Note added successfully! ✨', 'success');
}

function deleteNote(button) {
    button.parentElement.remove();
    showNotification('Note deleted!', 'info');
}

// Calendar
function showAddEventModal() {
    const title = prompt('Event title: 📅');
    if (title) {
        const date = prompt('Event date (YYYY-MM-DD): 📆');
        if (date) {
            addEvent(title, date);
        }
    }
}

function addEvent(title, date) {
    const calendarGrid = document.getElementById('calendarGrid');
    const eventElement = document.createElement('div');
    eventElement.className = 'event-card';
    eventElement.innerHTML = `
        <h3>${title}</h3>
        <p>Date: ${date}</p>
        <button onclick="deleteEvent(this)" class="btn-cute-3d">Delete</button>
    `;
    calendarGrid.appendChild(eventElement);
    showNotification('Event added successfully! ✨', 'success');
}

function deleteEvent(button) {
    button.parentElement.remove();
    showNotification('Event deleted!', 'info');
}

// Timer & Clock
let timerInterval = null;
let timerSeconds = 0;

function startClock() {
    updateClock();
    setInterval(updateClock, 1000);
}

function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    const clockDisplay = document.getElementById('clockDisplay');
    if (clockDisplay) {
        clockDisplay.textContent = `🕐 ${timeString}`;
    }
}

function startTimer() {
    if (timerInterval) return;
    
    timerInterval = setInterval(() => {
        timerSeconds++;
        updateTimerDisplay();
    }, 1000);
    
    showNotification('Timer started! ⏰', 'info');
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        showNotification('Timer stopped! ⏹️', 'info');
    }
}

function updateTimerDisplay() {
    const hours = Math.floor(timerSeconds / 3600);
    const minutes = Math.floor((timerSeconds % 3600) / 60);
    const seconds = timerSeconds % 60;
    
    const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    const timerDisplay = document.getElementById('timerDisplay');
    if (timerDisplay) {
        timerDisplay.textContent = `⏱️ ${timeString}`;
    }
}

// Study Groups
function showCreateGroupForm() {
    const name = prompt('Group name: 👥');
    if (name) {
        const description = prompt('Group description: 💭');
        createStudyGroup(name, description || '');
    }
}

function createStudyGroup(name, description) {
    const studyGroupsList = document.getElementById('studyGroupsList');
    const groupElement = document.createElement('div');
    groupElement.className = 'group-card';
    groupElement.innerHTML = `
        <h3>${name}</h3>
        <p>${description}</p>
        <button onclick="deleteGroup(this)" class="btn-cute-3d">Delete</button>
    `;
    studyGroupsList.appendChild(groupElement);
    showNotification('Study group created! ✨', 'success');
}

function deleteGroup(button) {
    button.parentElement.remove();
    showNotification('Group deleted!', 'info');
}

// Wellness
function toggleEyeReminders() {
    showNotification('Eye reminders toggled! 👁️', 'info');
}

function togglePostureReminders() {
    showNotification('Posture reminders toggled! 🧘', 'info');
}

// Chat
async function sendChatMessage() {
    const chatInput = document.getElementById('chatPrompt');
    const chatLog = document.getElementById('chatLog');
    
    if (!chatInput.value.trim()) {
        showNotification('Please enter a message! 💭', 'warning');
        return;
    }
    
    const message = chatInput.value.trim();
    chatInput.value = '';
    
    // Add user message
    addChatMessage(message, 'user');
    
    try {
        const prompt = [
            { role: 'system', content: 'You are a cute and helpful AI study companion. Be friendly, encouraging, and helpful with academic topics. Use emojis and make learning fun! Do not use asterisk symbols (*) for formatting. Use plain text only.' },
            { role: 'user', content: message }
        ];
        
        const response = await callLLM(prompt, { max_tokens: 3000, temperature: 0.7 });
        addChatMessage(response, 'assistant');
    } catch (err) {
        addChatMessage(`Error: ${err.message}`, 'assistant');
    }
}

function addChatMessage(message, sender) {
    const chatLog = document.getElementById('chatLog');
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${sender}`;
    messageElement.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI'}:</strong> ${message}`;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Utility Functions
function extractTextFromHTML(html) {
    const temp = document.createElement('div');
    temp.innerHTML = html;
    return temp.textContent || temp.innerText || '';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.background = type === 'error' ? 'linear-gradient(145deg, #ff6b6b, #ee5a52)' : 
                                  type === 'success' ? 'linear-gradient(145deg, #51cf66, #40c057)' :
                                  type === 'warning' ? 'linear-gradient(145deg, #ffd43b, #fab005)' :
                                  'linear-gradient(145deg, #74c0fc, #339af0)';
    notification.style.color = 'white';
    notification.style.padding = '15px 25px';
    notification.style.borderRadius = '15px';
    notification.style.boxShadow = '0 8px 25px rgba(0,0,0,0.2)';
    notification.style.zIndex = '1000';
    notification.style.fontWeight = 'bold';
    notification.style.animation = 'slideIn 0.5s ease';
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// API Functions
async function callLLM(prompt, options = {}) {
    if (!currentUser) {
        throw new Error('Please login first!');
    }
    
    if (currentUser.provider === 'openai') {
        return await callOpenAI(prompt, currentUser.apiKey, options);
    } else {
        return await callGemini(prompt, currentUser.apiKey, options);
    }
}

async function callOpenAI(prompt, apiKey, options = {}) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: prompt,
            max_tokens: options.max_tokens || 2000,
            temperature: options.temperature || 0.7
        })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(`OpenAI: ${response.status} ${error.error?.message || 'Unknown error'}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
}

async function callGemini(prompt, apiKey, options = {}) {
    const model = 'gemini-2.5-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contents: [{
                parts: [{
                    text: prompt.map(p => `${p.role}: ${p.content}`).join('\n\n')
                }]
            }],
            generationConfig: {
                maxOutputTokens: options.max_tokens || 2000,
                temperature: options.temperature || 0.7
            }
        })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(`Gemini: ${response.status} ${error.error?.message || 'Unknown error'}`);
    }
    
    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
}

// Make functions globally accessible
window.login = login;
window.logout = logout;
window.showSection = showSection;
window.generateSummary = generateSummary;
window.generateMCQs = generateMCQs;
window.generateFlashcards = generateFlashcards;
window.scrapeWebsite = scrapeWebsite;
window.showQuestionInput = showQuestionInput;
window.answerPdfQuestion = answerPdfQuestion;
window.summarizePdf = summarizePdf;
window.showAddNoteModal = showAddNoteModal;
window.addNote = addNote;
window.deleteNote = deleteNote;
window.showAddEventModal = showAddEventModal;
window.addEvent = addEvent;
window.deleteEvent = deleteEvent;
window.startTimer = startTimer;
window.stopTimer = stopTimer;
window.showCreateGroupForm = showCreateGroupForm;
window.createStudyGroup = createStudyGroup;
window.deleteGroup = deleteGroup;
window.toggleEyeReminders = toggleEyeReminders;
window.togglePostureReminders = togglePostureReminders;
window.sendChatMessage = sendChatMessage;
window.handlePdfUpload = handlePdfUpload;
window.handleDragOver = handleDragOver;
window.handleDrop = handleDrop;