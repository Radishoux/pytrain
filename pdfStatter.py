# i have a project i want to make using python numpy and matplotlib
# it's a pdf to graph project, i execute the program giving it a pdf, and it will read and give me a few graphs with fun statts about the pdf, like, characters in order of usage, the first word of evry chapter, if the book has color and the nunber of word per page and so on...
import PyPDF2
import collections
import re
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from wordcloud import WordCloud
from collections import Counter


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
            words = text.split()
            words_per_page_list.append(len(words))

    return words_per_page_list

# Visualization functions

def plot_character_frequency(frequencies):
    sorted_freq = dict(sorted(frequencies.items(), key=lambda item: ord(item[0])))
    labels, values = zip(*sorted_freq.items())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.xlabel("Character")
    plt.ylabel("Frequency")
    plt.title("Character Frequency")
    plt.show()

def plot_words_per_page(word_counts):
    word_counts_array = np.array(word_counts)
    mean = np.mean(word_counts_array)
    median = np.median(word_counts_array)
    std_dev = np.std(word_counts_array)

    plt.plot(word_counts, label='Word Count')
    plt.axhline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}')
    plt.axhline(median, color='g', linestyle='-.', label=f'Median: {median:.2f}')
    plt.fill_between(range(len(word_counts)), mean - std_dev, mean + std_dev, color='b', alpha=0.2, label=f'Std Dev: {std_dev:.2f}')

    plt.xlabel("Page Number")
    plt.ylabel("Word Count")
    plt.title("Word Count Per Page")
    plt.legend()
    plt.show()

def words_per_quarter_page(pdf_file):
    words_per_quarter_page_list = []
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in tqdm(range(num_pages), desc="Counting words per quarter page", unit="page"):
            page = reader.pages[page_num]
            text = page.extract_text()
            words = text.split()
            quarter_length = len(words) // 4

            for i in range(4):
                start_index = i * quarter_length
                end_index = (i + 1) * quarter_length if i < 3 else len(words)
                quarter_words = words[start_index:end_index]
                words_per_quarter_page_list.append(len(quarter_words))

    return words_per_quarter_page_list


def plot_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Word Cloud")
    plt.show()

def plot_top_20_words_pie(text):
    words = text.split()
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(20)

    labels, values = zip(*most_common_words)

    plt.figure(figsize=(10, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Top 20 Most Used Words")
    plt.show()

def plot_character_frequency_pie(frequencies):
    labels, values = zip(*frequencies.items())
    plt.figure(figsize=(10, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Character Frequency Distribution")
    plt.show()

def plot_cumulative_word_count(word_counts):
    cumulative_counts = np.cumsum(word_counts)
    plt.plot(cumulative_counts, label='Cumulative Word Count')
    plt.xlabel("Page Number")
    plt.ylabel("Cumulative Word Count")
    plt.title("Cumulative Word Count Across Pages")
    plt.legend()
    plt.show()

def plot_word_length_histogram(text):
    words = text.split()
    word_lengths = [len(word) for word in words]
    plt.hist(word_lengths, bins=range(1, max(word_lengths) + 1), edgecolor='black')
    plt.xlabel("Word Length")
    plt.ylabel("Frequency")
    plt.title("Histogram of Word Lengths")
    plt.show()

def plot_word_density_heatmap(word_counts):
    word_counts_matrix = np.array(word_counts).reshape((len(word_counts), 1))
    plt.imshow(word_counts_matrix, cmap='hot', interpolation='nearest', aspect='auto')
    plt.colorbar(label='Word Density')
    plt.xlabel("Page")
    plt.ylabel("Word Density")
    plt.title("Heatmap of Word Density per Page")
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

    # Word cloud
    plot_word_cloud(text)

    # Character frequency pie chart
    plot_character_frequency_pie(char_freq)

    # Cumulative word count
    plot_cumulative_word_count(words_per_page_list)

    # Word length histogram
    plot_word_length_histogram(text)

    # Word density heatmap
    plot_word_density_heatmap(words_per_page_list)

    # Top 20 words pie chart
    plot_top_20_words_pie(text)

# Usage
# pdf_file_path = "C:/Users/lucke/Downloads/The-Holy-Bible-King-James-Version.pdf"  # Replace with your PDF file path
pdf_file_path = "C:/Users/lucke/Downloads/quran-english-translation-clearquran-edition-allah.pdf"  # Replace with your PDF file path
analyze_pdf(pdf_file_path)
