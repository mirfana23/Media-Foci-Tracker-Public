import pathlib
import os
import nltk
import re
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
regex_email = '[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})'
regex_url = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

def open_file(file_loc): # input = file_loc, output = # list of sentences within a file, detecting a paragraph
    """
    # RULE for sents[row]
    # a proper sentence doesn't contain http/email. It contains less than 3*4-word letter.
    # after a blank, sentence must contain more than two words that have 3 letters.
    # while there is a continuation next line, go on as long as row < len(sents)
        # if sentence(row) ends with -, and there is a sentence on next row
        # if there is a sentnce ends with -, but the next row is blank, wait until there is a proper sentence
            # sometimes 'http' in the middle, so wait till the continuation
        # combine the sentence set as paragraph
    #  finally use sentence_separator
    """
    document = open(file_loc, 'r', encoding="utf8")
    sents = document.readlines()
    document.close()
    sents_clean = []
    title = sents[0]
    row = 2
    while row < len(sents):
        paragraph = str()
        if filter(sents[row],title): row += 1; continue
        paragraph += sents[row][:-1]
        row +=1
        while row < len(sents) and sents[row] != '\n':
            if paragraph.endswith('-'):
                paragraph = paragraph[:-1]
            else: paragraph = paragraph + ' '
            paragraph += sents[row][:-1]
            row +=1
        if paragraph.endswith('-') and row < len(sents):
            paragraph = paragraph[:-1]
            while row < len(sents) and filter(sents[row], title):
                row +=1
            if row < len(sents):
                paragraph += sents[row][:-1]
                row +=1
                while row < len(sents) and sents[row] != '\n':
                    if paragraph.endswith('-'):
                        paragraph = paragraph[:-1]
                    else: paragraph = paragraph + ' '
                    paragraph += sents[row][:-1]
                    row += 1
        paragraph_sents = sent_tokenizer.tokenize(paragraph)
        sents_clean += paragraph_sents
        row = row+1
    return sents_clean



def filter(any_strings,title): # filter
    return any_strings == '/n' or re.search('http', any_strings) or re.search(regex_email, any_strings) or \
           len(re.findall(r'\s?[A-za-z]{3,}\s?', any_strings)) < 2 or title in any_strings
    # len(re.findall(r'\s?[a-z]\s?{3,}',any_strings)) < 2


def final_filter(any_strings):
    return any_strings == '\n' or re.search(regex_url, any_strings) or re.search(regex_email, any_strings)

def write_txt(sents, file_loc):
    document = open(file_loc, 'w', encoding="utf8")
    for row in range(len(sents)):
        if final_filter(sents[row]): continue
        document.writelines(sents[row] + '\n')
    document.close()
    return

def main():

    for filename in os.listdir('text_data_zip'):
        file_loc = str(pathlib.Path().absolute()) + "\\text_data_zip\\" + filename
        sents = open_file(file_loc)
        file_loc = str(pathlib.Path().absolute()) + "\\output_clean_txt\\" + 'clean_' + filename
        write_txt(sents, file_loc)
    return


if __name__ == "__main__":
    main()