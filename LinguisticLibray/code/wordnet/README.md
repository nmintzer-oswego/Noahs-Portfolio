# English Word Morpheme Analysis Tools

A collection of Python tools for morpheme analysis, syllable processing, and word generation with a focus on English language morphology. This project provides utilities for syllable analysis, morpheme rule processing, and word generation based on morphological patterns.

## Core Components

### 1. Morpheme Rules System (`morpheme_rules.py`)
Defines the fundamental rules and patterns for English word formation.

#### Key Features:
- Phonological component definitions
- Syllable pattern templates
- Morpheme categorization rules

```python
# Phonological Components
VOWELS = {'a', 'e', 'i', 'o', 'u'}
SEMI_VOWELS = {'y', 'w'}
CONSONANTS = {'b', 'c', 'd', 'f', 'g', ...}

# Syllable Patterns with Examples
SYLLABLE_PATTERNS = {
    'CV':   {'pattern': 'CV',   'example': 'go',   'weight': 0.3},
    'CVC':  {'pattern': 'CVC',  'example': 'cat',  'weight': 0.3},
    'VC':   {'pattern': 'VC',   'example': 'at',   'weight': 0.1},
    # ... more patterns
}

# Phonological Rule Examples
class PhonologicalRules:
    @staticmethod
    def should_drop_final_e(root: str, suffix: str) -> bool:
        """Check if final 'e' should be dropped before adding suffix."""
        return (root.endswith('e') and 
                (suffix.startswith('i') or suffix.startswith('a')))

    @staticmethod
    def should_double_consonant(root: str, suffix: str) -> bool:
        """Check if final consonant should be doubled before adding suffix."""
```

### 2. Syllable Analysis (`syllable-utils.py`)
Provides tools for analyzing syllable structure in words using NLTK.

#### Key Features:
- Syllable tokenization
- Position tracking
- Morpheme enhancement with syllable data

```python
class MorphemeSyllableAnalyzer:
    def get_syllable_positions(self, word):
        """
        Get syllables and their positions in a word.
        Returns: {
            "count": 2,
            "components": [
                {"syllable": "un", "position": [0, 2]},
                {"syllable": "der", "position": [2, 5]}
            ]
        }
        """

    def enhance_morphemes_file(self, input_file, output_file):
        """Process morphemes and add syllable information."""
```

### 3. Dataset Enhancement (`enhance-morphemes.py`)
Tool for adding syllable analysis data to the morpheme dataset.

#### Key Features:
- NLTK integration for syllable analysis
- Syllable position tracking
- Vowel sequence handling
- Enhanced dataset generation

```python
def process_morphemes():
    """
    Process morphemes and add syllable analysis:
    1. Initialize NLTK tokenizer
    2. Process each morpheme entry
    3. Add syllable information
    4. Generate enhanced dataset
    """

def clean_and_enhance_morpheme(entry, tokenizer):
    """
    Clean and enhance a single morpheme entry with:
    - Syllable count
    - Syllable positions
    - Component analysis
    """
```

### 4. Word Generation (`syllable_word_generator.py`)
Generates words based on syllable patterns and morpheme rules.

#### Key Features:
- Configurable syllable count (1-4 syllables)
- Morpheme-based construction
- Syllable pattern matching
- Detailed word breakdown

```python
class SyllableWordGenerator:
    def generate_word(self, syllable_count: int) -> dict:
        """
        Generate a word with specified syllable count.
        Returns: {
            'word': 'unport',
            'syllable_breakdown': ['un', 'port'],
            'components': {
                'prefix': {'form': 'un', 'meaning': ['not']},
                'root': {'form': 'port', 'meaning': ['carry']}
            }
        }
        """
```

Example usage:
```bash
$ python syllable_word_generator.py 2
unport
Syllable breakdown: un + port
prefix: un (not)
root: port (carry)
```

## Installation

1. Install Python 3.x from https://www.python.org/downloads/

2. Install required packages:
```bash
pip install nltk
```

3. Download required NLTK resources:
```python
import nltk
nltk.download('words')
nltk.download('punkt')
```

## Usage

### Enhancing Morpheme Dataset
```bash
python enhance-morphemes.py
```

### Generating Words
```bash
python syllable_word_generator.py <syllable_count>
```

## Development Notes

### Dependencies
- Python 3.x
- NLTK package
- NLTK resources: words corpus, punkt tokenizer

### CITATION
```
Bird, Steven, Edward Loper and Ewan Klein (2009).
Natural Language Processing with Python.  O'Reilly Media Inc.
```
