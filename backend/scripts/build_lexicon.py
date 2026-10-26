"""Build a word -> phones lexicon from the Urdu phonetic speech corpus.

Pairs Transcription-UNICODE-Arabic.txt (Urdu script) with
Transcription-CISAMPA.txt (phones) sentence by sentence, word by word.
Sentences whose word counts differ are skipped, never guessed.

Run from backend/ with the venv active:

    python -m scripts.build_lexicon                      # build the CSV
    python -m scripts.build_lexicon --find "K AE L AA"   # look up a phone sequence
    python -m scripts.build_lexicon --sound K --where initial --maxlen 4 --top 30

The CSV goes to scoring/data/ (gitignored). Read the corpus licence before
copying any of its content into the app or the repo.
"""
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

from scripts.seed_phonemes import PHONES

DEFAULT_DIR = Path(r"C:\Users\HP\Downloads\UrduPhoneticSpeechCorpus")
OUT = Path("scoring/data/lexicon.csv")
IPA = {label: ipa for label, ipa, _ in PHONES}


def to_ipa(phones):
    return " ".join(IPA.get(p, f"[{p}]") for p in phones.split())


def read_cisampa(path):
    sentences = []
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("<s>##"):
            continue  # skips the format header and blank lines
        body = line.replace("<s>", "").replace("</s>", "")
        sentences.append([w.split() for w in body.split("##") if w.strip()])
    return sentences


def read_urdu(path):
    text = path.read_text(encoding="utf-8-sig")
    return [line.split() for line in text.splitlines() if line.strip()]


def build(corpus):
    phones = read_cisampa(corpus / "Transcription-CISAMPA.txt")
    urdu = read_urdu(corpus / "Transcription-UNICODE-Arabic.txt")
    print(f"sentences: cisampa={len(phones)}, urdu={len(urdu)}")
    if len(phones) != len(urdu):
        print("WARNING: sentence counts differ, so alignment may be off. "
              "Check the files before trusting the lexicon.")

    counts = Counter()
    ok = skipped = 0
    for a, b in zip(phones, urdu):
        if len(a) != len(b):
            skipped += 1
            continue
        ok += 1
        for ph, word in zip(a, b):
            counts[(word, " ".join(ph))] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["urdu", "cisampa", "ipa", "count"])
        for (word, ph), n in counts.most_common():
            w.writerow([word, ph, to_ipa(ph), n])

    print(f"aligned sentences: {ok}, skipped (word count mismatch): {skipped}")
    print(f"unique word/pronunciation pairs: {len(counts)}")
    print(f"written to {OUT.resolve()}")


def load():
    if not OUT.exists():
        raise SystemExit("lexicon.csv not found. Run without arguments first to build it.")
    with open(OUT, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def show(rows, top):
    for r in rows[:top]:
        print(f"{r['urdu']:14s} {r['cisampa']:24s} {r['ipa']:22s} x{r['count']}")
    print(f"({min(top, len(rows))} of {len(rows)} shown)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR, help="corpus folder")
    ap.add_argument("--find", help='exact CISAMPA sequence, e.g. "K AE L AA"')
    ap.add_argument("--sound", help="CISAMPA label to search for, e.g. K or TT")
    ap.add_argument("--where", choices=["initial", "medial", "final", "any"], default="any")
    ap.add_argument("--maxlen", type=int, default=99, help="max phones per word")
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args()

    if args.find:
        rows = [r for r in load() if r["cisampa"] == args.find.strip()]
        show(rows, args.top)
    elif args.sound:
        rows = []
        for r in load():
            ph = r["cisampa"].split()
            if len(ph) > args.maxlen:
                continue
            hit = {
                "initial": ph[0] == args.sound,
                "final": ph[-1] == args.sound,
                "medial": args.sound in ph[1:-1],
                "any": args.sound in ph,
            }[args.where]
            if hit:
                rows.append(r)
        show(rows, args.top)
    else:
        build(args.dir)


if __name__ == "__main__":
    main()