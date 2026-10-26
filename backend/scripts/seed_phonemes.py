"""Seed the Urdu phoneme inventory into app.phonemes.

Source: Mappings.pdf (Appendix A, IPA to SAMPA to CISAMPA) from the
Urdu phonetic speech corpus. 59 phones, safe to re-run.

`label` stores the CISAMPA code, so the corpus lexicon
(Transcription-CISAMPA.txt) can be mapped to phoneme rows later.

Run from backend/ with the venv active:
    python -m scripts.seed_phonemes
"""
import uuid
from collections import Counter

from db.session import SessionLocal
from db.models import Phoneme, Language

LANG = "ur"

DENT = "\u032a"   # dental diacritic
ASP = "\u02b0"    # aspiration (the PDF uses this mark for all aspirated sounds)
NAS = "\u0303"    # nasalisation

# (CISAMPA label, IPA, manner)
PHONES = [
    # stops
    ("P", "p", "stop"), ("P_H", "p" + ASP, "stop"),
    ("B", "b", "stop"), ("B_H", "b" + ASP, "stop"),
    ("T_D", "t" + DENT, "stop"), ("T_D_H", "t" + DENT + ASP, "stop"),
    ("D_D", "d" + DENT, "stop"), ("D_D_H", "d" + DENT + ASP, "stop"),
    ("TT", "\u0288", "stop"), ("TT_H", "\u0288" + ASP, "stop"),   # retroflex t
    ("DD", "\u0256", "stop"), ("DD_H", "\u0256" + ASP, "stop"),   # retroflex d
    ("K", "k", "stop"), ("K_H", "k" + ASP, "stop"),
    ("G", "g", "stop"), ("G_H", "g" + ASP, "stop"),
    ("Q", "q", "stop"),
    ("Y", "\u0294", "stop"),                                       # glottal stop
    # affricates
    ("T_SH", "t\u0283", "affricate"), ("T_SH_H", "t\u0283" + ASP, "affricate"),
    ("D_ZZ", "d\u0292", "affricate"), ("D_ZZ_H", "d\u0292" + ASP, "affricate"),
    # fricatives
    ("F", "f", "fricative"), ("S", "s", "fricative"), ("Z", "z", "fricative"),
    ("SH", "\u0283", "fricative"), ("ZZ", "\u0292", "fricative"),
    ("X", "\u03c7", "fricative"), ("7", "\u0263", "fricative"),    # chi, gamma
    ("H", "h", "fricative"),
    # nasals
    ("M", "m", "nasal"), ("N", "n", "nasal"), ("N_H", "n" + ASP, "nasal"),
    ("NG", "\u014b", "nasal"),
    # liquids and glides
    ("L", "l", "lateral"),
    ("R", "r", "trill"), ("R_H", "r" + ASP, "trill"),
    ("RR", "\u027d", "flap"), ("RR_H", "\u027d" + ASP, "flap"),    # retroflex flap
    ("J", "j", "approximant"), ("V", "v", "approximant"),
    # oral vowels
    ("UU", "u", "vowel"), ("OO", "o", "vowel"), ("O", "\u0254", "vowel"),
    ("AA", "\u0251", "vowel"), ("II", "i", "vowel"), ("AE", "e", "vowel"),
    ("E", "\u025b", "vowel"), ("AY", "\u00e6", "vowel"),
    ("I", "\u026a", "vowel"), ("U", "\u028a", "vowel"), ("A", "\u0259", "vowel"),
    # nasalised vowels
    ("UUN", "u" + NAS, "nasal_vowel"), ("OON", "o" + NAS, "nasal_vowel"),
    ("ON", "\u0254" + NAS, "nasal_vowel"), ("AAN", "\u0251" + NAS, "nasal_vowel"),
    ("IIN", "i" + NAS, "nasal_vowel"), ("AEN", "e" + NAS, "nasal_vowel"),
    ("AYN", "\u00e6" + NAS, "nasal_vowel"),
]

assert len({ipa for _, ipa, _ in PHONES}) == len(PHONES), "duplicate IPA"
assert len({lab for lab, _, _ in PHONES}) == len(PHONES), "duplicate label"


def main():
    db = SessionLocal()
    try:
        if db.get(Language, LANG) is None:
            raise SystemExit("Language 'ur' not found. Run the language seed first.")

        existing = {
            p.ipa: p
            for p in db.query(Phoneme).filter(Phoneme.language_code == LANG)
        }
        added = updated = 0
        for order, (label, ipa, manner) in enumerate(PHONES, start=1):
            row = existing.get(ipa)
            if row is None:
                db.add(Phoneme(
                    id=uuid.uuid4(), language_code=LANG, ipa=ipa,
                    label=label, manner=manner, sort_order=order,
                ))
                added += 1
            else:
                row.label, row.manner, row.sort_order = label, manner, order
                updated += 1
        db.commit()

        print(f"added {added}, updated {updated}, total {len(PHONES)}")
        for manner, n in Counter(m for _, _, m in PHONES).items():
            print(f"  {manner:12s} {n}")
    finally:
        db.close()


if __name__ == "__main__":
    main()