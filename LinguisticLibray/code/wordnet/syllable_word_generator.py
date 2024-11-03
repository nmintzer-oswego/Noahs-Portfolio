#!/usr/bin/env python3
"""
syllable_word_generator.py - Generate a word with specified syllable count
Usage: python syllable_word_generator.py <syllable_count>
Example: python syllable_word_generator.py 2
"""

from nltk.tokenize import SyllableTokenizer
from nltk import download
import random
import json
import os
import re
import sys


class SyllableWordGenerator:
    def __init__(self):
        try:
            self.syllable_tokenizer = SyllableTokenizer()
        except LookupError:
            download('punkt')
            self.syllable_tokenizer = SyllableTokenizer()

        # Load morphemes from enhanced dataset
        data_directory = "../../data/"
        morphemes_enhanced_path = os.path.join(data_directory, 'morphemes_enhanced.json')

        with open(morphemes_enhanced_path, 'r', encoding='utf-8') as file:
            self.morphemes = json.load(file)

        # Process morphemes into categories
        self.prefixes = {'light': {}, 'heavy': {}}
        self.roots = {'light': {}, 'heavy': {}}
        self.suffixes = {'light': {}, 'heavy': {}}

        for key, value in self.morphemes.items():
            if not isinstance(value, dict) or 'forms' not in value or not value['forms']:
                continue

            form = value['forms'][0]
            loc = form.get('loc', '')

            # Clean the form and get syllable count
            clean_form = self._clean_morpheme(form.get('form', ''))
            if not clean_form:
                continue

            # Get syllable information from the enhanced dataset
            syllables_info = value.get('syllables', {})
            syllable_count = syllables_info.get('count', 1)
            syllable_components = syllables_info.get('components', [])

            weight = 'heavy' if syllable_count > 1 else 'light'

            value_with_clean_form = dict(value)
            value_with_clean_form['forms'][0]['form'] = clean_form
            value_with_clean_form['syllable_components'] = syllable_components

            if loc == 'prefix':
                self.prefixes[weight][clean_form] = dict(value_with_clean_form, syllables=syllable_count)
            elif loc == 'embedded':  # root
                self.roots[weight][clean_form] = dict(value_with_clean_form, syllables=syllable_count)
            elif loc == 'suffix':
                self.suffixes[weight][clean_form] = dict(value_with_clean_form, syllables=syllable_count)

    def _clean_morpheme(self, morpheme: str) -> str:
        """Clean a morpheme by removing hyphens and special characters."""
        return re.sub(r'[^a-zA-Z]', '', morpheme).strip()

    def _get_syllable_components(self, morpheme_info):
        """Get syllable components from morpheme info."""
        if 'syllable_components' in morpheme_info:
            return [comp['syllable'] for comp in morpheme_info['syllable_components']]
        return [morpheme_info['forms'][0]['form']]

    def _combine_morphemes(self, prefix: str, root: str, suffix: str) -> str:
        """Combine morphemes with proper handling of connecting vowels/consonants."""
        word = ""
        if prefix:
            word += prefix
            if root and not any(prefix.endswith(v) for v in 'aeiou'):
                word += 'o'
        if root:
            word += root
        if suffix:
            if root and root.endswith(suffix[0]):
                word = word[:-1]
            word += suffix
        return word

    def generate_word(self, syllable_count: int) -> dict:
        """Generate a single word with the specified syllable count."""
        if syllable_count < 1 or syllable_count > 4:
            raise ValueError("Syllable count must be between 1 and 4")

        # For 1-syllable words, just use a root
        if syllable_count == 1:
            root, root_info = random.choice(list(self.roots['light'].items()))
            return {
                'word': root,
                'syllable_breakdown': self._get_syllable_components(root_info),
                'components': {
                    'root': {'form': root, 'meaning': root_info.get('meaning', [])}
                }
            }

        # For multi-syllable words
        components = {'prefix': None, 'root': None, 'suffix': None}
        syllable_parts = []
        remaining = syllable_count

        # Try to add prefix
        if syllable_count >= 2 and random.random() > 0.3:
            prefix_weight = 'heavy' if remaining >= 2 else 'light'
            if self.prefixes[prefix_weight]:
                prefix, prefix_info = random.choice(list(self.prefixes[prefix_weight].items()))
                prefix_syllables = prefix_info.get('syllables', 1)
                if prefix_syllables <= remaining:
                    components['prefix'] = {'form': prefix, 'meaning': prefix_info.get('meaning', [])}
                    syllable_parts.extend(self._get_syllable_components(prefix_info))
                    remaining -= prefix_syllables

        # Add root if needed
        if remaining > 0:
            root_weight = 'heavy' if remaining >= 2 else 'light'
            if self.roots[root_weight]:
                root, root_info = random.choice(list(self.roots[root_weight].items()))
                root_syllables = root_info.get('syllables', 1)
                if root_syllables <= remaining:
                    components['root'] = {'form': root, 'meaning': root_info.get('meaning', [])}
                    syllable_parts.extend(self._get_syllable_components(root_info))
                    remaining -= root_syllables

        # Add suffix if needed
        if remaining > 0:
            suffix_weight = 'heavy' if remaining >= 2 else 'light'
            if self.suffixes[suffix_weight]:
                suffix, suffix_info = random.choice(list(self.suffixes[suffix_weight].items()))
                if suffix_info.get('syllables', 1) == remaining:
                    components['suffix'] = {'form': suffix, 'meaning': suffix_info.get('meaning', [])}
                    syllable_parts.extend(self._get_syllable_components(suffix_info))

        # Combine morphemes
        word = self._combine_morphemes(
            components['prefix']['form'] if components['prefix'] else "",
            components['root']['form'] if components['root'] else "",
            components['suffix']['form'] if components['suffix'] else ""
        )

        if not word:
            return self.generate_word(syllable_count)  # Try again if combination failed

        return {
            'word': word,
            'syllable_breakdown': syllable_parts,
            'components': components
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python syllable_word_generator.py <syllable_count>")
        print("Example: python syllable_word_generator.py 2")
        sys.exit(1)

    try:
        syllable_count = int(sys.argv[1])
        if syllable_count < 1 or syllable_count > 4:
            raise ValueError("Syllable count must be between 1 and 4")
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    try:
        generator = SyllableWordGenerator()
        result = generator.generate_word(syllable_count)

        # Print word and its breakdown
        print(result['word'])
        print(f"Syllable breakdown: {' + '.join(result['syllable_breakdown'])}")

        # Print components with meanings
        if result['components']['prefix']:
            print(
                f"prefix: {result['components']['prefix']['form']} ({', '.join(result['components']['prefix']['meaning'])})")
        if result['components']['root']:
            print(
                f"root: {result['components']['root']['form']} ({', '.join(result['components']['root']['meaning'])})")
        if result['components']['suffix']:
            print(
                f"suffix: {result['components']['suffix']['form']} ({', '.join(result['components']['suffix']['meaning'])})")

    except FileNotFoundError:
        print("Error: Could not find morphemes_enhanced.json in ../../data/")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()