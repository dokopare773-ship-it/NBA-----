import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="NBA参加者名簿",
    page_icon="✨",
    layout="centered"
)
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 900px;
}
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    h1 {
        font-size: 1.9rem !important;
    }
    h2, h3 {
        font-size: 1.25rem !important;
    }
    .stButton > button {
    width: 100%;
    min-height: 48px;
    background-color: #111111 !important;
    color: #ffffff !important;
    border: 2px solid #000000 !important;
    font-weight: 700 !important;
}
    input {
        font-size: 16px !important;
    }
}
.stApp {
    background-color: #FFD800 !important;
    color: #000000 !important;
}
.stCheckbox div.st-emotion-cache-bqwma9 {
    background-color: #ffffff !important;
    border: 2px solid #000000 !important;
}
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp div {
    color: #000000;
}

/* 参加者の入力欄 */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 2px solid #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* 参加者カード */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 2px solid #000000 !important;
}

/* 参加者カードの見出し */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary p {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 600 !important;
}

/* 開いた参加者カードの中 */
[data-testid="stExpanderDetails"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* ボタン */
.stButton > button {
    width: auto !important;
    min-width: 0 !important;
    min-height: 48px !important;
    background-color: #111111 !important;
    color: #FFFFFF !important;
    border: 2px solid #000000 !important;
}

/* ボタン内の文字も白 */
.stButton > button *,
.stButton > button p,
.stButton > button div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)
# ===== セミナーポスター設定 =====
st.subheader("🖼️ セミナーポスター")

poster_file = st.file_uploader(
    "新しいセミナーのポスターをアップロード",
    type=["png", "jpg", "jpeg"]
)

poster_bucket = supabase.storage.from_("seminar-posters")
poster_path = "current_poster"

if poster_file is not None:
    poster_bytes = poster_file.getvalue()

    existing_files = poster_bucket.list()
    poster_exists = any(
        item["name"] == poster_path
        for item in existing_files
    )

    if poster_exists:
        poster_bucket.update(
            poster_path,
            poster_bytes,
            {"content-type": poster_file.type}
        )
    else:
        poster_bucket.upload(
            poster_path,
            poster_bytes,
            {"content-type": poster_file.type}
        )

    st.success("ポスターを保存しました")

try:
    saved_poster = poster_bucket.download(poster_path)
    st.image(saved_poster, use_container_width=True)
except Exception:
    pass
def extract_limit_from_poster(image_bytes):
    import re
    from io import BytesIO
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter
    import pytesseract

    try:
        original = Image.open(BytesIO(image_bytes)).convert("RGB")
        w, h = original.size

        # ポスター全体＋複数エリアを読む
        regions = [
            original,                              # 全体
            original.crop((0, 0, w, h // 2)),     # 上半分
            original.crop((0, h // 2, w, h)),     # 下半分
            original.crop((0, 0, w // 2, h)),     # 左半分
            original.crop((w // 2, 0, w, h)),     # 右半分
            original.crop((w // 4, 0, 3*w // 4, h)),  # 中央縦
            original.crop((0, h // 4, w, 3*h // 4)),  # 中央横
        ]

        patterns = [
            r"(\d{1,3})名限定",
            r"限定(\d{1,3})名",
            r"(\d{1,3})名.{0,3}限定",
            r"限定.{0,3}(\d{1,3})名",
        ]

        for region in regions:
            # 3倍に拡大
            enlarged = region.resize(
                (region.width * 3, region.height * 3)
            )

            # 白黒化＋コントラスト強化
            gray = ImageOps.grayscale(enlarged)
            gray = ImageEnhance.Contrast(gray).enhance(2.5)
            gray = gray.filter(ImageFilter.SHARPEN)

            # 通常版と二値化版の両方を読む
            versions = [
                gray,
                gray.point(lambda x: 0 if x < 160 else 255, "1"),
            ]

            for img in versions:
                for psm in [6, 11, 12]:
                    text = pytesseract.image_to_string(
                        img,
                        lang="jpn+eng",
                        config=f"--psm {psm}"
                    )

                    normalized = (
                        text.replace(" ", "")
                            .replace("　", "")
                            .replace("\n", "")
                            .replace("１", "1")
                            .replace("２", "2")
                            .replace("３", "3")
                            .replace("４", "4")
                            .replace("５", "5")
                            .replace("６", "6")
                            .replace("７", "7")
                            .replace("８", "8")
                            .replace("９", "9")
                            .replace("０", "0")
                    )

                    for pattern in patterns:
                        match = re.search(pattern, normalized)
                        if match:
                            value = int(match.group(1))

                            # 現実的な参加上限だけ採用
                            if 1 <= value <= 100:
                                return value

    except Exception:
        pass

    # 読み取れなかった時だけ従来の30名
    return 30
initial_members = [
    {"name": "比嘉海輝", "new": False, "introducer": ""},
    {"name": "吉田富和", "new": False, "introducer": ""},
    {"name": "遠藤法子", "new": False, "introducer": ""},
    {"name": "謝花優", "new": False, "introducer": ""},
    {"name": "金武 美架", "new": True, "introducer": "新城めぐみ"},
    {"name": "伊芸 登美江", "new": True, "introducer": "新城めぐみ"},
    {"name": "新城 めぐみ", "new": False, "introducer": ""},
    {"name": "まえざとのりこ", "new": False, "introducer": ""},
    {"name": "宜名眞清悟", "new": False, "introducer": ""},
    {"name": "粟国龍之介", "new": True, "introducer": "宜名眞清悟"},
    {"name": "外間政一郎", "new": True, "introducer": "吉田富和"},
    {"name": "山本健蔵", "new": True, "introducer": "松島崇明・関塚知義"},
    {"name": "宮里翔子", "new": False, "introducer": ""},
    {"name": "関塚知義", "new": False, "introducer": ""},
    {"name": "宮城享美", "new": False, "introducer": ""},
    {"name": "宮城勇", "new": False, "introducer": ""},
    {"name": "松崎悟之", "new": False, "introducer": ""},
    {"name": "栗原繁", "new": True, "introducer": "吉田富和"},
    {"name": "砂川善考", "new": True, "introducer": "謝花優"},
    {"name": "下地隆貴", "new": False, "introducer": "遠藤法子"},
]
while len(initial_members) < 30:
    initial_members.append(
        {"name": "", "new": False, "introducer": ""}
    )
    if "members" not in st.session_state:
        st.session_state.members = initial_members.copy()
        rows = supabase.table("participants").select("*").order("slot_number").execute().data
        if rows:
            for row in rows:
                if row["slot_number"] is None:
                    continue
                slot = row["slot_number"] - 1
                if 0 <= slot < 30:
                    st.session_state.members[slot] = {
                        "name": row["name"],
                        "new": row["is_new"],
                        "introducer": row["introducer"] or ""
                        }
members = st.session_state.members

total_max_members = 30
if "saved_poster" in locals():
    max_members = extract_limit_from_poster(saved_poster)
    from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

debug_image = Image.open(BytesIO(saved_poster)).convert("RGB")
debug_image = debug_image.resize(
    (debug_image.width * 3, debug_image.height * 3)
)
debug_image = ImageOps.grayscale(debug_image)
debug_image = ImageEnhance.Contrast(debug_image).enhance(2.5)

debug_text = pytesseract.image_to_string(
    debug_image,
    lang="jpn+eng",
    config="--psm 11"
)

st.info(f"OCR読取結果：\n{debug_text}")
total_members = sum(1 for member in members if member["name"])
new_members = sum(1 for member in members if member["name"] and member["new"])

st.divider()

st.markdown(
    f'<div style="margin:10px 25px 0;">'
    f'<div style="font-size:22px;font-weight:700;color:#000000;">参加者</div>'
    f'<div style="margin-top:4px;white-space:nowrap;">'
    f'<span style="font-size:38px;font-weight:900;color:#ff0000;">限定 {total_members}名</span>'
    f'<span style="font-size:38px;font-weight:900;color:#000000;"> / {max_members}名</span>'
    f'<span style="font-size:20px;font-weight:900;color:#000000;"> 上限</span>'
    f'</div>'
    f'<div style="font-size:28px;font-weight:900;color:#000000;margin-top:2px;">'
    f'（新規 {new_members}名）'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)
empty_slot_shown = False
for i, member in enumerate(members):
    number = i + 1
    if not member["name"]:
        if empty_slot_shown:
            continue
        empty_slot_shown = True
    if member["name"]:
            label = f"{number}. {member['name']}"
            if member["new"]:
                label += " 🟡"
            if member["introducer"]:
                label += f"（{member['introducer']}）"
    else:
            label = f"{number}. ＋ 参加者を登録"

    with st.expander(label):
            name = st.text_input(
                "参加者名",
                value=member["name"],
                key=f"name_{i}_{st.session_state.get('form_version', 0)}"
            )

            is_new = st.checkbox(
                "🟡 新規参加者",
                value=member["new"],
                key=f"new_{i}_{st.session_state.get('form_version', 0)}"
            )

            introducer = st.text_input(
                "紹介者名",
                value=member["introducer"],
                key=f"introducer_{i}_{st.session_state.get('form_version', 0)}"
            )
            if st.session_state.members[i]["name"]:
                if st.button("🗑 この参加者を削除", key=f"delete_{i}"):

                    # 削除した参加者をリストから取り除き、後ろを自動で前へ詰める
                    st.session_state.members.pop(i)
                    st.session_state.form_version = st.session_state.get("form_version", 0) + 1
                    for j in range(i, len(st.session_state.members) + 1):
                        st.session_state.pop(f"name_{j}", None)
                        st.session_state.pop(f"new_{j}", None)
                        st.session_state.pop(f"introducer_{j}", None)
                    # 一番最後に新規登録用の空欄を1つ追加
                    st.session_state.members.append({
                        "name": "",
                        "new": False,
                        "introducer": ""
                    })

                    # 削除位置以降の番号をSupabase側でも振り直す
                    for j in range(i, len(st.session_state.members)):
                        member_data = st.session_state.members[j]

                        if member_data["name"]:
                            supabase.table("participants").upsert({
                                "slot_number": j + 1,
                                "name": member_data["name"],
                                "is_new": member_data["new"],
                                "introducer": member_data["introducer"]
                            }, on_conflict="slot_number").execute()
                        else:
                            supabase.table("participants").delete().eq(
                                "slot_number", j + 1
                            ).execute()

                    st.rerun()
            if st.button("💾 保存", key=f"save_{i}"):
                    st.session_state.members[i] = {
                        "name": name.strip(),
                        "new": is_new,
                        "introducer": introducer.strip()
                    }
                    st.success("保存しました")
                    supabase.table("participants").upsert({
                        "slot_number": i + 1,
                                        "name": name.strip(),
                                        "is_new": is_new,
                                        "introducer": introducer.strip()
                    }, on_conflict="slot_number").execute()
                    st.rerun()
                    