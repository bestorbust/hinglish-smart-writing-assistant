"""Hinglish Smart Writing Assistant: transliteration, editing and translation demo."""
import re
import streamlit as st
from core import fallback, polish_text, translate_text, normalize_hinglish

st.set_page_config(page_title="Hinglish Smart Writing Assistant", page_icon="✍️")
st.title("Hinglish Smart Writing Assistant")
st.caption("Turn Roman-script Hinglish into readable Devanagari, polish phrasing, and optionally translate.")

def transliterate(text: str, use_model: bool) -> tuple[str, str]:
    if use_model:
        try:
            from ai4bharat.transliteration import XlitEngine
            engine = XlitEngine("hi", beam_width=10)
            norm = normalize_hinglish(text)
            out = []
            for token in re.findall(r"[A-Za-z]+|[^A-Za-z]+", norm):
                if token.isalpha():
                    pred = engine.translit_word(token.lower(), topk=1)
                    out.append(next(iter(pred.values()))[0] if isinstance(pred, dict) else str(pred))
                else:
                    out.append(token)
            return "".join(out), "AI4Bharat IndicXlit neural model applied."
        except Exception as exc:
            return fallback(text), f"IndicXlit unavailable ({type(exc).__name__}); context-aware hybrid transliterator applied."
    return fallback(text), "Context-aware hybrid lexicon and phonetic transliteration applied."

with st.sidebar:
    st.subheader("Model settings")
    model = st.checkbox("Use AI4Bharat IndicXlit if installed", value=False)
    st.caption("IndicXlit requires its separately installed runtime and weights. Built-in engine works offline without downloads.")
    target = st.selectbox(
        "Translation target",
        ["English", "Hindi", "Kannada", "Tamil", "Telugu"],
        index=0,
        key="target"
    )
    st.caption("Translates Hinglish into your selected language (neural translation with offline phrase/pattern fallback).")
    st.markdown("---")
    st.markdown("**Context-Aware Typo & Slang Handling:**")
    st.caption("• Shorthand resolution: `rha` → `raha`, `kr` → `kar`, `h` → `hai`/`hain`\n"
               "• Typo & fuzzy correction: `offce` → `office`, `meting` → `meeting`\n"
               "• Clause context disambiguation: `ap kaisa ho` → `aap kaise ho`")

text = st.text_area("Enter Roman-script Hinglish", "Main offce ja rha hu", height=120)
if st.button("Transform text", type="primary"):
    norm_text = normalize_hinglish(text)
    if norm_text.strip().lower() != text.strip().lower():
        st.info(f"💡 **Context-aware interpretation:** \"{norm_text}\" *(auto-corrected informal spelling/shorthand)*")

    native, note = transliterate(text, model)
    st.subheader("Native-script output")
    st.write(native)
    st.caption(note)

    st.subheader("Polished Roman text")
    st.write(polish_text(text))

    translated, trans_note = translate_text(text, target, native)
    st.subheader(f"Translation output ({target})")
    st.write(translated)
    st.caption(trans_note)

with st.expander("How this prototype works"):
    st.write(
        "1. **Context-Aware Error Tolerance**: Understands informal texting shorthand (e.g. `rha`, `kr`, `pni`, `chye`), resolves typos via fuzzy matching (`offce` → `office`), and disambiguates words using surrounding context.\n"
        "2. **Transliteration**: Uses an extensive Hinglish lexicon coupled with a rule-based phonetic engine. Words not found in the dictionary are transliterated phonetically, ensuring complete Devanagari script conversion without leaving words in Roman characters.\n"
        "3. **Polishing**: Standardizes chat shorthand, normalizes repeated vowel/consonant letters, cleans punctuation, and fixes capitalization.\n"
        "4. **Translation**: Connects to neural machine translation for English, Kannada, Tamil, Hindi, and Telugu when online, and falls back to a multi-phrase, template-based offline grammar engine when offline."
    )
