This dataset (in morphemes.json) has been curated with the objective of enabling automated access. 

It houses prefixes, roots/stems, and suffixes, along with meanings and other associated characteristics.

An initial count shows 2400+ groupings, containing 3000+ prefixes, 1000+ roots/stems, and 800+ suffixes.


Prefixes:

Fields associated with prefixes are as follows:
* form: the prefix characters as they would exist in a word (eg. "ab")
* root: reference to the form,with "-" appended (eg. "ab-")
* loc: the fixed value "prefix"
* attach_to: a list of parts of speech that this prefix would attach to (eg. ["noun"])
* category: one of the following values (this list is extensible):
  * preposition-like
  * relating to
  * negation
  * ...


Suffixes:

Fields associated with suffixes are as follows:
* form: the suffix characters as they would exist in a word (eg. "able")
* root: reference to the form,with "-" prepended (eg. "-able")
* loc: the fixed value "suffix"
* pos: part of speech (allows for multiples)
* type:
  * derivational
  * inflectional


Roots/Stems:

Fields associated with roots/stems are as follows:
* form: the root/stem characters as they would exist in a word (eg. "fess")
* root: reference to the form,with "-" prepended and appended (eg. "-fess-")
* loc: the fixed value "embedded"


Entries are grouped according to meaning. Fields in a grouping are:
* meaning: a list of words or phrases that apply to all the prefixes, suffixes, and roots/stems in the grouping
* theme: a categorization of the grouping (eg. "society"). Some values of theme are:
  * color
  * society
  * diminutive
  * human_body
  * gender
  * movement
  * negation
  * proportion
  * ...
* origin: language of origin (eg. "Latin")

Enhanced Dataset (morphemes_enhanced.json):

The enhanced dataset builds upon morphemes.json by adding syllable analysis while streamlining the data structure. Key differences include:

Fields in the enhanced version:
* forms: retained from original (contains root, form, loc, attach_to, category)
* meaning: retained from original
* origin: retained from original
* syllables: new field containing syllable analysis:
  * count: total number of syllables
  * components: array of syllable information:
    * syllable: the syllable text
    * position: array with start and end position [start, end]

Example entry from morphemes_enhanced.json:
```json
{
  "Euro": {
    "forms": [
      {
        "root": "Euro-",
        "form": "Euro",
        "loc": "prefix",
        "attach_to": ["noun"],
        "category": "relating to"
      }
    ],
    "meaning": ["European"],
    "origin": "",
    "syllables": {
      "count": 2,
      "components": [
        {
          "syllable": "Eu",
          "position": [0, 2]
        },
        {
          "syllable": "ro",
          "position": [2, 4]
        }
      ]
    }
  }
}
```

The enhanced dataset:
* Uses NLTK's LegalitySyllableTokenizer for syllable analysis
* Provides precise syllable boundaries through position tracking
* Maintains essential morphological information
* Removes redundant or unused fields for cleaner data structure

Note: Syllable analysis is performed using linguistic principles and may be refined over time as the underlying algorithms improve.
