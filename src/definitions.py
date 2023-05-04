from enum import Enum

# ディレクトリ定義
WORK_DIR = "/workdir"
INIT_DIR = f"{WORK_DIR}/init"

# stat.ink 統計情報ダウンロード URL などの定義
STATINK_DOWNLOAD_BASE_URL = "https://dl-stats.stats.ink"
STATINK_DOWNLOAD_BATTLE_PATH = "/splatoon-3/battle-results-csv/"
STATINK_DOWNLOAD_BATTLE_ZIP_URL = (
    f"{STATINK_DOWNLOAD_BASE_URL}{STATINK_DOWNLOAD_BATTLE_PATH}battle-results-csv.zip"
)


class Lobby(Enum):
    REGULAR = "regular"
    BANKARA_OPEN = "bankara_open"
    BANKARA_CHALLENGE = "bankara_challenge"
    XMATCH = "xmatch"
    SPLATFEST_OPEN = "splatfest_open"
    SPLATFEST_CHALLENGE = "splatfest_challenge"


class Mode(Enum):
    NAWABARI = "nawabari"
    AREA = "area"
    YAGURA = "yagura"
    HOKO = "hoko"
    ASARI = "asari"


MODE_ORDER = [Mode.AREA.value, Mode.YAGURA.value, Mode.HOKO.value, Mode.ASARI.value]


class Stage(Enum):
    KINMEDAI = "kinmedai"
    KUSAYA = "kusaya"
    GONZUI = "gonzui"
    ZATOU = "zatou"
    SUMESHI = "sumeshi"
    CHOZAME = "chozame"
    NAMERO = "namero"
    NAMPLA = "nampla"
    HIRAME = "hirame"
    MASABA = "masaba"
    MATEGAI = "mategai"
    MAHIMAHI = "mahimahi"
    MANTA = "manta"
    YAGARA = "yagara"
    YUNOHANA = "yunohana"
    AMABI = "amabi"


STAGE_ORDER = [
    Stage.KINMEDAI.value,
    Stage.KUSAYA.value,
    Stage.GONZUI.value,
    Stage.ZATOU.value,
    Stage.SUMESHI.value,
    Stage.CHOZAME.value,
    Stage.NAMERO.value,
    Stage.NAMPLA.value,
    Stage.HIRAME.value,
    Stage.MASABA.value,
    Stage.MATEGAI.value,
    Stage.MAHIMAHI.value,
    Stage.MANTA.value,
    Stage.YAGARA.value,
    Stage.YUNOHANA.value,
    Stage.AMABI.value,
]


COLOR_PAIR_ORDER = [
    "#343bc4-#df6624",
    "#1a1aaf-#e38d24",
    "#3a0ccd-#d0bf08",
    "#6325cd-#bfcd41",
    "#6e04b6-#cd510a",
    "#9025c6-#cfb121",
    "#ba30b0-#a0c937",
    "#c12d74-#2cb721",
    "#c43a6e-#1bbfab",
    "#d74b31-#1ec0ad",
]
