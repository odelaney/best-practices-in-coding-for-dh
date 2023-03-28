"""This file runs named entity recognition on the letter input of your choice.

Run this on the command line without arguments. It will:
Print the named entities
Output a visualisation as html"""

from bs4 import BeautifulSoup
import en_core_web_sm
import spacy
from spacy import displacy
import json
from pathlib import Path

def extract_transcription():

    """Opens the file and formats the transcription of the letter element for further processing

    Parameters
    ----------

    Returns
    -------
    transcription
        a cleaned version of the letter element
    """

    with open("data/henslow/letters_152.xml", encoding="utf-8") as file:
        letter = BeautifulSoup(file, "lxml-xml")

    transcription = letter.find(type="transcription").text

    transcription = transcription.replace("& ", "and ")

    return transcription

def process_transcription(transcription):
    nlp = en_core_web_sm.load()

    nlp.meta

    spacy.explain("FAC")

    document = nlp(transcription)
    document.text

    for entity in document.ents:
        print(f"{entity.text}: {entity.label_}")

    return document

def format_json(document):
    doc_dict = document.to_json()
    doc_dict

    ents_dict = {key: value for (key, value) in doc_dict.items() if key == "ents"}
    ents_dict

    json.dumps(ents_dict)
    displacy.render(document, style="ent")

def output_results(document):
    # Create a filepath for the output file
    output_file = Path("results/ent_viz.html")

    # Give the document a title for reference
    document.user_data[
        "title"
    ] = "Letter from William Christy, Jr., to John Henslow, 26 February 1831"

    # Output the visualisation as HTML
    html = displacy.render(document, style="ent", jupyter=False, page=True)

    # Write the HTML to the output file
    output_file.open("w", encoding="utf-8").write(html)

def main():
    text = extract_transcription()
    doc = process_transcription(text)
    format_json(doc)
    output_results(doc)

if __name__ == "__main__":
    main()