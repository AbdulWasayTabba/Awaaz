import uuid
from typing import Optional

from pydantic import BaseModel


class Sound_Out(BaseModel):
    code: str                      # CISAMPA code, e.g. "K"
    ipa: str                       # e.g. "k"
    manner: Optional[str] = None   # stop, fricative, ...
    item_count: int               # how many published practice items target it


class Item_Out(BaseModel):
    id: uuid.UUID
    text: str                      # Urdu script
    transliteration: str
    gloss: Optional[str] = None    # English meaning
    ipa: str                       # space-separated phones
    tier: str                      # sound | word | sentence
    position: str                  # initial | medial | final
    sound: str                     # CISAMPA code of the target sound
    sound_ipa: str