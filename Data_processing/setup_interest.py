# -*- coding: utf-8 -*-
"""setup_interest.ipynb

Automatically generated by Colab.
"""
"""setup_interest.ipynb"""

!pip install googletrans==3.1.0a0

import pandas as pd
import re
from googletrans import Translator
import argparse

def process_profiles(input_file_path, translated_file_path, target_lang='es'):
    """
    Cleans and translates the 'interests' column in the input Excel file,
    then saves the cleaned and translated data to new Excel files.

    Parameters:
    input_file_path (str): Path to the input Excel file.
    translated_file_path (str): Path to save the cleaned and translated Excel file.
    target_lang (str): Target language for translation. Default is 'es'.
    """

    # Read the input Excel file
    df = pd.read_excel(input_file_path)

    # Clean brackets from the 'interests' column
    df['interests'] = df['interests'].str.replace(r'[\[\]]', '', regex=True)

    # Translate and format terms
    def translate_and_format_terms(areas):
        translator = Translator()
        try:
            translated_terms = [translator.translate(term, dest=target_lang).text.capitalize() for term in areas.split(r',\s*|\sy\s*|\.\s*| • ')] #', '
            return ', '.join(translated_terms)
        except Exception as e:
            print(f"Error translating '{areas}': {e}")
            return areas

    # Apply the translation and formatting function
    df['interests'] = df['interests'].apply(translate_and_format_terms)

    # Save the translated DataFrame to a new Excel file
    df[['name', 'interests']].to_excel(translated_file_path, index=False)
    print(f'Translated DataFrame saved to {translated_file_path}')

# Comment out the argparse section when running in a Jupyter Notebook

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and translate researcher profiles.")
    parser.add_argument('input_file', type=str, help='Path to the input Excel file.')
    parser.add_argument('cleaned_file', type=str, help='Path to save the cleaned Excel file.')
    parser.add_argument('translated_file', type=str, help='Path to save the translated Excel file.')
    parser.add_argument('--lang', type=str, default='es', help='Target language for translation. Default is "es".')

    args = parser.parse_args()

    process_profiles(args.input_file, args.cleaned_file, args.translated_file, args.lang)
