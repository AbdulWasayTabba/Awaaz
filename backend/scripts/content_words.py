"""Word-tier practice content for Awaaz: 15 target sounds x 10 words.

Each row: (target sound, position in word, Urdu, transliteration,
           English gloss, CISAMPA phones)

Sound codes and phone codes are the CISAMPA labels from the corpus
(Mappings.pdf). Phone sequences are hand-written, so they are checked by
scripts/seed_practice_items.py against the corpus lexicon where possible.
A few words appear under two sounds on purpose (sarak, gaajar, khargosh,
akhbaar). To change a sound, replace its 10 rows. Nothing else needs editing.
"""

WORDS = [
    # ---- K (k) ----
    ("K", "initial", "کیلا", "kela", "banana", "K AE L AA"),
    ("K", "initial", "کتاب", "kitaab", "book", "K I T_D AA B"),
    ("K", "initial", "کان", "kaan", "ear", "K AA N"),
    ("K", "initial", "کرسی", "kursi", "chair", "K U R S II"),
    ("K", "medial", "بکری", "bakri", "goat", "B A K R II"),
    ("K", "medial", "شکر", "shakar", "sugar", "SH A K A R"),
    ("K", "medial", "دکان", "dukaan", "shop", "D_D U K AA N"),
    ("K", "final", "سڑک", "sarak", "road", "S A RR A K"),
    ("K", "final", "پاک", "paak", "clean", "P AA K"),
    ("K", "final", "نیک", "nek", "good", "N AE K"),

    # ---- G (g) ----
    ("G", "initial", "گاڑی", "gaari", "car", "G AA RR II"),
    ("G", "initial", "گڑیا", "guriya", "doll", "G U RR J AA"),
    ("G", "initial", "گلاب", "gulaab", "rose", "G U L AA B"),
    ("G", "initial", "گاجر", "gaajar", "carrot", "G AA D_ZZ A R"),
    ("G", "medial", "پگڑی", "pagri", "turban", "P A G RR II"),
    ("G", "medial", "بگلا", "bagla", "heron", "B A G L AA"),
    ("G", "medial", "جگنو", "jugnu", "firefly", "D_ZZ U G N UU"),
    ("G", "final", "آگ", "aag", "fire", "AA G"),
    ("G", "final", "ساگ", "saag", "leafy greens", "S AA G"),
    ("G", "final", "ناگ", "naag", "cobra", "N AA G"),

    # ---- T_D (dental t) ----
    ("T_D", "initial", "تالا", "taala", "lock", "T_D AA L AA"),
    ("T_D", "initial", "تیر", "teer", "arrow", "T_D II R"),
    ("T_D", "initial", "تین", "teen", "three", "T_D II N"),
    ("T_D", "initial", "تتلی", "titli", "butterfly", "T_D I T_D L II"),
    ("T_D", "medial", "ستارہ", "sitaara", "star", "S I T_D AA R AA"),
    ("T_D", "medial", "پتلا", "patla", "thin", "P A T_D L AA"),
    ("T_D", "medial", "پتنگ", "patang", "kite", "P A T_D A NG"),
    ("T_D", "final", "رات", "raat", "night", "R AA T_D"),
    ("T_D", "final", "سات", "saat", "seven", "S AA T_D"),
    ("T_D", "final", "دانت", "daant", "tooth", "D_D AA N T_D"),

    # ---- S (s) ----
    ("S", "initial", "سیب", "seb", "apple", "S AE B"),
    ("S", "initial", "سبزی", "sabzi", "vegetable", "S A B Z II"),
    ("S", "initial", "سردی", "sardi", "cold", "S A R D_D II"),
    ("S", "initial", "سائیکل", "saaikal", "bicycle", "S AA II K A L"),
    ("S", "medial", "پیسہ", "paisa", "money", "P AY S AA"),
    ("S", "medial", "بستہ", "basta", "school bag", "B A S T_D AA"),
    ("S", "medial", "بستر", "bistar", "bed", "B I S T_D A R"),
    ("S", "final", "بس", "bas", "bus", "B A S"),
    ("S", "final", "گھاس", "ghaas", "grass", "G_H AA S"),
    ("S", "final", "پیاس", "pyaas", "thirst", "P I J AA S"),

    # ---- Z (z) ----
    ("Z", "initial", "زمین", "zameen", "ground", "Z A M II N"),
    ("Z", "initial", "زرافہ", "zarafa", "giraffe", "Z A R AA F AA"),
    ("Z", "initial", "زیور", "zewar", "jewellery", "Z AE V A R"),
    ("Z", "initial", "زبان", "zabaan", "tongue", "Z A B AA N"),
    ("Z", "medial", "بازار", "bazaar", "market", "B AA Z AA R"),
    ("Z", "medial", "روزہ", "roza", "fast", "R OO Z AA"),
    ("Z", "medial", "دروازہ", "darwaza", "door", "D_D A R V AA Z AA"),
    ("Z", "final", "میز", "mez", "table", "M AE Z"),
    ("Z", "final", "آواز", "aawaaz", "voice", "AA V AA Z"),
    ("Z", "final", "راز", "raaz", "secret", "R AA Z"),

    # ---- SH (sh) ----
    ("SH", "initial", "شیر", "sher", "lion", "SH AE R"),
    ("SH", "initial", "شام", "shaam", "evening", "SH AA M"),
    ("SH", "initial", "شیشہ", "sheesha", "glass", "SH II SH AA"),
    ("SH", "initial", "شلوار", "shalwaar", "trousers", "SH A L V AA R"),
    ("SH", "medial", "کشتی", "kashti", "boat", "K I SH T_D II"),
    ("SH", "medial", "گوشت", "gosht", "meat", "G OO SH T_D"),
    ("SH", "medial", "خوشی", "khushi", "happiness", "X U SH II"),
    ("SH", "final", "آتش", "aatish", "fire", "AA T_D I SH"),
    ("SH", "final", "فرش", "farsh", "floor", "F A R SH"),
    ("SH", "final", "خرگوش", "khargosh", "rabbit", "X A R G OO SH"),

    # ---- F (f) ----
    ("F", "initial", "فیل", "feel", "elephant", "F II L"),
    ("F", "initial", "فون", "phone", "phone", "F OO N"),
    ("F", "initial", "فرج", "fridge", "fridge", "F R I D_ZZ"),
    ("F", "initial", "فراک", "frock", "frock", "F R AA K"),
    ("F", "medial", "کافی", "kaafi", "enough", "K AA F II"),
    ("F", "medial", "سفر", "safar", "journey", "S A F A R"),
    ("F", "medial", "لفافہ", "lifaafa", "envelope", "L I F AA F AA"),
    ("F", "final", "برف", "baraf", "ice", "B A R F"),
    ("F", "final", "صاف", "saaf", "clean", "S AA F"),
    ("F", "final", "لحاف", "lihaaf", "quilt", "L I H AA F"),

    # ---- L (l) ----
    ("L", "initial", "لڑکا", "larka", "boy", "L A RR K AA"),
    ("L", "initial", "لال", "laal", "red", "L AA L"),
    ("L", "initial", "لکڑی", "lakri", "wood", "L A K RR II"),
    ("L", "initial", "لوٹا", "lota", "jug", "L OO TT AA"),
    ("L", "medial", "جلیبی", "jalebi", "jalebi sweet", "D_ZZ A L AE B II"),
    ("L", "medial", "بالٹی", "baalti", "bucket", "B AA L TT II"),
    ("L", "medial", "سالن", "saalan", "curry", "S AA L A N"),
    ("L", "final", "گل", "gul", "flower", "G U L"),
    ("L", "final", "دال", "daal", "lentils", "D_D AA L"),
    ("L", "final", "پھل", "phal", "fruit", "P_H A L"),

    # ---- R (trilled r) ----
    ("R", "initial", "روٹی", "roti", "bread", "R OO TT II"),
    ("R", "initial", "رنگ", "rang", "colour", "R A NG"),
    ("R", "initial", "ریل", "rail", "train", "R AE L"),
    ("R", "initial", "ریچھ", "reechh", "bear", "R II T_SH_H"),
    ("R", "medial", "بارش", "baarish", "rain", "B AA R I SH"),
    ("R", "medial", "مرغی", "murghi", "hen", "M U R 7 II"),
    ("R", "medial", "شربت", "sharbat", "sherbet", "SH A R B A T_D"),
    ("R", "final", "کار", "kaar", "car", "K AA R"),
    ("R", "final", "انار", "anaar", "pomegranate", "A N AA R"),
    ("R", "final", "اخبار", "akhbaar", "newspaper", "A X B AA R"),

    # ---- RR (retroflex flap; never word-initial in Urdu) ----
    ("RR", "medial", "بڑا", "bara", "big", "B A RR AA"),
    ("RR", "medial", "کیڑا", "keera", "insect", "K II RR AA"),
    ("RR", "medial", "گھوڑا", "ghora", "horse", "G_H OO RR AA"),
    ("RR", "medial", "ٹکڑا", "tukra", "piece", "TT U K RR AA"),
    ("RR", "medial", "جھاڑو", "jhaaroo", "broom", "D_ZZ_H AA RR OO"),
    ("RR", "medial", "لڑکی", "larki", "girl", "L A RR K II"),
    ("RR", "medial", "سڑک", "sarak", "road", "S A RR A K"),
    ("RR", "final", "پہاڑ", "pahaar", "mountain", "P A H AA RR"),
    ("RR", "final", "بھیڑ", "bheer", "sheep", "B_H AE RR"),
    ("RR", "final", "جڑ", "jar", "root", "D_ZZ A RR"),

    # ---- T_SH (ch) ----
    ("T_SH", "initial", "چاند", "chaand", "moon", "T_SH AA N D_D"),
    ("T_SH", "initial", "چڑیا", "chiriya", "sparrow", "T_SH I RR J AA"),
    ("T_SH", "initial", "چابی", "chaabi", "key", "T_SH AA B II"),
    ("T_SH", "initial", "چار", "chaar", "four", "T_SH AA R"),
    ("T_SH", "medial", "اچار", "achaar", "pickle", "A T_SH AA R"),
    ("T_SH", "medial", "کچا", "kacha", "raw", "K A T_SH AA"),
    ("T_SH", "medial", "سچا", "sacha", "true", "S A T_SH AA"),
    ("T_SH", "final", "پانچ", "paanch", "five", "P AA N T_SH"),
    ("T_SH", "final", "کانچ", "kaanch", "glass", "K AA N T_SH"),
    ("T_SH", "final", "پیچ", "pech", "screw", "P AE T_SH"),

    # ---- D_ZZ (j) ----
    ("D_ZZ", "initial", "جوتا", "joota", "shoe", "D_ZZ UU T_D AA"),
    ("D_ZZ", "initial", "جہاز", "jahaaz", "aeroplane", "D_ZZ A H AA Z"),
    ("D_ZZ", "initial", "جال", "jaal", "net", "D_ZZ AA L"),
    ("D_ZZ", "initial", "جانور", "jaanwar", "animal", "D_ZZ AA N V A R"),
    ("D_ZZ", "medial", "کاجو", "kaaju", "cashew", "K AA D_ZZ UU"),
    ("D_ZZ", "medial", "گاجر", "gaajar", "carrot", "G AA D_ZZ A R"),
    ("D_ZZ", "medial", "پنجرہ", "pinjra", "cage", "P I N D_ZZ A R AA"),
    ("D_ZZ", "final", "تاج", "taaj", "crown", "T_D AA D_ZZ"),
    ("D_ZZ", "final", "اناج", "anaaj", "grain", "A N AA D_ZZ"),
    ("D_ZZ", "final", "بیج", "beej", "seed", "B II D_ZZ"),

    # ---- TT (retroflex t) ----
    ("TT", "initial", "ٹوپی", "topi", "cap", "TT OO P II"),
    ("TT", "initial", "ٹماٹر", "tamatar", "tomato", "TT A M AA TT A R"),
    ("TT", "initial", "ٹیلا", "tela", "hill", "TT AE L AA"),
    ("TT", "initial", "ٹانگ", "taang", "leg", "TT AA NG"),
    ("TT", "medial", "آٹا", "aata", "flour", "AA TT AA"),
    ("TT", "medial", "بٹن", "batan", "button", "B A TT A N"),
    ("TT", "medial", "چٹنی", "chatni", "chutney", "T_SH A TT N II"),
    ("TT", "final", "نوٹ", "note", "banknote", "N OO TT"),
    ("TT", "final", "کوٹ", "coat", "coat", "K OO TT"),
    ("TT", "final", "پلیٹ", "plate", "plate", "P L AE TT"),

    # ---- DD (retroflex d) ----
    ("DD", "initial", "ڈاکٹر", "doctor", "doctor", "DD AA K TT A R"),
    ("DD", "initial", "ڈنڈا", "danda", "stick", "DD A N DD AA"),
    ("DD", "initial", "ڈور", "dor", "string", "DD OO R"),
    ("DD", "initial", "ڈالی", "daali", "branch", "DD AA L II"),
    ("DD", "medial", "انڈا", "anda", "egg", "A N DD AA"),
    ("DD", "medial", "مینڈک", "maindak", "frog", "M AEN DD A K"),
    ("DD", "medial", "ہانڈی", "haandi", "cooking pot", "H AA N DD II"),
    ("DD", "final", "کارڈ", "card", "card", "K AA R DD"),
    ("DD", "final", "گارڈ", "guard", "guard", "G AA R DD"),
    ("DD", "final", "ٹھنڈ", "thand", "cold weather", "TT_H A N DD"),

    # ---- X (kh, velar fricative) ----
    ("X", "initial", "خرگوش", "khargosh", "rabbit", "X A R G OO SH"),
    ("X", "initial", "خیمہ", "khema", "tent", "X AE M AA"),
    ("X", "initial", "خالہ", "khaala", "maternal aunt", "X AA L AA"),
    ("X", "initial", "خوشبو", "khushbu", "fragrance", "X U SH B UU"),
    ("X", "medial", "بخار", "bukhaar", "fever", "B U X AA R"),
    ("X", "medial", "سخت", "sakht", "hard", "S A X T_D"),
    ("X", "medial", "اخبار", "akhbaar", "newspaper", "A X B AA R"),
    ("X", "final", "شاخ", "shaakh", "branch", "SH AA X"),
    ("X", "final", "تاریخ", "taareekh", "date", "T_D AA R II X"),
    ("X", "final", "سرخ", "surkh", "red", "S U R X"),
]