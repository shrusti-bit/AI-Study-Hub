#!/usr/bin/env python3
"""
🌸 Cute Study Hub - Complete Example ✨
Demonstrates all functionalities with perfect preprocessing and beautiful formatting.
"""

from cute_study_hub_complete import CuteStudyHub
import json
from datetime import datetime, timedelta

def main():
    """Complete example demonstrating all features."""
    
    print("🌸 Cute Study Hub - Complete Example ✨")
    print("=" * 50)
    
    # Initialize with your API key
    API_KEY = "your-api-key-here"  # Replace with your actual API key
    PROVIDER = "gemini"  # or "openai"
    
    try:
        # Create the hub instance
        hub = CuteStudyHub(API_KEY, PROVIDER)
        print("✅ Cute Study Hub initialized!")
        
        # Example 1: Web Scraping with Perfect Preprocessing
        print("\n🌐 Example 1: Advanced Web Scraping")
        print("-" * 50)
        
        url = "https://www.geeksforgeeks.org/machine-learning/ml-machine-learning/"
        print(f"🔄 Scraping: {url}")
        
        scraped_data = hub.scrape_website(url)
        
        if scraped_data.get('scraping_successful', False):
            print(f"✅ Scraping successful!")
            print(f"📊 Title: {scraped_data.get('title', 'N/A')}")
            print(f"📝 Content: {scraped_data.get('word_count', 0)} words")
            print(f"🔗 Links: {len(scraped_data.get('links', []))}")
            print(f"🖼️ Images: {len(scraped_data.get('images', []))}")
            print(f"🔑 Key Phrases: {len(scraped_data.get('key_phrases', []))}")
            
            # Show sample of processed text
            if scraped_data.get('text'):
                sample_text = scraped_data['text'][:300] + "..." if len(scraped_data['text']) > 300 else scraped_data['text']
                print(f"\n📄 Sample Processed Text:")
                print(f"   {sample_text}")
        else:
            print(f"❌ Scraping failed: {scraped_data.get('error', 'Unknown error')}")
        
        # Example 2: PDF Processing with Perfect Preprocessing
        print("\n📄 Example 2: Advanced PDF Processing")
        print("-" * 50)
        
        # Note: You would need an actual PDF file for this example
        pdf_path = "sample.pdf"  # Replace with actual PDF path
        print(f"🔄 Processing PDF: {pdf_path}")
        
        # Uncomment when you have a PDF file
        # pdf_data = hub.process_pdf(pdf_path)
        # if pdf_data.get('processing_successful', False):
        #     print(f"✅ PDF processing successful!")
        #     print(f"📊 File: {pdf_data.get('file_name', 'N/A')}")
        #     print(f"📄 Pages: {pdf_data.get('total_pages', 0)}")
        #     print(f"📝 Words: {pdf_data.get('word_count', 0)}")
        #     print(f"🔑 Key Phrases: {len(pdf_data.get('key_phrases', []))}")
        # else:
        #     print(f"❌ PDF processing failed: {pdf_data.get('error', 'Unknown error')}")
        
        print("ℹ️ PDF processing example skipped (no PDF file provided)")
        
        # Example 3: AI Summary Generation with Beautiful Formatting
        print("\n📝 Example 3: AI Summary Generation")
        print("-" * 50)
        
        if scraped_data.get('text'):
            print("🔄 Generating summary...")
            summary = hub.generate_summary(scraped_data['text'], "scraped")
            print("\n📝 Generated Summary:")
            print("=" * 60)
            print(summary)
            print("=" * 60)
        
        # Example 4: MCQ Generation with Beautiful Formatting
        print("\n❓ Example 4: MCQ Generation")
        print("-" * 50)
        
        if scraped_data.get('text'):
            print("🔄 Generating MCQ questions...")
            mcq = hub.generate_mcq(scraped_data['text'], 3)
            print("\n❓ Generated MCQ Questions:")
            print("=" * 60)
            print(mcq)
            print("=" * 60)
        
        # Example 5: Flashcards Generation with Beautiful Formatting
        print("\n🃏 Example 5: Flashcards Generation")
        print("-" * 50)
        
        if scraped_data.get('text'):
            print("🔄 Generating flashcards...")
            flashcards = hub.generate_flashcards(scraped_data['text'])
            print("\n🃏 Generated Flashcards:")
            print("=" * 60)
            print(flashcards)
            print("=" * 60)
        
        # Example 6: AI Chat with Beautiful Formatting
        print("\n💬 Example 6: AI Chat")
        print("-" * 50)
        
        chat_messages = [
            "Explain machine learning in simple terms",
            "What are the main types of machine learning?",
            "How does supervised learning work?"
        ]
        
        for message in chat_messages:
            print(f"👤 User: {message}")
            response = hub.chat_with_ai(message)
            print(f"🤖 AI: {response}")
            print("-" * 40)
        
        # Example 7: Study Notes Management
        print("\n📝 Example 7: Study Notes Management")
        print("-" * 50)
        
        # Add some notes
        note1 = hub.add_note(
            "Machine Learning Basics",
            "Machine learning is a subset of artificial intelligence that enables computers to learn without explicit programming.",
            ["AI", "ML", "basics"]
        )
        
        note2 = hub.add_note(
            "Types of ML",
            "Supervised learning uses labeled data, unsupervised learning finds patterns in unlabeled data, and reinforcement learning learns through trial and error.",
            ["ML", "types", "supervised", "unsupervised"]
        )
        
        print(f"✅ Added note: {note1.title}")
        print(f"✅ Added note: {note2.title}")
        
        # Example 8: Study Events Management
        print("\n📅 Example 8: Study Events Management")
        print("-" * 50)
        
        # Add some events
        event1 = hub.add_event(
            "ML Study Session",
            "Review machine learning concepts and practice problems",
            datetime.now() + timedelta(days=1, hours=14),
            120
        )
        
        event2 = hub.add_event(
            "AI Quiz Preparation",
            "Prepare for upcoming AI quiz on supervised learning",
            datetime.now() + timedelta(days=3, hours=10),
            90
        )
        
        print(f"✅ Added event: {event1.title}")
        print(f"✅ Added event: {event2.title}")
        
        # Example 9: Study Groups Management
        print("\n👥 Example 9: Study Groups Management")
        print("-" * 50)
        
        # Create study groups
        group1 = hub.create_study_group(
            "ML Study Group",
            "Weekly study group for machine learning concepts",
            ["Alice", "Bob", "Charlie"]
        )
        
        group2 = hub.create_study_group(
            "AI Research Team",
            "Advanced AI research and development team",
            ["David", "Eve", "Frank"]
        )
        
        print(f"✅ Created group: {group1.name}")
        print(f"✅ Created group: {group2.name}")
        
        # Example 10: Data Persistence
        print("\n💾 Example 10: Data Persistence")
        print("-" * 50)
        
        # Save all data
        filename = hub.save_data()
        print(f"💾 All data saved to: {filename}")
        
        # Show statistics
        print("\n📊 Final Statistics:")
        print("=" * 30)
        print(f"📝 Notes: {len(hub.notes)}")
        print(f"📅 Events: {len(hub.events)}")
        print(f"👥 Study Groups: {len(hub.study_groups)}")
        print(f"🌐 Scraped Websites: {len(hub.scraped_content)}")
        print(f"📄 Processed PDFs: {len(hub.pdf_content)}")
        print("=" * 30)
        
        # Example 11: Data Loading
        print("\n📂 Example 11: Data Loading")
        print("-" * 50)
        
        # Create a new hub instance
        hub2 = CuteStudyHub(API_KEY, PROVIDER)
        
        # Load data
        hub2.load_data(filename)
        print(f"✅ Data loaded successfully!")
        print(f"📝 Loaded notes: {len(hub2.notes)}")
        print(f"📅 Loaded events: {len(hub2.events)}")
        print(f"👥 Loaded groups: {len(hub2.study_groups)}")
        
        print("\n🎉 All examples completed successfully!")
        print("🌸 Cute Study Hub - Perfect Preprocessing & Beautiful Formatting ✨")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
