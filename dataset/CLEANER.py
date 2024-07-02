import re


def double_space_to_single(text_in:str) -> str:
    text_out = text_in.replace("  ", " ").replace("\t", " ")
    return text_out

def clean_unicode_chars(text):
    """ Remove or replace unicode characters for proper AI training."""
    # Map of common Unicode characters to their ASCII equivalents
    unicode_replacements = {
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

    # Replace Unicode characters with ASCII ones
    for unicode_char, ascii_char in unicode_replacements.items():
        text = text.replace(unicode_char, ascii_char)

    # Remove any other remaining non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    return text


def clean_quotes(text):
    """Replace or remove quotes appropriately for AI training."""
    # Replace smart quotes with standard quotes
    text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

    # Handling standalone quotes at the beginning or end of sentences
    text = re.sub(r'(^\s*"\s*)|(\s*"\s*$)', '', text)

    # Handling quotes used incorrectly or around URLs and metadata
    text = re.sub(r'"\s*,', ',', text)  # Remove quote before comma
    text = re.sub(r'\s*"\s*', ' ', text)  # Replace quotes with space

    # Ensure URL/metadata integrity while removing quotes around them
    text = re.sub(r'http\s*:\s*//', 'http://', text, flags=re.IGNORECASE)

    return text.strip()

def clean_sentence(sentence):
    # Remove unnecessary characters and normalize spaces
    sentence = re.sub(r'\s+', ' ', sentence)  # Replace multiple spaces with a single space
    sentence = re.sub(r'\s*\(\s*', '(', sentence)  # Normalize spaces around parentheses
    sentence = re.sub(r'\s*\)\s*', ') ', sentence)
    sentence = re.sub(r'\s*:\s*', ': ', sentence)
    sentence = re.sub(r' +', ' ', sentence)  # Remove multiple spaces
    sentence = sentence.strip()  # Remove leading and trailing spaces

    # Fix common misspellings and formatting issues
    sentence = re.sub(r'\bModdel\b', 'Model', sentence)
    sentence = re.sub(r'\bColorad\b', 'Colorado', sentence)
    sentence = re.sub(r'\bcorporat\b', 'corporate', sentence)
    sentence = re.sub(r'\bDenve\b', 'Denver', sentence)
    sentence = re.sub(r'\bGarret Modde\b', 'Garrett Model', sentence)
    sentence = re.sub(r'\bBoulde\b', 'Boulder', sentence)
    sentence = re.sub(r'\bdisclaime\b', 'disclaimer', sentence)
    sentence = re.sub(r'\bFiled on\b', 'filed on', sentence)
    sentence = re.sub(r'\bPhotovoltaic Devic\b', 'Photovoltaic Device', sentence)
    sentence = re.sub(r'\bPatent\b', 'Patent.', sentence)
    sentence = re.sub(r'\bPhotovoltaic Devic\b', 'Photovoltaic Device', sentence)
    sentence = re.sub(r'\bApplic\b', 'Applicant', sentence)
    sentence = re.sub(r'\binventor\b', 'Inventor', sentence)
    sentence = re.sub(r'\bAssignee\b', 'Assignee:', sentence)
    sentence = re.sub(r'\bfield\b', 'Field', sentence)
    sentence = re.sub(r'\bapplication\b', 'Application', sentence)
    sentence = re.sub(r'\bsearch\b', 'Search', sentence)
    sentence = re.sub(r'\bpublication\b', 'Publication', sentence)
    sentence = re.sub(r'\bAttorney\b', 'Attorney', sentence)
    sentence = re.sub(r'\bAgent\b', 'Agent', sentence)
    sentence = re.sub(r'\bPrimary Examiner\b', 'Primary Examiner:', sentence)
    sentence = re.sub(r'\bFig\b', 'Figure', sentence)
    sentence = re.sub(r'\bLe\b', 'le', sentence)
    sentence = re.sub(r'\be\b', 'e', sentence)
    sentence = re.sub(r'\bo\b', 'o', sentence)
    sentence = re.sub(r'\ba\b', 'a', sentence)
    sentence = re.sub(r'\bnew\b', 'new', sentence)
    sentence = re.sub(r'\bfollow\b', 'follow', sentence)
    sentence = re.sub(r'\bdate\b', 'Date', sentence)
    sentence = re.sub(r'\btitle\b', 'Title', sentence)
    sentence = re.sub(r'\bNumber\b', 'Number', sentence)
    sentence = re.sub(r'\bApp\b', 'Application', sentence)
    sentence = re.sub(r'\bFiled\b', 'filed', sentence)
    sentence = re.sub(r'\bDated\b', 'dated', sentence)
    sentence = re.sub(r'\bdated\b', 'dated', sentence)
    sentence = re.sub(r'\bTherm\b', 'therm', sentence)
    sentence = re.sub(r'\bZero\b', 'zero', sentence)
    sentence = re.sub(r'\bLambe\b', 'lambe', sentence)
    sentence = re.sub(r'\bLebedev\b', 'lebedev', sentence)
    sentence = re.sub(r'\bHaisch\b', 'haisch', sentence)
    sentence = re.sub(r'\bL\b', 'le', sentence)
    sentence = re.sub(r'\bLambe\b', 'lambe', sentence)
    sentence = re.sub(r'\bGarret Modde\b', 'Garrett Moddel', sentence)

    return sentence
def clean_training_data(sentences):
    cleaned_sentences = [clean_sentence(sentence) for sentence in sentences]
    return cleaned_sentences


def clean_text(text):
    one = double_space_to_single(text)
    two = clean_unicode_chars(one)
    three = clean_quotes(two)
    four = clean_sentence(three)
    return four
