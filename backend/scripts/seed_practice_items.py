"""Seed word-tier practice items into app.practice_items.

Checks first, inserts second:
  1. every phone code exists in the phoneme inventory
  2. the target sound really sits at the stated position in the word
  3. where the word occurs in the corpus lexicon, the phones are compared

Nothing is inserted if check 1 or 2 fails. Check 3 only warns.

Run from backend/ with the venv active:
    python -m scripts.seed_practice_items --author you@example.com --dry-run
    python -m scripts.seed_practice_items --author you@example.com

--author is the email of an existing account (practice_items.authored_by).
Safe to re-run: rows that already exist are skipped.
"""
import argparse
import csv
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from db.session import SessionLocal
from db.models import PracticeItem, Phoneme, User
from scripts.seed_phonemes import PHONES
from scripts.content_words import WORDS

LANG = "ur"
DISCIPLINE = "slt"
LEXICON = Path("scoring/data/lexicon.csv")
IPA = {label: ipa for label, ipa, _ in PHONES}


def check_words():
    errors = []
    seen = set()
    for sound, pos, urdu, tr, gloss, phones in WORDS:
        ph = phones.split()
        bad = [p for p in ph if p not in IPA]
        if sound not in IPA:
            errors.append(f"{urdu}: target sound {sound!r} is not a known phone")
            continue
        if bad:
            errors.append(f"{urdu} ({tr}): unknown phone(s) {bad}")
            continue
        where = {
            "initial": ph[0] == sound,
            "final": ph[-1] == sound,
            "medial": sound in ph[1:-1],
        }.get(pos)
        if not where:
            errors.append(f"{urdu} ({tr}): {sound} is not {pos} in '{phones}'")
        if (sound, pos, urdu) in seen:
            errors.append(f"{urdu}: listed twice for {sound}/{pos}")
        seen.add((sound, pos, urdu))
    return errors


def corpus_pronunciations():
    if not LEXICON.exists():
        return None
    out = {}
    with open(LEXICON, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["urdu"], set()).add(r["cisampa"])
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--author", required=True, help="email of an existing user")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    errors = check_words()
    if errors:
        print("Fix these in scripts/content_words.py, then run again:")
        for e in errors:
            print("  -", e)
        raise SystemExit(1)
    print(f"checks passed: {len(WORDS)} words, {len({w[0] for w in WORDS})} sounds")

    corpus = corpus_pronunciations()
    verified = set()
    if corpus is None:
        print("lexicon.csv not found, skipping the corpus cross-check")
    else:
        differing, not_in = [], 0
        for sound, pos, urdu, tr, gloss, phones in WORDS:
            if urdu not in corpus:
                not_in += 1
            elif phones in corpus[urdu]:
                verified.add(urdu)
            else:
                differing.append((urdu, tr, phones, sorted(corpus[urdu])))
        print(f"corpus cross-check: {len(verified)} match, "
              f"{len(differing)} differ, {not_in} not in corpus")
        for urdu, tr, mine, theirs in differing:
            print(f"  DIFFERS {urdu} ({tr}): mine '{mine}' | corpus {theirs}")

    per = Counter((w[0], w[1]) for w in WORDS)
    print("\nsound  initial medial final")
    for s in dict.fromkeys(w[0] for w in WORDS):
        print(f"{s:6s} {per[(s, 'initial')]:7d} {per[(s, 'medial')]:6d} {per[(s, 'final')]:5d}")

    if args.dry_run:
        print("\ndry run: nothing written")
        return

    db = SessionLocal()
    try:
        author = db.query(User).filter(User.email == args.author).one_or_none()
        if author is None:
            raise SystemExit(f"no user with email {args.author}")
        pid = {p.label: p.id for p in
               db.query(Phoneme).filter(Phoneme.language_code == LANG)}
        missing = {w[0] for w in WORDS} - set(pid)
        if missing:
            raise SystemExit(f"run seed_phonemes first, missing: {sorted(missing)}")

        existing = {
            (i.text_native, i.target_phoneme_id, i.position)
            for i in db.query(PracticeItem).filter(
                PracticeItem.language_code == LANG, PracticeItem.tier == "word")
        }
        now = datetime.now(timezone.utc)
        added = 0
        for sound, pos, urdu, tr, gloss, phones in WORDS:
            if (urdu, pid[sound], pos) in existing:
                continue
            db.add(PracticeItem(
                id=uuid.uuid4(),
                language_code=LANG,
                discipline_key=DISCIPLINE,
                kind="practice",
                tier="word",
                text_native=urdu,
                transliteration=tr,
                gloss_en=gloss,
                ipa=" ".join(IPA[p] for p in phones.split()),
                ipa_source="csalt_corpus" if urdu in verified else "manual",
                target_phoneme_id=pid[sound],
                position=pos,
                elicitation_modes=["repeat"],
                is_screening_probe=False,
                status="published",
                authored_by=author.id,
                published_at=now,
                created_at=now,
                updated_at=now,
            ))
            added += 1
        db.commit()
        print(f"\nadded {added}, skipped {len(WORDS) - added} already present")
    finally:
        db.close()


if __name__ == "__main__":
    main()