import re


class TextCleaner:
    def __init__(self):
        self.unicode_replacements = {
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            '\u2013': '-',  # En dash
            '\u2014': '-',  # Em dash
            '\u2026': '...',  # Ellipsis
            '\u00e9': 'e',  # é to e
            # Add more replacements as needed
        }
        self.title_pattern = re.compile(r'\b(' + '|'.join([
            'Mr\.', 'Mrs\.', 'Miss\.', 'Ms\.', 'Dr\.', 'Prof\.', 'Capt\.', 'Col\.', 'Gen\.', 'Lt\.', 'Maj\.', 'Sgt\.',
            'Adm\.', 'Cpl\.', 'Rev\.', 'Sen\.', 'Rep\.', 'Gov\.', 'Pres\.', 'Rt\.', 'Hon\.', 'Cmdr\.', 'Amb\.', 'Sec\.',
            'Dir\.',  # Add any additional titles as necessary
        ]) + r')\b')

    def double_space_to_single_cleaner(self, text: str) -> str:
        """Replace double spaces with single space and tab with space."""
        return text.replace("  ", " ").replace("\t", " ")

    def unicode_cleaner(self, text: str) -> str:
        """Remove or replace unicode characters for proper AI training."""
        for unicode_char, ascii_char in self.unicode_replacements.items():
            text = text.replace(unicode_char, ascii_char)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text

    def quote_cleaner(self, text: str) -> str:
        """Replace or remove quotes appropriately for AI training."""
        text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
        text = re.sub(r'(^\s*"\s*)|(\s*"\s*$)', '', text)
        text = re.sub(r'"\s*,', ',', text)
        text = re.sub(r'\s*"\s*', ' ', text)
        text = re.sub(r'http\s*:\s*//', 'http://', text, flags=re.IGNORECASE)
        return text.strip()

    def remove_period_from_titles(self, text):
        """Remove the period from common titles in the text."""

        # Create a regex pattern to match any of the titles with a period
        title_pattern = re.compile(r'\b(' + '|'.join([re.escape(title) for title in self.title_pattern]) + r')\b')

        # Replace periods from the titles
        def replace_period(match):
            return match.group(0).replace('.', '')

        return title_pattern.sub(replace_period, text)

    def sentence_cleaner(self, sentence: str) -> str:
        """Clean up a sentence by normalizing spaces and fixing common misspellings."""
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.sub(r'\s*\(\s*', '(', sentence)
        sentence = re.sub(r'\s*\)\s*', ') ', sentence)
        sentence = re.sub(r'\s*:\s*', ': ', sentence)
        sentence = re.sub(r' +', ' ', sentence)
        sentence = sentence.strip()

        common_replacements = {
            r'\bModdel\b': 'Model',
            r'\bColorad\b': 'Colorado',
            # Add more replacements as needed
        }
        for pattern, replacement in common_replacements.items():
            sentence = re.sub(pattern, replacement, sentence)

        return sentence

    def pipeline_basic_cleaning(self, text: str) -> str:
        """Run a basic cleaning pipeline on the text."""
        text = self.remove_period_from_titles(text)
        text = self.double_space_to_single_cleaner(text)
        text = self.unicode_cleaner(text)
        text = self.quote_cleaner(text)
        return text

    def pipeline_full_cleaning(self, text: str) -> str:
        """Run a full cleaning pipeline on the text."""
        text = self.pipeline_basic_cleaning(text)

        text = self.sentence_cleaner(text)
        return text

    def clean_training_data(self, sentences: list) -> list:
        """Clean a list of sentences for AI training."""
        return [self.sentence_cleaner(sentence) for sentence in sentences]


