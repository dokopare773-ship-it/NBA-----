import streamlit as st
st.set_page_config(
    page_title="NBA参加者名簿",
    page_icon="✨",
    layout="centered"
)

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

members = st.session_state.members

total_members = sum(1 for member in members if member["name"])
new_members = sum(1 for member in members if member["name"] and member["new"])

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric("👥 参加者", f"{total_members}名 / 30名")

with col2:
    st.metric("🟡 新規", f"{new_members}名")

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
        if st.button("💾 保存", key=f"save_{i}"):
                st.session_state.members[i] = {
                    "name": name.strip(),
                    "new": is_new,
                    "introducer": introducer.strip()
                }
                st.success("保存しました")
                st.rerun()
                if member["name"]:
                    if st.button("🗑️ この参加者を削除", key=f"delete_{i}"):
                        st.session_state.members[i] = {
                            "name": "",
                            "new": False,
                            "introducer": ""
                        }
                        st.rerun()