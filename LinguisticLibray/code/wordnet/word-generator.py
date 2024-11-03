import random
import json
import os
from typing import List, Dict, Optional
import morphemes_lib as morphemes  # Import the morphemes_lib to get the data directory path


class WordGenerator:
    def __init__(self, morphemes_file: str = "morphemes_enhanced.json"):
        """Initialize the word generator with a morphemes database."""
        # Use the data directory path from morphemes_lib
        morphemes_filepath = os.path.join(morphemes.data_directory_path, morphemes_file)

        try:
            with open(morphemes_filepath, 'r') as f:
                self.morphemes = json.loads(f.read())
        except FileNotFoundError:
            # If enhanced file doesn't exist, try to create it
            print("Enhanced morphemes file not found. Attempting to create it...")
            from enhance_morphemes import process_morphemes
            process_morphemes()
            # Now try to load the newly created file
            with open(morphemes_filepath, 'r') as f:
                self.morphemes = json.loads(f.read())
            self.morphemes = json.loads(f.read())

        # Separate morphemes by location
        self.prefixes = []
        self.roots = []
        self.suffixes = []

        for key, entry in self.morphemes.items():
            for form in entry["forms"]:
                if form["loc"] == "prefix":
                    self.prefixes.append({
                        "form": form["form"],
                        "meaning": entry["meaning"],
                        "category": form.get("category", ""),
                        "attach_to": form.get("attach_to", [])
                    })
                elif form["loc"] == "embedded":
                    self.roots.append({
                        "form": form["form"],
                        "meaning": entry["meaning"]
                    })
                elif form["loc"] == "suffix":
                    self.suffixes.append({
                        "form": form["form"],
                        "meaning": entry["meaning"]
                    })

    def is_valid_combination(self, prefix: str, root: str, suffix: str) -> bool:
        """Check if the morpheme combination follows phonetic and syllabic rules."""
        vowels = set('aeiou')

        # Check if there's at least one vowel in the combination
        combined = prefix + root + suffix
        if not any(c in vowels for c in combined.lower()):
            return False

        # Get syllable counts for each component
        def get_syllable_count(form: str) -> int:
            for morph in self.morphemes.values():
                if any(f["form"] == form for f in morph["forms"]):
                    return morph.get("syllables", {}).get("count", 1)
            return 1  # Default to 1 if not found

        prefix_syllables = get_syllable_count(prefix) if prefix else 0
        root_syllables = get_syllable_count(root) if root else 0
        suffix_syllables = get_syllable_count(suffix) if suffix else 0

        total_syllables = prefix_syllables + root_syllables + suffix_syllables

        # Most English words have between 1 and 4 syllables
        if total_syllables > 4 or total_syllables < 1:
            return False

        # Avoid triple consonants at morpheme boundaries
        def is_consonant(c: str) -> bool:
            return c.lower() not in vowels and c.isalpha()

        if prefix and root:
            if (is_consonant(prefix[-1]) and
                    is_consonant(root[0]) and
                    (len(root) > 1 and is_consonant(root[1]))):
                return False

        if root and suffix:
            if (len(root) > 1 and is_consonant(root[-2]) and
                    is_consonant(root[-1]) and
                    is_consonant(suffix[0])):
                return False

        return True

    def generate_word(self,
                      include_prefix: bool = True,
                      include_root: bool = True,
                      include_suffix: bool = True,
                      max_attempts: int = 50,
                      max_syllables: int = 3) -> Dict:
        """Generate a new word by combining morphemes."""
        for _ in range(max_attempts):
            # Randomly select morphemes
            prefix = random.choice(self.prefixes) if include_prefix else {"form": "", "meaning": []}
            root = random.choice(self.roots) if include_root else {"form": "", "meaning": []}
            suffix = random.choice(self.suffixes) if include_suffix else {"form": "", "meaning": []}

            # Check if the combination is valid
            if self.is_valid_combination(prefix["form"], root["form"], suffix["form"]):
                word = prefix["form"] + root["form"] + suffix["form"]
                # Get syllable information
                syllable_info = self.get_combined_syllables(prefix["form"], root["form"], suffix["form"])

                return {
                    "word": word,
                    "segments": f"{prefix['form']}+{root['form']}+{suffix['form']}" if include_root else f"{prefix['form']}+{suffix['form']}",
                    "syllables": syllable_info,
                    "prefix": {
                        "form": prefix["form"],
                        "meaning": prefix["meaning"]
                    } if include_prefix else None,
                    "root": {
                        "form": root["form"],
                        "meaning": root["meaning"]
                    } if include_root else None,
                    "suffix": {
                        "form": suffix["form"],
                        "meaning": suffix["meaning"]
                    } if include_suffix else None
                }

        raise ValueError("Could not generate a valid word within the maximum attempts")

    def generate_multiple(self, count: int = 5) -> List[Dict]:
        """Generate multiple words."""
        words = []
        for _ in range(count):
            try:
                word = self.generate_word()
                words.append(word)
            except ValueError:
                continue
        return words

    def get_combined_syllables(self, prefix: str, root: str, suffix: str) -> Dict:
        """Get syllable information for the combined word."""

        def get_syllable_info(form: str) -> Dict:
            for morph in self.morphemes.values():
                if any(f["form"] == form for f in morph["forms"]):
                    return morph.get("syllables",
                                     {"count": 1, "components": [{"syllable": form, "position": [0, len(form)]}]})
            return {"count": 1, "components": [{"syllable": form, "position": [0, len(form)]}]}

        # Get syllable info for each component
        prefix_info = get_syllable_info(prefix) if prefix else {"count": 0, "components": []}
        root_info = get_syllable_info(root) if root else {"count": 0, "components": []}
        suffix_info = get_syllable_info(suffix) if suffix else {"count": 0, "components": []}

        # Combine syllable counts
        total_count = prefix_info["count"] + root_info["count"] + suffix_info["count"]

        # Adjust positions for combined word
        components = []
        current_pos = 0

        # Add prefix syllables
        for comp in prefix_info["components"]:
            length = comp["position"][1] - comp["position"][0]
            components.append({
                "syllable": comp["syllable"],
                "position": [current_pos, current_pos + length]
            })
            current_pos += length

        # Add root syllables
        for comp in root_info["components"]:
            length = comp["position"][1] - comp["position"][0]
            components.append({
                "syllable": comp["syllable"],
                "position": [current_pos, current_pos + length]
            })
            current_pos += length

        # Add suffix syllables
        for comp in suffix_info["components"]:
            length = comp["position"][1] - comp["position"][0]
            components.append({
                "syllable": comp["syllable"],
                "position": [current_pos, current_pos + length]
            })
            current_pos += length

        return {
            "count": total_count,
            "components": components
        }

    def get_morphemes_by_meaning_theme(self, theme: str) -> Dict[str, List]:
        """Get morphemes related to a theme based on their meaning."""
        theme_words = {
            "society": ["society", "social", "people", "community", "group", "gather", "meet", "lead", "rule",
                        "govern"],
            "color": ["color", "red", "blue", "green", "yellow", "black", "white", "bright", "dark", "light", "shade"],
            "movement": ["move", "go", "come", "walk", "run", "flow", "turn", "spin", "rise", "fall"],
            "human_body": ["body", "head", "arm", "leg", "heart", "blood", "bone", "muscle", "brain", "eye", "hand",
                           "foot"],
            "mind": ["think", "know", "learn", "mind", "brain", "memory", "idea", "thought", "reason", "logic"],
            "time": ["time", "year", "day", "hour", "before", "after", "early", "late", "now", "then"]
        }

        if theme not in theme_words:
            return {"prefixes": [], "roots": []}

        themed_prefixes = []
        themed_roots = []

        # Find morphemes whose meanings overlap with theme words
        theme_set = set(theme_words[theme])

        for prefix in self.prefixes:
            prefix_meanings = set(" ".join(prefix["meaning"]).lower().split())
            if prefix_meanings & theme_set:
                themed_prefixes.append(prefix)

        for root in self.roots:
            root_meanings = set(" ".join(root["meaning"]).lower().split())
            if root_meanings & theme_set:
                themed_roots.append(root)

        return {
            "prefixes": themed_prefixes,
            "roots": themed_roots
        }

    def generate_themed_word(self, theme: str) -> Optional[Dict]:
        """Generate a word using morphemes related to a specific theme."""
        # Get themed morphemes based on meaning
        themed_morphemes = self.get_morphemes_by_meaning_theme(theme)

        if not themed_morphemes["prefixes"] and not themed_morphemes["roots"]:
            print(f"No morphemes found for theme: {theme}")
            return None

        # Try to generate a themed word
        for _ in range(50):
            try:
                # Use either a themed prefix or root (or both if available)
                if themed_morphemes["prefixes"] and themed_morphemes["roots"] and random.random() < 0.5:
                    prefix = random.choice(themed_morphemes["prefixes"])
                    root = random.choice(themed_morphemes["roots"])
                elif themed_morphemes["prefixes"]:
                    prefix = random.choice(themed_morphemes["prefixes"])
                    root = random.choice(self.roots)
                else:
                    prefix = random.choice(self.prefixes)
                    root = random.choice(themed_morphemes["roots"])

                suffix = random.choice(self.suffixes)  # Allow any suffix

                if self.is_valid_combination(prefix["form"], root["form"], suffix["form"]):
                    word = prefix["form"] + root["form"] + suffix["form"]
                    syllable_info = self.get_combined_syllables(prefix["form"], root["form"], suffix["form"])

                    return {
                        "word": word,
                        "segments": f"{prefix['form']}+{root['form']}+{suffix['form']}",
                        "syllables": syllable_info,
                        "theme": theme,
                        "prefix": {"form": prefix["form"], "meaning": prefix["meaning"]},
                        "root": {"form": root["form"], "meaning": root["meaning"]},
                        "suffix": {"form": suffix["form"], "meaning": suffix["meaning"]}
                    }
            except (IndexError, StopIteration):
                continue

        print(f"Could not generate a valid word for theme: {theme}")
        return None


def main():
    # Initialize the word generator
    generator = WordGenerator()

    print("Generating 5 random words:")
    words = generator.generate_multiple(5)
    for word in words:
        print("\nGenerated word:", word["word"])
        print("Segments:", word["segments"])
        if word.get("syllables"):
            print("Syllables:", word["syllables"]["count"])
            syllables = [comp["syllable"] for comp in word["syllables"]["components"]]
            print("Syllable breakdown:", "-".join(syllables))
        if word["prefix"]:
            print("Prefix meaning:", word["prefix"]["meaning"])
        if word["root"]:
            print("Root meaning:", word["root"]["meaning"])
        if word["suffix"]:
            print("Suffix meaning:", word["suffix"]["meaning"])

    print("\nGenerating themed words:")
    themes = ["society", "color", "movement", "human_body"]
    for theme in themes:
        print(f"\nTrying theme: {theme}")
        themed_word = generator.generate_themed_word(theme)
        if themed_word:
            print("Generated word:", themed_word["word"])
            print("Segments:", themed_word["segments"])
            if themed_word.get("syllables"):
                print("Syllables:", themed_word["syllables"]["count"])
                syllables = [comp["syllable"] for comp in themed_word["syllables"]["components"]]
                print("Syllable breakdown:", "-".join(syllables))
            print("Theme:", themed_word["theme"])
            print("Meanings:", {
                "prefix": themed_word["prefix"]["meaning"],
                "root": themed_word["root"]["meaning"],
                "suffix": themed_word["suffix"]["meaning"]
            })


if __name__ == "__main__":
    main()