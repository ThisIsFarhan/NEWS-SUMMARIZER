# Extractive Text Summarizer Using NLP  

This project implements an **Extractive Text Summarizer** using **NLP techniques** and provides a **Streamlit interface** for user interaction. Users can input text, and the application generates a concise summary based on the implemented NLP logic.  

---

## Features  

- **NLP-Based Summarization**: Uses an extractive summarization algorithm to highlight important parts of the text.  
- **Streamlit User Interface**: Interactive and easy-to-use interface for entering text and displaying the summary.  
- **Customizable Summarization Logic**: The algorithm uses keywords, scoring, and similarity metrics to extract key sentences.  

---

## Code Structure  

### Backend: Summarizer Logic  

The summarization logic is implemented in a Python module (`summarizer.py`) that:  

1. **Preprocesses Text**: Removes stop words and stems specific words using SpaCy and NLTK.  
2. **Keyword Extraction**: Builds a keyword table using title words, named entities, cardinal numbers, and nouns.  
3. **Sentence Scoring**: Assigns a score to each sentence based on the keyword table.  
4. **Similarity Filtering**: Removes redundant sentences by comparing their similarity scores.  
5. **Final Summary**: Selects top-ranked sentences for the summary based on the desired percentage.  

### Frontend: Streamlit Application  

The **Streamlit app** (`app.py`) provides an interface for the summarizer. Features include:  
- **Text Input**: Users can enter the text they want to summarize.  
- **Summarization**: Clicking the **Summarize** button processes the text and generates the summary.  
- **Real-Time Output**: Displays both the input text and the generated summary interactively.  

---

## Installation  

### Prerequisites  

- Python 3.8+  
- Required Python libraries:  
  - `spacy`  
  - `nltk`  
  - `streamlit`  

### Steps  

1. Clone the repository:  
   ```bash
   git clone https://github.com/ThisIsFarhan/NEWS-SUMMARIZER.git
   cd NEWS-SUMMARIZER
