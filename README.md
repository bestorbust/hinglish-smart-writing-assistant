# ✍️ Hinglish Smart Writing Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Benchmark Accuracy](https://img.shields.io/badge/Benchmark%20Accuracy-100%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, context-aware writing and translation assistant for Romanized Hindi-English (**Hinglish**). It automatically resolves informal texting shorthand and typos, converts Roman script into fluent **Devanagari**, polishes readability, and translates into multiple Indic languages and English.

**Individual Submission:** Priya Darshini P  
**Coursework:** Working With Large Language Models (WWLLM) — CIE 3 Activity

---

## 🌟 Key Features

1. **Context-Aware Error & Slang Tolerance**
   - **Texting Shorthand Resolution**: Automatically detects and expands common informal contractions (e.g., `rha` $\rightarrow$ `raha`, `kr` $\rightarrow$ `kar`, `pni` $\rightarrow$ `paani`, `chye` $\rightarrow$ `chahiye`).
   - **Fuzzy Typo Tolerance**: Resolves misspelled English loanwords and Hindi terms (e.g., `offce` / `ofice` $\rightarrow$ `office`, `meting` $\rightarrow$ `meeting`, `namste` $\rightarrow$ `namaste`).
   - **Clause Context Disambiguation**: Infers ambiguous tokens based on grammatical context (e.g., in `hum ghr ja rhe h`, `h` is disambiguated to `hain` rather than `hai` because of the plural subject `hum`).

2. **Dual-Engine Devanagari Transliteration**
   - **Hybrid Lexicon + Phonetic Rules**: Includes an extensive vocabulary of conversational Hinglish and loanwords (`office`, `doctor`, `hospital`, `call`, `station`, etc.) paired with an open-vocabulary sound-based phonetic engine for arbitrary unseen words and proper names (e.g., `Priya`, `Lonavala`).
   - **Optional AI4Bharat IndicXlit Support**: Seamlessly switchable via the UI for users who have the official pretrained model installed.

3. **Readable Roman Text Polishing**
   - Fixes capitalization, normalizes elongated chat spellings (e.g., `haaaan` $\rightarrow$ `haan`, `theeeek` $\rightarrow$ `theek`), formats punctuation, and expands abbreviations.

4. **Multilingual Translation**
   - Real-time translation to **English**, **Hindi**, **Kannada**, **Tamil**, and **Telugu**.
   - Built-in offline grammar template engine ensures functional translations even without an active internet connection.

---

## 📊 Live Demonstration Examples

| Input (Informal / Typos) | Auto-Understood Context | Native Devanagari | Polished Roman Text | English Translation |
| :--- | :--- | :--- | :--- | :--- |
| `Main offce ja rha hu` | `Main office ja raha hoon` | **मैं ऑफिस जा रहा हूँ** | `Main office ja raha hoon.` | *I am going to office.* |
| `namste ap kaisa ho? main thek hu` | `namaste aap kaise ho? main theek hoon` | **नमस्ते आप कैसे हो? मैं ठीक हूँ** | `Namaste aap kaise ho? Main theek hoon.` | *Hello how are you? I am fine.* |
| `kl subh meting h` | `kal subah meeting hai` | **कल सुबह मीटिंग है** | `Kal subah meeting hai.` | *There is a meeting tomorrow morning.* |
| `mujhe pni chye plzz` | `mujhe paani chahiye please` | **मुझे पानी चाहिए प्लीज़** | `Mujhe paani chahiye please.` | *I need water please.* |
| `hum ghr ja rhe h` | `hum ghar ja rahe hain` | **हम घर जा रहे हैं** | `Hum ghar ja rahe hain.` | *We are going home.* |

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/hinglish-smart-writing-assistant.git
cd hinglish-smart-writing-assistant
```

### 2. Create and Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Optional)* To test with AI4Bharat IndicXlit:
```bash
pip install -r requirements-model.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Evaluation & Benchmark Results

The repository includes a 30-case validation benchmark in `evaluation_cases.csv` testing closed-lexicon consistency, phonetic reproduction, and script conversion.

To run the evaluation script:
```bash
python evaluate.py
```

### Benchmark Metrics:
- **Test Cases:** 30
- **Exact-Match Accuracy:** `100.0%`
- **Mean Character Error Rate (CER):** `0.000`

---

## 📁 Repository Structure

```text
├── app.py                   # Streamlit web application & interactive UI
├── core.py                  # Normalization, phonetic transliteration & translation engine
├── evaluate.py              # Benchmark evaluation script (accuracy & CER)
├── evaluation_cases.csv     # 30-case evaluation dataset
├── requirements.txt         # Core dependencies (Streamlit, Requests, Pandas)
├── requirements-model.txt   # Optional AI4Bharat IndicXlit dependencies
├── .gitignore               # Ignored environments, cache, and system files
└── README.md                # Project documentation
```

---

## 🎯 Coursework Rubric Mapping

- **Problem Formulation:** Solves informal script conversion, typos, and translation barriers in everyday code-mixed Hindi-English text.
- **Modeling & Logic:** Hybrid rule-based phonetic engine + context normalizer with optional integration for pretrained neural models (`AI4Bharat IndicXlit`).
- **User Interface:** Streamlit app featuring real-time feedback, target language selection, and context-interpretation cues.
- **Evaluation:** Quantitative assessment via exact-match accuracy and Character Error Rate (CER).

---

## 📚 References & Acknowledgments

- [AI4Bharat IndicXlit](https://github.com/AI4Bharat/IndicXlit) — Pretrained Indic transliteration framework
- [Aksharantar Benchmark](https://github.com/AI4Bharat/IndianNLP-Transliteration) — Multi-script dataset for Indian languages
- [Streamlit](https://streamlit.io/) — Python application framework
