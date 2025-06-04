import bibtexparser
import sys
import re
import os
from calendar import month_name
from typing import List

FIELDS_TO_DELETE = [
    "website", "badges", "renamedfrom"
]

FIELD_ORDER = [
    'title',
    'author',
    'editor',
    'journal',
    'booktitle',
    'type'
    'publisher',
    'school',
    'howpublished',
    'address',
    'year',
    'month',
    'location',
    'volume',
    'number',
    'numpages',
    'pages',
    'articleno',
    'keywords',
    'doi',
    'url',
    'isbn',
    'pissn',
    'annotation',
    'note',
    'award_name',
    'award',
    'pdf',
    'code',
    'slides',
    'video',
    'supp',
    'selected',
]

def parsebool(string):
    return string == "true"

def compile(entries):
    new_entries = []
    for entry in entries:
        # only put entries to my website I want there to be
        if parsebool(entry["website"]):
            new_entries.append(entry)

    for entry in new_entries:
        # delete entries that should be deleted
        for delfield in FIELDS_TO_DELETE:
            if delfield in entry:
                entry.pop(delfield)
        # Add the "bibtex_show" attribute so that people can download the bibtex code on our website.
        entry["bibtex_show"] = ""

    return new_entries

def order_fields(entries: List[dict], field_order=None) -> List[dict]:
    if field_order is None:
        field_order = FIELD_ORDER

    ordered_entries = []
    for entry in entries:
        ordered_entry = {'ENTRYTYPE': entry['ENTRYTYPE'], 'ID': entry['ID']}
        # Add known fields in order
        for field in field_order:
            if field in entry:
                ordered_entry[field] = entry[field]
        # Add remaining fields (not in specified order)
        for key in entry:
            if key not in ordered_entry and key not in ['ENTRYTYPE', 'ID']:
                ordered_entry[key] = entry[key]
        ordered_entries.append(ordered_entry)
    return ordered_entries

def order_entries(entries: List[dict]) -> List[dict]:
    # Helper: convert month to numeric value (handles "January", "Jan", "1", etc.)
    def month_to_num(m):
        m = str(m).lower().strip()
        months = {name.lower(): i for i, name in enumerate(month_name) if name}
        short = {name[:3].lower(): i for i, name in enumerate(month_name) if name}
        try:
            return int(m)
        except ValueError:
            return months.get(m, short.get(m[:3], 0))

    # Sort entries by year, then month (descending)
    return sorted(
        entries,
        key=lambda e: (int(e.get('year', 0)), month_to_num(e.get('month', 0))),
        reverse=True
    )

### IO

def sanitize_bibtex(content):
    # Replace unquoted true/false with quoted strings, allowing arbitrary whitespace
    content = re.sub(r'=\s*true\b', '= "true"', content, flags=re.IGNORECASE)
    content = re.sub(r'=\s*false\b', '= "false"', content, flags=re.IGNORECASE)
    return content

def load_bibtex_file(variables, file_path):
    with open(file_path, 'r', encoding='utf-8') as bibtex_file:
        contents = variables.rstrip('\n') + '\n' + bibtex_file.read()
        contents = sanitize_bibtex(contents)
        bib_database = bibtexparser.loads(contents)
    return bib_database.entries

def save_bibtex_file(entries, output_path):
    writer = bibtexparser.bwriter.BibTexWriter()
    writer.order_entries_by = ('year', 'month')
    writer.indent = '  '
    writer.align_values = True
    writer.add_blank_lines = True

    ## TODO: Write a custom exporter because this one messes up ordering of attributes.
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = entries
    with open(output_path, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(db, bibtex_file, writer=writer)

def export_bibtex(entries: List[dict], align_equal=True) -> str:
    bib_lines = []

    for entry in entries:
        bib_lines.append(f"@{entry['ENTRYTYPE']}{{{entry['ID']},")

        # Extract fields in current order (excluding ENTRYTYPE and ID)
        fields = [(k, v) for k, v in entry.items() if k not in ['ENTRYTYPE', 'ID']]

        # Align '=' signs if requested
        maxlen = max(len(k) for k, _ in fields) if align_equal and fields else 0

        for i, (key, value) in enumerate(fields):
            eq = ' = ' if align_equal else '='
            padding = ' ' * (maxlen - len(key)) if align_equal else ''
            comma = ',' if i < len(fields) - 1 else ''
            bib_lines.append(f"    {key}{padding}{eq}{{{value}}}{comma}")

        bib_lines.append("}\n")  # Close entry and add a blank line

    return '\n'.join(bib_lines)

def save_file(content, output_path):
    with open(output_path, "w") as text_file:
        text_file.write(content)

### These two functions are used to load the MYabrv.tex and all variables loaded at the top of literature.bib because I use these variables in BibPax/papers.bib.

def truncate_after_match(text, pattern):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if pattern in line:
            return '\n'.join(lines[:i])  # Exclude matching line and everything after
    return text  # Return original if no match

def load_variables(literature_path, abrv_path):
    with open(abrv_path, 'r', encoding='utf-8') as abrv_file:
      with open(literature_path, 'r', encoding='utf-8') as literature_file:
          lit = truncate_after_match(
              literature_file.read(),
              "%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Unpublished Entries %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
          )
          contents = abrv_file.read().rstrip('\n') + '\n' + lit
          return contents

# 1: path to papers.bib from BibPax
# 2: path to BibTags
# 3: path to which to write output
if __name__ == "__main__":
    input_path = sys.argv[1]
    bibtags_path = sys.argv[2]
    output_path = sys.argv[3]

    # todo: merge this simplification into phd generator
    lit_path = os.path.join(bibtags_path, "literature/literature.bib")
    abrv_path = os.path.join(bibtags_path, "literature/MYabrv.bib")

    print("Using bibtexparser version", bibtexparser.__version__)

    print("Reading:", input_path)

    variables = load_variables(lit_path, abrv_path)
    entries = load_bibtex_file(variables, input_path)
    entries = compile(entries)
    entries = order_fields(entries)
    entries = order_entries(entries)

    print("Writing:", output_path)
    text = export_bibtex(entries)
    save_file(text, output_path)
