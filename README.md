# Media Foci Tracker

The **Media Foci Tracker** is a project that aims to develop a program that assesses and analyzes public trends across different countries using Natural Language Processing. The approach involves implementing Named Entity Recognition (NER) and Term Frequency-Inverse Document Frequency (TF-IDF) to obtain meaningful insights.

## Workflow

The following steps are involved in the project workflow:

- **Raw data** - Data is collected from various sources and stored in raw format.
- **Clean text** - The raw data is preprocessed and cleaned to obtain text data in zip format.
- **Clean sentences** - The clean text data is further processed to obtain output clean text.
- **Title extraction** - The first sentence is extracted as the title of the news article.
- **Keywords extraction** - Keywords are extracted using a summarization algorithm for all the news articles.
- **Data organization** - The final output is in the form of a list of tuples containing the date and keywords.

## Conclusion

The Media Foci Tracker project is an innovative approach to track and analyze public trends across different countries. By using NER and TF-IDF techniques, the program can provide meaningful insights into the current public discourse.
