import streamlit as st
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="MCQ Test App", layout="wide")

# -----------------------------
# QUESTIONS (EDIT HERE)
# -----------------------------
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
        "answer": 1
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": 1
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "Java", "HTML", "All"],
        "answer": 3
    },
    {
        "question": "Sun rises from?",
        "options": ["West", "East", "North", "South"],
        "answer": 1
    },
    {
        "question": "Which is a programming language?",
        "options": ["Python", "Snake", "Lion", "Tiger"],
        "answer": 0
    },
    {
        "question": "Which is fastest?",
        "options": ["Car", "Bike", "Plane", "Bus"],
        "answer": 2
    },
    {
        "question": "Which is fruit?",
        "options": ["Carrot", "Potato", "Apple", "Onion"],
        "answer": 2
    },
    {
        "question": "HTML stands for?",
        "options": [
            "Hyper Text Markup Language",
            "High Text Machine Language",
            "Hyper Tool Multi Language",
            "None"
        ],
        "answer": 0
    },
    {
        "question": "CSS is used for?",
        "options": ["Logic", "Styling", "Database", "Backend"],
        "answer": 1
    },
    {
        "question": "Python is?",
        "options": ["Snake", "Language", "Animal", "Bird"],
        "answer": 1
    }
]

TOTAL_QUESTIONS = len(questions)

# -----------------------------
# SESSION STATE
# -----------------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.answers = [-1] * TOTAL_QUESTIONS
    st.session_state.marked = [False] * TOTAL_QUESTIONS
    st.session_state.start_time = time.time()
    st.session_state.submitted = False

# -----------------------------
# TIMER
# -----------------------------
elapsed = int(time.time() - st.session_state.start_time)
minutes = elapsed // 60
seconds = elapsed % 60

st.title("📝 MCQ Test App")

col1, col2 = st.columns([8, 2])
with col2:
    st.metric("⏱ Time", f"{minutes}:{seconds:02d}")

# -----------------------------
# SIDEBAR PALETTE
# -----------------------------
st.sidebar.title("📊 Question Palette")

for i in range(TOTAL_QUESTIONS):
    color = "🟢" if st.session_state.answers[i] != -1 else "⚪"
    if st.session_state.marked[i]:
        color = "🟡"

    if st.sidebar.button(f"{color} Q{i+1}", key=f"q{i}"):
        st.session_state.current_q = i

# -----------------------------
# MAIN QUESTION
# -----------------------------
if not st.session_state.submitted:

    q_idx = st.session_state.current_q
    q = questions[q_idx]

    st.subheader(f"Question {q_idx + 1}/{TOTAL_QUESTIONS}")
    st.write(q["question"])

    selected = st.radio(
        "Choose your answer:",
        q["options"],
        index=st.session_state.answers[q_idx]
        if st.session_state.answers[q_idx] != -1 else 0,
        key=f"radio_{q_idx}"
    )

    # Save answer
    st.session_state.answers[q_idx] = q["options"].index(selected)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Previous") and q_idx > 0:
            st.session_state.current_q -= 1

    with col2:
        if st.button("Mark for Review"):
            st.session_state.marked[q_idx] = not st.session_state.marked[q_idx]

    with col3:
        if st.button("Next ➡") and q_idx < TOTAL_QUESTIONS - 1:
            st.session_state.current_q += 1

    st.divider()

    if st.button("🚀 Submit Test"):
        st.session_state.submitted = True

# -----------------------------
# RESULT PAGE
# -----------------------------
else:
    st.header("📊 Test Result")

    score = 0
    for i, q in enumerate(questions):
        if st.session_state.answers[i] == q["answer"]:
            score += 1

    st.success(f"Your Score: {score}/{TOTAL_QUESTIONS}")

    st.subheader("📋 Detailed Report")

    for i, q in enumerate(questions):
        user_ans = st.session_state.answers[i]
        correct_ans = q["answer"]

        if user_ans == correct_ans:
            st.write(f"✅ Q{i+1}: Correct")
        else:
            st.write(
                f"❌ Q{i+1}: Wrong | Correct: {q['options'][correct_ans]}"
            )

    st.divider()

    # Stats
    attempted = sum([1 for a in st.session_state.answers if a != -1])
    marked = sum(st.session_state.marked)

    st.write(f"Attempted: {attempted}")
    st.write(f"Marked for Review: {marked}")
    st.write(f"Unattempted: {TOTAL_QUESTIONS - attempted}")
