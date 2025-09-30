#!/usr/bin/env python3
"""
Script to generate large test files with 300,000+ words each.
"""

import os

def generate_large_content(base_text, target_words=300000):
    """Generate large content by repeating and varying the base text."""
    # Split base text into words
    words = base_text.split()
    base_word_count = len(words)
    
    # Calculate how many repetitions we need
    repetitions_needed = target_words // base_word_count + 1
    
    # Generate the content
    large_content = []
    
    for i in range(repetitions_needed):
        # Add variation to make it more realistic
        varied_words = []
        for word in words:
            if i > 0:
                # Add some variation every few repetitions
                if i % 100 == 0 and word[0].isalpha():
                    varied_words.append(word.capitalize())
                elif i % 200 == 0 and word.endswith('.'):
                    varied_words.append(word.replace('.', '!'))
                else:
                    varied_words.append(word)
            else:
                varied_words.append(word)
        
        large_content.extend(varied_words)
        
        # Add paragraph breaks periodically
        if i % 50 == 0 and i > 0:
            large_content.append('\n\n')
        
        # Stop if we've reached our target
        if len(large_content) >= target_words:
            break
    
    return ' '.join(large_content[:target_words])

def main():
    # Base content for each test file
    test_contents = {
        'test1.txt': """This is test file 1. It contains sample text for testing purposes. You can use this file to test document processing functionality. The content is designed to be processed by various text analysis tools and document vectorization systems. This file serves as a benchmark for testing the performance and accuracy of document processing algorithms. Each sentence is carefully crafted to provide meaningful content while maintaining readability and coherence.""",
        
        'test2.txt': """This is test file 2. This file contains different content to test various scenarios. It includes some numbers: 123, 456, 789. And some special characters: @#$%^&*(). The file also contains technical terms and programming concepts like API, database, algorithm, and machine learning. This diverse content helps test how document processing systems handle different types of text including alphanumeric sequences, special symbols, and technical vocabulary.""",
        
        'test3.txt': """Test file 3 - Sample document. This is a longer text sample that spans multiple lines. It can be used to test document analysis and processing features. The content includes various sentence structures and punctuation marks. This helps ensure the system handles different text formats correctly. The document contains comprehensive information about software development, data science, and artificial intelligence concepts that are commonly used in modern applications.""",
        
        'test4.txt': """Test Document 4. This file demonstrates structured text with headers. It includes bullet points and numbered lists. This format tests how the system handles formatted documents. The content covers topics such as web development, cloud computing, cybersecurity, and software engineering best practices. Each section provides detailed explanations of complex technical concepts in a structured format that is easy to read and understand.""",
        
        'test5.txt': """Final test file for the document collection. This contains technical terms: API, JSON, HTTP, REST. Also includes dates: 2024-01-15, March 2024. And some code-like text: function test() { return true; }. Perfect for testing various text processing scenarios. The file covers advanced topics in computer science including algorithms, data structures, system design, and software architecture patterns that are essential for building scalable applications."""
    }
    
    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)
    
    # Generate large files
    for filename, base_content in test_contents.items():
        print(f"Generating {filename}...")
        large_content = generate_large_content(base_content, 300000)
        
        filepath = os.path.join('docs', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(large_content)
        
        # Count actual words
        word_count = len(large_content.split())
        print(f"Generated {filename} with {word_count:,} words")
    
    print("All large test files generated successfully!")

if __name__ == "__main__":
    main()
