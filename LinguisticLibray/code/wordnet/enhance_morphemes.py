#!/usr/bin/env python3

from nltk.tokenize import LegalitySyllableTokenizer
from nltk.corpus import words
from nltk import download
import json
import sys
import os
import morphemes_lib as morphemes

# Get the data directory path from morphemes_lib
DATA_DIRECTORY = morphemes.data_directory_path


def ensure_nltk_resources():
    """Ensure required NLTK resources are available"""
    try:
        words.words()
    except LookupError:
        print("Downloading required NLTK resources...")
        download('words')


def combine_vowel_syllables(syllables, positions):
    """Combine adjacent syllables that shouldn't be split"""
    if len(syllables) <= 1:
        return syllables, positions

    new_syllables = []
    new_positions = []
    i = 0

    while i < len(syllables):
        if (len(syllables[i]) == 1 and
                syllables[i].lower() in 'aeiou' and
                i < len(syllables) - 1):
            combined = syllables[i] + syllables[i + 1]
            new_syllables.append(combined)
            new_positions.append([
                positions[i][0],
                positions[i + 1][1]
            ])
            i += 2
        else:
            new_syllables.append(syllables[i])
            new_positions.append(positions[i])
            i += 1

    return new_syllables, new_positions


def clean_and_enhance_morpheme(entry, tokenizer):
    """Clean and enhance a single morpheme entry"""
    # Create new entry with selected fields
    cleaned_entry = {
        "forms": entry["forms"],
        "meaning": entry["meaning"],
        "origin": entry["origin"]
    }

    # Process syllables if there are forms
    if cleaned_entry["forms"] and len(cleaned_entry["forms"]) > 0:
        form = cleaned_entry["forms"][0]["form"]

        # Get initial syllables
        syllables = tokenizer.tokenize(form)

        # Calculate initial positions
        current_pos = 0
        positions = []
        for syllable in syllables:
            start_pos = current_pos
            end_pos = start_pos + len(syllable)
            positions.append([start_pos, end_pos])
            current_pos = end_pos

        # Combine syllables where needed
        syllables, positions = combine_vowel_syllables(syllables, positions)

        # Create components list
        syllable_components = [
            {
                "syllable": syl,
                "position": pos
            }
            for syl, pos in zip(syllables, positions)
        ]

        # Add syllable information
        cleaned_entry["syllables"] = {
            "count": len(syllables),
            "components": syllable_components
        }

    return cleaned_entry


def process_morphemes():
    """Process morphemes from morphemes_lib, clean and add syllable analysis"""
    try:
        # Initialize tokenizer
        tokenizer = LegalitySyllableTokenizer(words.words())

        # Get morphemes from the imported library
        morpheme_data = morphemes.morphemes

        # Track statistics
        total_entries = len(morpheme_data)
        processed_entries = 0

        # Create new dictionary for cleaned and enhanced entries
        enhanced_data = {}

        # Process each morpheme
        for key, entry in morpheme_data.items():
            try:
                # Clean and enhance the entry
                enhanced_data[key] = clean_and_enhance_morpheme(entry, tokenizer)
                processed_entries += 1

                # Show progress every 100 entries
                if processed_entries % 100 == 0:
                    print(f"Processed {processed_entries}/{total_entries} entries...")

            except Exception as e:
                print(f"Warning: Could not process entry '{key}': {str(e)}")

        # Prepare output file path in data directory
        output_filename = "morphemes_enhanced.json"
        output_filepath = os.path.join(DATA_DIRECTORY, output_filename)

        # Ensure data directory exists
        os.makedirs(DATA_DIRECTORY, exist_ok=True)

        # Write enhanced data
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2)

        return processed_entries, total_entries, enhanced_data, output_filepath

    except Exception as e:
        print(f"Error processing morphemes: {str(e)}")
        return 0, 0, None, None


def main():
    print("Syllable Analysis Enhancement Tool for Morphemes")
    print("==============================================")

    # Ensure NLTK resources
    ensure_nltk_resources()

    print("\nProcessing morphemes from morphemes_lib...")
    processed, total, enhanced_data, output_filepath = process_morphemes()

    if processed > 0:
        print(f"\nSuccess! Processed {processed}/{total} entries")
        print(f"Enhanced morphemes file created: {output_filepath}")

        # Show example entry
        if enhanced_data:
            first_key = next(iter(enhanced_data))
            print("\nExample enhanced entry:")
            print(json.dumps({first_key: enhanced_data[first_key]}, indent=2))

            if "Euro" in enhanced_data:
                print("\nEuro entry:")
                print(json.dumps({"Euro": enhanced_data["Euro"]}, indent=2))
    else:
        print("\nFailed to process morphemes")
        sys.exit(1)


if __name__ == "__main__":
    main()