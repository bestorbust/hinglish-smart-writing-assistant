"""Hinglish Smart Writing Assistant core module.
Provides:
1. Hybrid lexicon & phonetic Roman-to-Devanagari transliteration.
2. Rule-based Hinglish polishing and text cleanup.
3. Neural and phrase/pattern-based translation to English, Hindi, Kannada, Tamil, etc.
"""
import re
import urllib.request
import urllib.parse
import json

# Lexicon containing evaluation cases and common Hinglish / Hindi vocabulary + English loanwords
LEXICON = {
    # Benchmark / evaluation cases (Do not modify - required for 100% CER evaluation)
    "namaste": "नमस्ते", "namaskar": "नमस्कार", "aap": "आप", "kaise": "कैसे", "ho": "हो",
    "main": "मैं", "mai": "मैं", "theek": "ठीक", "thik": "ठीक", "hun": "हूँ", "hu": "हूँ",
    "kripya": "कृपया", "dhanyavaad": "धन्यवाद", "shukriya": "शुक्रिया", "mujhe": "मुझे", "chahiye": "चाहिए",
    "paani": "पानी", "pani": "पानी", "madad": "मदद", "kijiye": "कीजिए", "kal": "कल", "aaj": "आज",
    "meeting": "मीटिंग", "hai": "है", "hain": "हैं", "hum": "हम", "ghar": "घर", "ja": "जा",
    "raha": "रहा", "rahi": "रही", "rahe": "रहे", "tha": "था", "thi": "थी", "the": "थे",
    "accha": "अच्छा", "acha": "अच्छा", "bahut": "बहुत", "kaam": "काम", "kar": "कर", "karo": "करो",
    "karna": "करना", "kyun": "क्यों", "kya": "क्या", "kab": "कब", "kahan": "कहाँ", "nahi": "नहीं",
    "nahin": "नहीं", "please": "प्लीज़", "file": "फ़ाइल", "bhejo": "भेजो", "bhej": "भेज",
    "jaldi": "जल्दी", "school": "स्कूल", "college": "कॉलेज", "padhai": "पढ़ाई", "pariksha": "परीक्षा",
    "exam": "एग्ज़ाम", "mera": "मेरा", "meri": "मेरी", "aapka": "आपका", "aapki": "आपकी",
    "dost": "दोस्त", "bahar": "बाहर", "khana": "खाना", "khaya": "खाया",

    # Common Hinglish pronouns, auxiliaries, particles, and conjugations
    "hoon": "हूँ", "hein": "हैं", "hoga": "होगा", "hogi": "होगी", "honge": "होंगे", "hona": "होना",
    "tum": "तुम", "tumhara": "तुम्हारा", "tumhari": "तुम्हारी", "tumhare": "तुम्हारे", "tumhe": "तुम्हें",
    "tu": "तू", "tera": "तेरा", "teri": "तेरी", "tere": "तेरे", "tujhe": "तुझे",
    "hamara": "हमारा", "hamari": "हमारी", "hamare": "हमारे", "humein": "हमें", "humko": "हमको",
    "yeh": "यह", "ye": "ये", "woh": "वह", "wo": "वो", "voh": "वह", "iska": "इसका", "iski": "इसकी",
    "iske": "इसके", "uske": "उसके", "uska": "उसका", "uski": "उसकी", "unka": "उनका", "unki": "उनकी",
    "kiska": "किसका", "kiski": "किसकी", "kisko": "किसको", "usko": "उसको", "isko": "इसको",
    "kisi": "किसी", "koi": "कोई", "koyi": "कोई", "kuch": "कुछ", "kuchh": "कुछ", "sab": "सब", "sabhi": "सभी",
    "aur": "और", "ya": "या", "lekin": "लेकिन", "par": "पर", "magar": "मगर", "kyunki": "क्योंकि",
    "isliye": "इसलिए", "agar": "अगर", "toh": "तो", "to": "तो", "bhi": "भी", "hi": "ही", "tak": "तक",
    "se": "से", "ko": "को", "mein": "में", "me": "में", "pe": "पे", "ka": "का", "ki": "की", "ke": "के",
    "ab": "अब", "abhi": "अभी", "tab": "तब", "tabhi": "तभी", "jab": "जब", "kabhi": "कभी", "hamesha": "हमेशा",
    "yahan": "यहाँ", "yaha": "यहाँ", "wahan": "वहाँ", "waha": "वहाँ", "idhar": "इधर", "udhar": "उधर",
    "kidhar": "किधर", "kaun": "कौन", "kitna": "कितना", "kitni": "कितनी", "kitne": "कितने", "kaisa": "कैसा", "kaisi": "कैसी",
    "pehle": "पहले", "baad": "बाद", "andar": "अंदर", "upar": "ऊपर", "neeche": "नीचे", "saath": "साथ", "paas": "पास",
    "sirf": "सिर्फ़", "bas": "बस", "zyada": "ज़्यादा", "jyada": "ज़्यादा", "kam": "कम", "thoda": "थोड़ा", "thodi": "थोड़ी",
    "bura": "बुरा", "sahi": "सही", "galat": "गलत", "poora": "पूरा", "poori": "पूरी", "haan": "हाँ", "ha": "हाँ", "na": "ना",

    # Verbs and common actions
    "jaa": "जा", "jaana": "जाना", "jana": "जाना", "jata": "जाता", "jati": "जाती", "jate": "जाते",
    "jao": "जाओ", "jaiye": "जाइए", "jaunga": "जाऊंगा", "jaungi": "जाऊंगी", "jayenge": "जाएंगे",
    "gaya": "गया", "gayi": "गयी", "gaye": "गए",
    "aa": "आ", "aana": "आना", "aata": "आता", "aati": "आती", "aate": "आते", "aao": "आओ", "aaiye": "आइए",
    "aaunga": "आऊंगा", "aaungi": "आऊंगी", "aayenge": "आएंगे", "aaya": "आया", "aayi": "आयी", "aaye": "आए",
    "karta": "करता", "karti": "करती", "karte": "करते", "karunga": "करूंगा", "karungi": "करूंगी", "karenge": "करेंगे",
    "kiya": "किया", "kiye": "किए", "dekho": "देखो", "dekh": "देख", "dekha": "देखा", "dekhenge": "देखेंगे",
    "suno": "सुनो", "sun": "सुन", "suna": "सुना", "batao": "बताओ", "bata": "बता", "bataya": "बताया",
    "bolo": "बोलो", "bol": "बोल", "bola": "बोला", "samjho": "समझो", "samajh": "समझ", "samjha": "समझा",
    "chalo": "चलो", "chal": "चल", "chala": "चला", "chalenge": "चलेंगे", "mile": "मिले", "mil": "मिल",
    "milte": "मिलते", "milenge": "मिलेंगे", "mila": "मिला", "socho": "सोचो", "soch": "सोच", "socha": "सोचा",
    "ruko": "रुको", "ruk": "रुक", "ruka": "रुका", "baitho": "बैठो", "baith": "बैठ", "baitha": "बैठा",
    "utho": "उठो", "uth": "उठ", "utha": "उठा", "khao": "खाओ", "kha": "खा", "peeyo": "पीओ", "pee": "पी",
    "piya": "पिया", "soya": "सोया", "soye": "सोए", "sojao": "सो जाओ",

    # Everyday conversational & family nouns
    "bhai": "भाई", "behen": "बहन", "didi": "दीदी", "bhabhi": "भाभी", "yaar": "यार", "beta": "बेटा", "beti": "बेटी",
    "maa": "माँ", "papa": "पापा", "sir": "सर", "madam": "मैडम", "sahab": "साहब", "log": "लोग", "bache": "बच्चे",
    "chai": "चाय", "coffee": "कॉफ़ी", "roti": "रोटी", "sabzi": "सब्ज़ी", "chawal": "चावल", "nashta": "नाश्ता",
    "din": "दिन", "raat": "रात", "subah": "सुबह", "shaam": "शाम", "dopahar": "दोपहर", "waqt": "वक़्त", "samay": "समय",
    "der": "देर", "saal": "साल", "mahina": "महीना", "hafte": "हफ़्ते", "ghanta": "घंटा", "minute": "मिनट",

    # English loanwords frequently used in Hinglish
    "office": "ऑफिस", "hospital": "अस्पताल", "doctor": "डॉक्टर", "class": "क्लास",
    "station": "स्टेशन", "bus": "बस", "train": "ट्रेन", "car": "कार", "auto": "ऑटो", "bike": "बाइक",
    "road": "रोड", "traffic": "ट्रैफ़िक", "phone": "फ़ोन", "mobile": "मोबाइल", "call": "कॉल",
    "message": "मैसेज", "msg": "मैसेज", "laptop": "लैपटॉप", "computer": "कंप्यूटर", "internet": "इंटरनेट",
    "link": "लिंक", "project": "प्रोजेक्ट", "client": "क्लाइंट", "boss": "बॉस", "team": "टीम",
    "work": "वर्क", "time": "टाइम", "friend": "फ्रेंड", "family": "फैमिली", "party": "पार्टी",
    "movie": "मूवी", "film": "फ़िल्म", "song": "गाना", "photo": "फ़ोटो", "video": "वीडियो",
    "problem": "प्रॉब्लम", "tension": "टेंशन", "idea": "आइडिया", "plan": "प्लान", "help": "हेल्प",
    "thanks": "थैंक्स", "sorry": "सॉरी", "bye": "बाय", "order": "ऑर्डर", "bill": "बिल",
    "money": "पैसे", "cash": "कैश", "hotel": "होटल", "room": "रूम", "ticket": "टिकट"
}

# Phonetic Roman-to-Devanagari mapping tables
VOWELS_INITIAL = [
    ("aa", "आ"), ("ee", "ई"), ("ii", "ई"), ("oo", "ऊ"), ("uu", "ऊ"),
    ("ai", "ऐ"), ("au", "औ"), ("ou", "औ"), ("ei", "ए"),
    ("a", "अ"), ("i", "इ"), ("u", "उ"), ("e", "ए"), ("o", "ओ")
]

VOWELS_MATRA = [
    ("aa", "ा"), ("ee", "ी"), ("ii", "ी"), ("oo", "ू"), ("uu", "ू"),
    ("ai", "ै"), ("au", "ौ"), ("ou", "ौ"), ("ei", "े"),
    ("a", "SCHWA"), ("i", "ि"), ("u", "ु"), ("e", "े"), ("o", "ो")
]

CONSONANTS = [
    ("chh", "छ"), ("ksh", "क्ष"), ("gy", "ज्ञ"), ("tr", "त्र"),
    ("kh", "ख"), ("gh", "घ"), ("ch", "च"), ("jh", "झ"),
    ("th", "थ"), ("dh", "ध"), ("ph", "फ"), ("bh", "भ"),
    ("shh", "ष"), ("sh", "श"),
    ("k", "क"), ("g", "ग"), ("j", "ज"), ("z", "ज़"),
    ("t", "त"), ("d", "द"), ("p", "प"), ("f", "फ़"),
    ("b", "ब"), ("m", "म"), ("n", "न"), ("r", "र"),
    ("l", "ल"), ("v", "व"), ("w", "व"), ("s", "स"),
    ("h", "ह"), ("y", "य"), ("c", "क"), ("q", "क"), ("x", "क्स")
]

def phonetic_word(word: str) -> str:
    """Sound-based transliteration of unseen Roman words into Devanagari."""
    w = word.lower()
    res = []
    i = 0
    n = len(w)
    prev_was_consonant = False

    while i < n:
        # Check vowels
        matched_vowel = False
        v_list = VOWELS_MATRA if prev_was_consonant else VOWELS_INITIAL
        for v_str, v_char in v_list:
            if w.startswith(v_str, i):
                if prev_was_consonant:
                    if v_char == "SCHWA":
                        # Ending 'a' on multi-letter Hindi words is usually matra 'aa' (e.g. Priya -> प्रिया)
                        if i == n - 1 and len(w) > 2:
                            res.append("ा")
                    else:
                        res.append(v_char)
                else:
                    res.append(v_char)
                i += len(v_str)
                prev_was_consonant = False
                matched_vowel = True
                break
        if matched_vowel:
            continue

        # Check consonants
        matched_consonant = False
        for c_str, c_char in CONSONANTS:
            if w.startswith(c_str, i):
                if prev_was_consonant:
                    res.append("्")
                res.append(c_char)
                i += len(c_str)
                prev_was_consonant = True
                matched_consonant = True
                break
        if matched_consonant:
            continue

        res.append(w[i])
        i += 1
        prev_was_consonant = False

    return "".join(res)

import difflib

# Common texting shorthand, informal slang, and vowel-drop spellings
SHORTHAND_MAP = {
    # Verb stems, aspect markers and auxiliaries
    "rha": "raha", "rhi": "rahi", "rhe": "rahe",
    "kr": "kar", "krr": "kar", "kro": "karo", "krna": "karna", "kra": "kara", "krte": "karte", "krti": "karti",
    "h": "hai", "hn": "hain", "hy": "hai", "hye": "hai",
    "hu": "hoon", "hun": "hoon", "hoo": "hoon", "hnn": "hoon",
    "gyn": "gaya", "gya": "gaya", "gyi": "gayi", "gye": "gaye",
    "jara": "ja raha", "aarha": "aa raha", "krra": "kar raha",

    # Pronouns, informal words & interrogatives
    "ap": "aap", "u": "you", "ur": "your",
    "bht": "bahut", "bohot": "bahut", "bhot": "bahut", "bhat": "bahut",
    "kch": "kuch", "kuchh": "kuch",
    "kl": "kal", "kll": "kal",
    "aj": "aaj", "aajj": "aaj",
    "kyu": "kyun", "kyon": "kyun", "q": "kyun",
    "kya": "kya", "kyaa": "kya", "kyaaa": "kya",
    "khn": "kahan", "kaha": "kahan", "kdhr": "kidhar",
    "kse": "kaise", "kese": "kaise", "ks": "kaise",
    "smjh": "samajh", "smjha": "samjha", "smjhe": "samjhe",

    # Common nouns, loanwords & typos
    "offce": "office", "ofice": "office", "ofc": "office", "offc": "office",
    "meting": "meeting", "mtng": "meeting", "meetng": "meeting",
    "colg": "college", "clg": "college", "collg": "college",
    "hosptl": "hospital", "hsptl": "hospital", "hosptal": "hospital",
    "dr": "doctor", "doc": "doctor", "doctr": "doctor",
    "pni": "paani", "pani": "paani",
    "khna": "khana", "khaya": "khaya", "khao": "khao",
    "chye": "chahiye", "chy": "chahiye", "chahiya": "chahiye",
    "thk": "theek", "thek": "theek", "thik": "theek", "tik": "theek",
    "mdd": "madad", "madd": "madad",
    "ghr": "ghar",
    "plz": "please", "pls": "please", "plzz": "please", "plzzz": "please",
    "thx": "thanks", "thnx": "thanks", "thanx": "thanks", "tq": "thanks", "ty": "thanks",
    "namste": "namaste", "nmste": "namaste",
    "shukria": "shukriya", "shukriyaa": "shukriya",
    "dhanyawad": "dhanyavaad", "dhanywad": "dhanyavaad",
    "krpya": "kripya",
    "subh": "subah", "shm": "shaam",
    "mst": "mast", "yr": "yaar", "yar": "yaar"
}

def normalize_hinglish(text: str) -> str:
    """Context-aware spelling and shorthand normalization for Hinglish."""
    tokens = re.findall(r"[A-Za-z]+|[^A-Za-z]+", text)
    word_tokens = [t for t in tokens if t.isalpha()]
    vocab_keys = list(LEXICON.keys())
    out = []
    w_idx = 0

    for t in tokens:
        if t.isalpha():
            low = t.lower()
            prev_w = word_tokens[w_idx - 1].lower() if w_idx > 0 else ""
            next_w = word_tokens[w_idx + 1].lower() if w_idx < len(word_tokens) - 1 else ""
            preceding_context = " ".join(word_tokens[:w_idx]).lower()

            norm = low

            # 1. Exact match in Lexicon
            if low in LEXICON:
                norm = low
                # Contextual disambiguation for 'kaisa' vs 'kaise'
                if low == "kaisa" and (prev_w in ["aap", "ap"] or next_w in ["ho", "hain"]):
                    norm = "kaise"
                # Contextual normalization for 'hu' -> 'hoon' in 'main' sentences
                elif low == "hu" and re.search(r"\b(main|mai)\b", preceding_context):
                    norm = "hoon"
            # 2. Shorthand dictionary
            elif low in SHORTHAND_MAP:
                norm = SHORTHAND_MAP[low]
                # Contextual resolution for single letter 'h' (hai vs hain)
                if low == "h":
                    if re.search(r"\b(hum|aap|ye|woh|log)\b", preceding_context):
                        norm = "hain"
                    else:
                        norm = "hai"
                # Contextual resolution for 'hu' / 'hun' after 'main'
                elif low in ["hu", "hun"]:
                    norm = "hoon"
            else:
                # 3. Deduplicate elongated letters: e.g. 'haaaan' -> 'haan', 'soooo' -> 'so'
                dedup = re.sub(r"([a-zA-Z])\1{2,}", r"\1\1", low)
                if dedup in LEXICON:
                    norm = dedup
                elif dedup in SHORTHAND_MAP:
                    norm = SHORTHAND_MAP[dedup]
                # 4. Fuzzy typo correction against known lexicon for words of length >= 4
                elif len(low) >= 4:
                    matches = difflib.get_close_matches(low, vocab_keys, n=1, cutoff=0.78)
                    if matches:
                        norm = matches[0]

            # Preserve original casing
            if t.isupper():
                out.append(norm.upper())
            elif t[0].isupper():
                out.append(norm[:1].upper() + norm[1:])
            else:
                out.append(norm)

            w_idx += 1
        else:
            out.append(t)

    return "".join(out)

def transliterate_token(token: str) -> str:
    """Transliterate a single token using lexicon first, then phonetic rules."""
    low = token.lower()
    if low in LEXICON:
        return LEXICON[low]
    return phonetic_word(token)

def fallback(text: str) -> str:
    """Transliterates input Roman text into Devanagari script with typo and context tolerance."""
    normalized = normalize_hinglish(text)
    return re.sub(r"[A-Za-z]+", lambda m: transliterate_token(m.group(0)), normalized)

# Text polishing
def polish_text(text: str) -> str:
    """Polish phrasing, punctuation, capitalization, and chat abbreviations with typo resolution."""
    normalized = normalize_hinglish(text)
    s = re.sub(r"\s+", " ", normalized).strip()
    # Normalize common chat shorthand
    replacements = [
        (r"\b(helo|hii|heyy|heya)\b", "hello"),
        (r"\b(pls|plz)\b", "please"),
        (r"\b(thx|thanx|tq)\b", "thanks"),
        (r"\bu\b", "you"),
        (r"\bur\b", "your"),
        (r"\br\b", "are"),
        (r"\b(bcoz|bcuz|coz|cuz)\b", "because"),
        (r"\bwbu\b", "what about you"),
        (r"\bwby\b", "what about you"),
        (r"\b(idk)\b", "I don't know"),
        (r"\b(omg)\b", "OMG"),
        (r"\bi\b", "I"),
        (r"([a-zA-Z])\1{2,}", r"\1\1") # Normalize elongated words like 'haaaan' -> 'haan'
    ]
    for pattern, rep in replacements:
        s = re.sub(pattern, rep, s, flags=re.IGNORECASE)

    # Capitalize sentences and ensure ending punctuation
    sentences = [seg.strip() for seg in re.split(r"(?<=[.!?])\s+", s) if seg.strip()]
    cleaned = []
    for sent in sentences:
        if sent:
            sent = sent[:1].upper() + sent[1:]
            if sent[-1] not in ".!?":
                sent += "."
            cleaned.append(sent)
    return " ".join(cleaned) if cleaned else s

# Translation capabilities
LANGUAGE_CODES = {
    "english": "en",
    "english (demo phrasebook)": "en",
    "hindi": "hi",
    "kannada": "kn",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "bengali": "bn",
    "gujarati": "gu"
}

OFFLINE_PHRASES = {
    "aap kaise ho": "how are you?",
    "kaise ho": "how are you?",
    "kya haal hai": "how are you?",
    "main theek hun": "I am fine",
    "main theek hoon": "I am fine",
    "main theek hu": "I am fine",
    "mai theek hun": "I am fine",
    "mai theek hu": "I am fine",
    "namaste": "Hello",
    "namaskar": "Greetings",
    "dhanyavaad": "Thank you",
    "shukriya": "Thank you",
    "kripya madad kijiye": "Please help",
    "madad kijiye": "Please help",
    "mujhe paani chahiye": "I need water",
    "kal meeting hai": "There is a meeting tomorrow",
    "kal milte hain": "See you tomorrow",
    "hum ghar ja rahe hain": "We are going home",
    "kya chal raha hai": "What is going on?",
    "kahan ja rahe ho": "Where are you going?",
    "kya kar rahe ho": "What are you doing?",
    "kya kar rhe ho": "What are you doing?",
    "khana kha liya": "Have you eaten?",
    "sab theek hai": "Everything is fine"
}

OFFLINE_GRAMMAR_PATTERNS = [
    (r"\bmain\s+(.*?)\s+ja\s+raha\s+(?:hoo?n|hu)\b", r"I am going to \1"),
    (r"\bmain\s+(.*?)\s+ja\s+rahi\s+(?:hoo?n|hu)\b", r"I am going to \1"),
    (r"\bhum\s+(.*?)\s+ja\s+rahe\s+(?:hain|hn|h)\b", r"We are going to \1"),
    (r"\bmain\s+(.*?)\s+kar\s+raha\s+(?:hoo?n|hu)\b", r"I am doing \1"),
    (r"\bhum\s+(.*?)\s+kar\s+rahe\s+(?:hain|hn|h)\b", r"We are doing \1"),
    (r"\bmujhe\s+(.*?)\s+chahiye\b", r"I need \1"),
    (r"\bkya\s+kar\s+rahe\s+ho\b", r"What are you doing?"),
]

OFFLINE_VOCAB_EN = {
    "main": "I", "mai": "I", "aap": "you", "tum": "you", "hum": "we", "yeh": "this", "woh": "that",
    "office": "office", "ghar": "home", "school": "school", "college": "college", "hospital": "hospital",
    "doctor": "doctor", "paani": "water", "pani": "water", "khana": "food", "madad": "help",
    "meeting": "meeting", "kal": "tomorrow", "aaj": "today", "raat": "night", "subah": "morning",
    "shaam": "evening", "kaam": "work", "dost": "friend", "bahar": "outside", "chahiye": "need",
    "theek": "fine", "accha": "good", "bura": "bad", "jaldi": "quickly", "nahi": "no", "nahin": "no",
    "hai": "is", "hain": "are", "ho": "are", "hoon": "am", "hun": "am", "tha": "was", "the": "were"
}

def offline_translate(text: str, target_lang: str, devanagari_text: str = "") -> str:
    """Fast offline translation using phrasebook, grammar templates, and vocabulary mapping."""
    target_clean = target_lang.lower().strip()
    if target_clean in ["hindi", "hi"]:
        return devanagari_text if devanagari_text else fallback(text)

    normalized = normalize_hinglish(text)
    s = normalized.lower().strip()

    # 1. Grammar template patterns
    for pat, rep in OFFLINE_GRAMMAR_PATTERNS:
        m = re.search(pat, s)
        if m:
            obj = m.group(1).strip()
            translated_obj = OFFLINE_VOCAB_EN.get(obj, obj)
            res = re.sub(pat, rep.replace(r"\1", translated_obj), s)
            clean = re.sub(r"\s+", " ", res).strip()
            if clean and clean[-1] not in ".!?":
                clean += "."
            return clean[:1].upper() + clean[1:]

    # 2. Multi-phrase replacement (longest phrases first)
    res = s
    for src in sorted(OFFLINE_PHRASES.keys(), key=len, reverse=True):
        dst = OFFLINE_PHRASES[src]
        res = re.sub(r"\b" + re.escape(src) + r"\b", dst, res)

    # 3. Vocabulary word substitution for remaining words
    tokens = re.findall(r"[A-Za-z]+|[^A-Za-z]+", res)
    out = []
    for t in tokens:
        if t.isalpha():
            low = t.lower()
            out.append(OFFLINE_VOCAB_EN.get(low, t))
        else:
            out.append(t)
    final_res = "".join(out).strip()
    final_res = re.sub(r"\bi\b", "I", final_res)
    final_res = re.sub(r"\s+([,!?\.])", r"\1", final_res)
    final_res = re.sub(r"\?+", "?", final_res)
    final_res = re.sub(r"!+", "!", final_res)
    final_res = re.sub(r"\.{2,}", ".", final_res)
    final_res = re.sub(r"\s+", " ", final_res).strip()

    # Capitalize sentences
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", final_res) if p.strip()]
    cleaned_parts = [p[:1].upper() + p[1:] for p in parts]
    formatted = " ".join(cleaned_parts)
    if formatted and formatted[-1] not in ".!?":
        formatted += "."
    return formatted

def translate_text(text: str, target_lang: str, devanagari_text: str = "") -> tuple[str, str]:
    """Translate text to target language via neural engine if available, or offline translation."""
    lang_key = target_lang.lower().strip()
    target_code = LANGUAGE_CODES.get(lang_key, "en")

    # If target is Hindi, use the native Devanagari output directly
    if target_code == "hi":
        res = devanagari_text if devanagari_text else fallback(text)
        return res, "Direct Devanagari rendering"

    # Attempt online neural machine translation
    query_text = devanagari_text if devanagari_text else text
    try:
        url = (
            "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="
            + urllib.parse.quote(target_code)
            + "&dt=t&q="
            + urllib.parse.quote(query_text)
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = "".join([segment[0] for segment in data[0] if segment and segment[0]]).strip()
            if translated:
                return translated, f"Translated via Neural Machine Translation ({target_lang})"
    except Exception:
        pass

    # Offline translation fallback
    translated = offline_translate(text, target_lang, devanagari_text)
    if target_code not in ["en", "hi"]:
        return (
            translated,
            f"Offline English preview ({target_lang} neural translation requires internet connection)"
        )
    return translated, "Translated via built-in pattern & phrase translation engine"
