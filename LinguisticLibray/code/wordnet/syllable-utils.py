from nltk.tokenize import LegalitySyllableTokenizer
from nltk.corpus import words
import json


class MorphemeSyllableAnalyzer:
    def __init__(self):
        # Initialize the LegalitySyllableTokenizer with English words corpus
        self.tokenizer = LegalitySyllableTokenizer(words.words())

    def get_syllable_positions(self, word):
        """
        Get syllables and their positions in a word
        """
        # Get syllables using the tokenizer
        syllables = self.tokenizer.tokenize(word)

        # Track position in word
        current_pos = 0
        syllable_components = []

        # Calculate position for each syllable
        for syllable in syllables:
            start_pos = current_pos
            end_pos = start_pos + len(syllable)

            syllable_components.append({
                "syllable": syllable,
                "position": [start_pos, end_pos]
            })

            current_pos = end_pos

        return {
            "count": len(syllables),
            "components": syllable_components
        }

    def enhance_morphemes_file(self, input_file, output_file):
        """
        Process morphemes.json and add syllable information
        """
        try:
            # Read existing morphemes
            with open(input_file, 'r', encoding='utf-8') as f:
                morpheme_data = json.load(f)

            # Process each morpheme
            for key, entry in morpheme_data.items():
                if entry["forms"] and len(entry["forms"]) > 0:
                    # Get the form from first forms entry
                    form = entry["forms"][0]["form"]

                    # Add syllable analysis
                    entry["syllables"] = self.get_syllable_positions(form)

            # Write enhanced data
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(morpheme_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error processing morphemes file: {str(e)}")
            return False


# Usage example
def main():
    # Initialize analyzer
    analyzer = MorphemeSyllableAnalyzer()

    # Example single word analysis
    word = "wonderful"
    syllables = analyzer.get_syllable_positions(word)
    print(f"Syllable analysis for '{word}':")
    print(json.dumps(syllables, indent=2))

    # Process full morphemes file
    input_file = "morphemes.json"
    output_file = "morphemes_enhanced.json"

    print(f"\nProcessing morphemes from {input_file}...")
    if analyzer.enhance_morphemes_file(input_file, output_file):
        print(f"Successfully created enhanced morphemes file: {output_file}")
    else:
        print("Failed to process morphemes file")


if __name__ == "__main__":
    main()