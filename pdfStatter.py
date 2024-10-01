# i have a project i want to make using python numpy and matplotlib
# it's a pdf to graph project, i execute the program giving it a pdf, and it will read and give me a few graphs with fun statts about the pdf, like, characters in order of usage, the first word of evry chapter, if the book has color and the nunber of word per page and so on...
import PyPDF2
import collections
import re
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# PDF extraction and analysis functions

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in tqdm(range(num_pages), desc="Extracting text from PDF", unit="page"):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def character_frequency(text):
    return collections.Counter(text)

def first_word_of_chapters(text):
    chapters = re.split(r'\bChapter\b', text)
    first_words = []
    for chapter in tqdm(chapters[1:], desc="Extracting first words of chapters", unit="chapter"):
        words = chapter.strip().split()
        if words:
            first_words.append(words[0])
    return first_words

def words_per_page(pdf_file):
    words_per_page_list = []
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in tqdm(range(num_pages), desc="Counting words per page", unit="page"):
            page = reader.pages[page_num]
            text = page.extract_text()
            word_count = len(text.split())
            words_per_page_list.append(word_count)
    return words_per_page_list

# Visualization functions

def plot_character_frequency(frequencies):
    labels, values = zip(*frequencies.items())
    indexes = range(len(labels))
    plt.bar(indexes, values)
    plt.xticks(indexes, labels)
    plt.xlabel("Characters")
    plt.ylabel("Frequency")
    plt.title("Character Frequency in PDF")
    plt.show()

def plot_words_per_page(word_counts):
    plt.plot(word_counts)
    plt.xlabel("Page Number")
    plt.ylabel("Word Count")
    plt.title("Word Count Per Page")
    plt.show()

# Main function to analyze PDF

def analyze_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)

    # Character frequency
    char_freq = character_frequency(text)
    print("Character frequency:", char_freq)
    plot_character_frequency(char_freq)

    # First word of each chapter
    first_words = first_word_of_chapters(text)
    print("First words of chapters:", first_words)

    # Words per page
    words_per_page_list = words_per_page(pdf_file)
    print("Words per page:", words_per_page_list)
    plot_words_per_page(words_per_page_list)

# Usage
pdf_file_path = "C:/Users/rudyq/Downloads/bible.pdf"  # Replace with your PDF file path
analyze_pdf(pdf_file_path)
