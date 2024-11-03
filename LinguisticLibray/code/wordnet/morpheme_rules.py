"""
morpheme_rules.py - Rules and patterns for English word formation
"""

# Basic phonological components
VOWELS = {'a', 'e', 'i', 'o', 'u'}
SEMI_VOWELS = {'y', 'w'}
CONSONANTS = {
    'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'
}

# Syllable patterns with examples
SYLLABLE_PATTERNS = {
    'CV': {'pattern': 'CV', 'example': 'go', 'weight': 0.3},
    'CVC': {'pattern': 'CVC', 'example': 'cat', 'weight': 0.3},
    'VC': {'pattern': 'VC', 'example': 'at', 'weight': 0.1},
    'CVCC': {'pattern': 'CVCC', 'example': 'test', 'weight': 0.1},
    'CCVC': {'pattern': 'CCVC', 'example': 'stop', 'weight': 0.1},
    'V': {'pattern': 'V', 'example': 'a', 'weight': 0.1}
}

# Morpheme categories with semantic info
MORPHEME_CATEGORIES = {
    'prefixes': {
        'light': {  # 1 syllable
            'un': {'meaning': 'not', 'attach_to': ['adjective', 'verb']},
            're': {'meaning': 'again', 'attach_to': ['verb']},
            'de': {'meaning': 'reverse/remove', 'attach_to': ['verb']},
            'pre': {'meaning': 'before', 'attach_to': ['noun', 'verb']},
            'in': {'meaning': 'not/in', 'attach_to': ['adjective', 'verb']},
            'dis': {'meaning': 'not/apart', 'attach_to': ['verb']},
            'en': {'meaning': 'make/in', 'attach_to': ['verb']},
            'ex': {'meaning': 'out/former', 'attach_to': ['noun']}
        },
        'heavy': {  # 2 syllables
            'counter': {'meaning': 'against', 'attach_to': ['noun', 'verb']},
            'inter': {'meaning': 'between', 'attach_to': ['noun', 'verb']},
            'super': {'meaning': 'above', 'attach_to': ['adjective', 'noun']},
            'hyper': {'meaning': 'excessive', 'attach_to': ['adjective']},
            'proto': {'meaning': 'first', 'attach_to': ['noun']},
            'pseudo': {'meaning': 'false', 'attach_to': ['noun', 'adjective']},
            'meta': {'meaning': 'beyond', 'attach_to': ['noun']}
        }
    },
    'roots': {
        'light': {  # 1 syllable
            'port': {'meaning': 'carry', 'category': 'action'},
            'act': {'meaning': 'do', 'category': 'action'},
            'graph': {'meaning': 'write', 'category': 'action'},
            'ject': {'meaning': 'throw', 'category': 'action'},
            'dict': {'meaning': 'say', 'category': 'communication'},
            'spec': {'meaning': 'look', 'category': 'perception'},
            'scrib': {'meaning': 'write', 'category': 'communication'}
        },
        'heavy': {  # 2 syllables
            'decis': {'meaning': 'decide', 'category': 'cognition'},
            'react': {'meaning': 'act again', 'category': 'action'},
            'produc': {'meaning': 'make', 'category': 'action'},
            'conject': {'meaning': 'guess', 'category': 'cognition'}
        }
    },
    'suffixes': {
        'light': {  # 1 syllable
            'ly': {'meaning': 'manner', 'attach_to': ['adjective'], 'creates': 'adverb'},
            'er': {'meaning': 'agent', 'attach_to': ['verb'], 'creates': 'noun'},
            'ful': {'meaning': 'full of', 'attach_to': ['noun'], 'creates': 'adjective'},
            'less': {'meaning': 'without', 'attach_to': ['noun'], 'creates': 'adjective'},
            'ness': {'meaning': 'state', 'attach_to': ['adjective'], 'creates': 'noun'},
            'ing': {'meaning': 'action', 'attach_to': ['verb'], 'creates': 'verb'},
            'ed': {'meaning': 'past', 'attach_to': ['verb'], 'creates': 'verb'},
            's': {'meaning': 'plural', 'attach_to': ['noun'], 'creates': 'noun'}
        },
        'heavy': {  # 2 syllables
            'ation': {'meaning': 'process', 'attach_to': ['verb'], 'creates': 'noun'},
            'ology': {'meaning': 'study of', 'attach_to': ['noun'], 'creates': 'noun'},
            'ific': {'meaning': 'making', 'attach_to': ['noun'], 'creates': 'verb'},
            'ative': {'meaning': 'tendency', 'attach_to': ['verb'], 'creates': 'adjective'},
            'able': {'meaning': 'capable', 'attach_to': ['verb'], 'creates': 'adjective'},
            'ible': {'meaning': 'capable', 'attach_to': ['verb'], 'creates': 'adjective'},
            'ity': {'meaning': 'state', 'attach_to': ['adjective'], 'creates': 'noun'}
        }
    }
}

# Themed morpheme groups
THEMED_MORPHEMES = {
    'academic': {
        'prefixes': ['meta', 'pseudo', 'proto'],
        'roots': ['graph', 'spec', 'log'],
        'suffixes': ['ology', 'osis', 'istic']
    },
    'movement': {
        'prefixes': ['trans', 'pro', 'retro'],
        'roots': ['port', 'ject', 'duc'],
        'suffixes': ['ion', 'ive', 'ant']
    },
    'quality': {
        'prefixes': ['un', 'in', 'dis'],
        'roots': ['form', 'color', 'size'],
        'suffixes': ['ful', 'less', 'ous']
    }
}

# Syllable formation patterns by word length
SYLLABLE_PATTERNS_BY_LENGTH = {
    1: [
        {'pattern': 'CVC', 'weight': 0.5},
        {'pattern': 'CVCC', 'weight': 0.3},
        {'pattern': 'CCVC', 'weight': 0.2}
    ],
    2: [
        {'components': ['prefix', 'root'], 'weight': 0.4},
        {'components': ['root', 'suffix'], 'weight': 0.4},
        {'components': ['light_root', 'light_root'], 'weight': 0.2}
    ],
    3: [
        {'components': ['prefix', 'root', 'suffix'], 'weight': 0.5},
        {'components': ['root', 'suffix', 'suffix'], 'weight': 0.3},
        {'components': ['light_prefix', 'heavy_root'], 'weight': 0.2}
    ],
    4: [
        {'components': ['prefix', 'root', 'heavy_suffix'], 'weight': 0.4},
        {'components': ['prefix', 'prefix', 'root', 'suffix'], 'weight': 0.3},
        {'components': ['prefix', 'root', 'suffix', 'suffix'], 'weight': 0.3}
    ]
}

# Phonological rules
class PhonologicalRules:
    @staticmethod
    def has_triple_vowels(word: str) -> bool:
        """Check if word has three consecutive vowels."""
        vowel_count = 0
        for char in word.lower():
            if char in VOWELS:
                vowel_count += 1
                if vowel_count >= 3:
                    return True
            else:
                vowel_count = 0
        return False

    @staticmethod
    def has_triple_consonants(word: str) -> bool:
        """Check if word has three consecutive consonants."""
        consonant_count = 0
        for char in word.lower():
            if char in CONSONANTS:
                consonant_count += 1
                if consonant_count >= 3:
                    return True
            else:
                consonant_count = 0
        return False

    @staticmethod
    def should_drop_final_e(root: str, suffix: str) -> bool:
        """Check if final 'e' should be dropped before adding suffix."""
        return (root.endswith('e') and 
                (suffix.startswith('i') or suffix.startswith('a')))

    @staticmethod
    def should_double_consonant(root: str, suffix: str) -> bool:
        """Check if final consonant should be doubled before adding suffix."""
        if not root or not suffix:
            return False
        # Single syllable words ending in CVC
        if (len(root) >= 3 and
            root[-1] in CONSONANTS and
            root[-2] in VOWELS and
            root[-3] in CONSONANTS):
            return True
        return False

class MorphemePatterns:
    @staticmethod
    def get_pattern_for_syllables(count: int) -> dict:
        """Get valid morpheme patterns for desired syllable count."""
        return SYLLABLE_PATTERNS_BY_LENGTH.get(count, [])

    @staticmethod
    def is_valid_combination(prefix: str, root: str, suffix: str) -> bool:
        """Check if morpheme combination follows phonological rules."""
        word = prefix + root + suffix
        rules = PhonologicalRules()
        
        if rules.has_triple_vowels(word):
            return False
        if rules.has_triple_consonants(word):
            return False
            
        return True

    @staticmethod
    def apply_phonological_rules(prefix: str, root: str, suffix: str) -> tuple:
        """Apply phonological rules to morpheme combination."""
        rules = PhonologicalRules()
        
        # Handle final 'e' dropping
        if rules.should_drop_final_e(root, suffix):
            root = root[:-1]
            
        # Handle consonant doubling
        if rules.should_double_consonant(root, suffix):
            root = root + root[-1]
            
        return prefix, root, suffix
