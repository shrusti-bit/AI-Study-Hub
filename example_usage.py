#!/usr/bin/env python3
"""
Example usage of Cute Study Hub with data preprocessing.
"""

from cute_study_hub import CuteStudyHub
import json

def main():
    """Example usage of the Cute Study Hub."""
    
    # Initialize with your API key
    API_KEY = "your-api-key-here"  # Replace with your actual API key
    PROVIDER = "gemini"  # or "openai"
    
    try:
        # Create the hub instance
        hub = CuteStudyHub(API_KEY, PROVIDER)
        print("✅ Cute Study Hub initialized!")
        
        # Example 1: Web Scraping with Data Preprocessing
        print("\n🌐 Example 1: Web Scraping")
        print("-" * 40)
        
        url = "https://www.geeksforgeeks.org/machine-learning/ml-machine-learning/"
        scraped_data = hub.scrape_website(url)
        
        print(f"📊 Scraping Results:")
        print(f"   Title: {scraped_data.get('title', 'N/A')}")
        print(f"   Text Length: {len(scraped_data.get('text', ''))}")
        print(f"   Links Found: {len(scraped_data.get('links', []))}")
        print(f"   Success: {scraped_data.get('scraping_successful', False)}")
        
        # Show a sample of the processed text
        if scraped_data.get('text'):
            sample_text = scraped_data['text'][:500] + "..." if len(scraped_data['text']) > 500 else scraped_data['text']
            print(f"\n📄 Sample Processed Text:")
            print(f"   {sample_text}")
        
        # Example 2: Generate Summary with Proper Formatting
        print("\n📝 Example 2: AI Summary Generation")
        print("-" * 40)
        
        if scraped_data.get('text'):
            summary = hub.generate_summary(scraped_data['text'], "scraped")
            print("📝 Generated Summary:")
            print(summary)
        
        # Example 3: Generate MCQ with Proper Formatting
        print("\n❓ Example 3: MCQ Generation")
        print("-" * 40)
        
        if scraped_data.get('text'):
            mcq = hub.generate_mcq(scraped_data['text'], 3)
            print("❓ Generated MCQ Questions:")
            print(mcq)
        
        # Example 4: Generate Flashcards with Proper Formatting
        print("\n🃏 Example 4: Flashcards Generation")
        print("-" * 40)
        
        if scraped_data.get('text'):
            flashcards = hub.generate_flashcards(scraped_data['text'])
            print("🃏 Generated Flashcards:")
            print(flashcards)
        
        # Example 5: Chat with AI
        print("\n💬 Example 5: AI Chat")
        print("-" * 40)
        
        chat_message = "Explain machine learning in simple terms"
        ai_response = hub.chat_with_ai(chat_message)
        print(f"👤 User: {chat_message}")
        print(f"🤖 AI: {ai_response}")
        
        # Example 6: Save All Data
        print("\n💾 Example 6: Save Data")
        print("-" * 40)
        
        filename = hub.save_data()
        print(f"💾 All data saved to: {filename}")
        
        # Show the structure of saved data
        with open(filename, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        print(f"\n📊 Saved Data Structure:")
        print(f"   Scraped Content: {len(saved_data.get('scraped_content', {}))} items")
        print(f"   PDF Content: {len(saved_data.get('pdf_content', {}))} items")
        print(f"   Notes: {len(saved_data.get('notes', []))} items")
        print(f"   Events: {len(saved_data.get('events', []))} items")
        print(f"   Study Groups: {len(saved_data.get('study_groups', []))} items")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
