


# import libraries
import pandas as pd
from tqdm import tqdm
import time 
import os
from PyPDF2 import PdfReader # for reading the PDF files
import nltk as nltk
import re

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake


# Function to find filepaths

def find_filepaths():
    
    """
    Finds the filepaths for the current directory and the output directory.
    
    Returns:
        A tuple containing the current directory and the output directory filepath.
    """
    
    print("Finding the filepaths...")
    
    current_directory = os.getcwd()
    #current_directory = os.path.dirname(current_directory)
    print("Current directory:", current_directory)
    
    output_fp = os.path.join(current_directory, "Output")
    if os.path.exists(output_fp) == False:
        os.makedirs(output_fp)
        
    # return filepaths
    return current_directory, output_fp
    



def clean_text_re(text):
    """
    Cleans the given text by adding spaces between lowercase and uppercase letters,
    letters and numbers, numbers and letters, punctuation and non-space characters,
    and before and after dashes/hyphens. It also corrects common conjunctions and
    abbreviations. Finally, it normalizes multiple spaces to a single space.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    
    # Add space between lowercase and uppercase letters
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    
    # Add space between letters and numbers
    text = re.sub(r'(?<=\D)(?=\d)', ' ', text)
    
    # Add space between numbers and letters
    text = re.sub(r'(?<=\d)(?=\D)', ' ', text)
    
    # Add space after punctuation if not followed by space
    text = re.sub(r'(?<=[.,;!?])(?=\S)', ' ', text)
    
    # Add space before and after dash/hyphen if not followed by space
    text = re.sub(r'(?<=\S)-(?=\S)', ' - ', text)
    
    # Correct common conjunctions and abbreviations (specific cases)
    text = re.sub(r'\bMEng\b', 'MEng ', text)
    text = re.sub(r'\bSINDy\b', 'SINDy ', text)
    
    # Normalize multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()




def clean_text_nltk(text):
    """
    Cleans the given text using NLTK tools.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.

    """
    # Download NLTK stuff
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")

    # actual algorithm
    sentences = sent_tokenize(text)

    # Initialize NLTK tools
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    cleaned_text = []

    for sentence in sentences:
        # Tokenize words
        words = word_tokenize(sentence)
        # Remove stop words and lemmatize
        words = [lemmatizer.lemmatize(word) for word in words if word.lower() not in stop_words]
        # Reconstruct the sentence
        cleaned_sentence = ' '.join(words)
        cleaned_text.append(cleaned_sentence)

    return ' '.join(cleaned_text)
    
    
    


# Parse Pdf Function

def parse_pdf(current_directory):
    """
    Parses the PDF files in the given directory and returns the extracted text.

    Args:
        current_directory (str): The path to the directory containing the PDF files.

    Returns:
        str: The extracted text from the PDF files.

    Raises:
        Exception: If there is an error reading a PDF file.

    """
    print("Parsing the PDF...")
    
    # get all files in the current directory
    files = os.listdir(current_directory)
    
        
    # Filter files with keyword "CV"
    cv_files = [file for file in files if "CV" in file and file.endswith('.pdf')]

    # Load and parse the PDF files into a large string
    pdf_data = ""
    for file in cv_files:
        file_path = os.path.join(current_directory, file)
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                pdf_data += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading file: {file}. Error message: {e}")

    pdf_data = clean_text_re(pdf_data)
    pdf_data = clean_text_nltk(pdf_data)
    print("PDF files loaded successfully.")
    
    return pdf_data
    


# create a word cloud/keywords 
# extraction function from the string

def extract_keywords(text):
    
    """
    Extracts keywords from the given text using the RAKE algorithm.

    Args:
        text (str): The text from which to extract keywords.

    Returns:
        list: The extracted keywords.

    """
    
    # Initialize the RAKE algorithm
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    # Remove duplicates
    keywords = list(set(keywords))
    print(keywords)
    
    return keywords



#   Main Loading Function

def main_loading_function():
    
    # find the filepaths
    (current_directory,
     output_fp) = find_filepaths()
    
    print("Loading in the data...")
    
    # parse the PDF
    pdf_data = parse_pdf(current_directory)
    raw_keywords = extract_keywords(pdf_data)
    


