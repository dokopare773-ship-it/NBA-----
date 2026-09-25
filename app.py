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

if poster_file is not None:
    st.image(poster_file, caption="現在のセミナーポスター", use_container_width=True)
st.title("✨ NBA 新しい資産の作り方")
st.subheader("スペシャルゲスト　古賀 輔")

st.write("📅 9月25日(金)")
st.write("🕐 12:30受付 ／ 13:00開始（13:00〜15:30）")
st.write("📍 ビジネスセンター KEEP FRONT")
st.write("那覇市泊2丁目1−18 T&C泊ビル 4F 会議室")

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

total_members = sum(1 for member in members if member["name"])
new_members = sum(1 for member in members if member["name"] and member["new"])

st.divider()

st.markdown(f"""
<div style="margin: 10px 0 25px 0;">
    <div style="font-size: 22px; font-weight: 700; color: #000000;">
        👥 参加者
    </div>

    <div style="margin-top: 4px; white-space: nowrap;">
        <span style="font-size: 38px; font-weight: 900; color: #ff0000;">
            限定 {total_members}名
        </span>
        <span style="font-size: 38px; font-weight: 900; color: #000000;">
            / 30名
        </span>
        <span style="font-size: 20px; font-weight: 900; color: #000000;">
            上限
        </span>
    </div>

    <div style="font-size: 28px; font-weight: 900; color: #000000; margin-top: 2px;">
        （新規 {new_members}名）
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("参加者名簿")

for i, member in enumerate(members):
    number = i + 1

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
            key=f"name_{i}"
        )

        is_new = st.checkbox(
            "🟡 新規参加者",
            value=member["new"],
            key=f"new_{i}"
        )

        introducer = st.text_input(
            "紹介者名",
            value=member["introducer"],
            key=f"introducer_{i}"
        )
        if st.session_state.members[i]["name"]:
            if st.button("🗑️ この参加者を削除", key=f"delete_{i}"):
                st.session_state.members[i] = {
                    "name": "",
                    "new": False,
                    "introducer": ""
                }
                supabase.table("participants").delete().eq("slot_number", i + 1).execute()
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
                    