import streamlit as st
import time


def load_progress():
    try:
        with open("progress.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0


def save_progress(index):
    with open("progress.txt", "w") as f:
        f.write(str(index))

# ----------------------
# Daten laden
# ----------------------
with open("Nailslist_formated.txt", "r") as f:
    nails = [line.strip() for line in f if line.strip()]

total = len(nails)

# ----------------------
# Session State
# ----------------------
if "index" not in st.session_state:
    st.session_state.index = load_progress()

if "running" not in st.session_state:
    st.session_state.running = False

if "interval" not in st.session_state:
    st.session_state.interval = 5

if "show_reset_confirm" not in st.session_state:
    st.session_state.show_reset_confirm = False

i = st.session_state.index

# ----------------------
# Titel
# ----------------------
st.title("🧵 String Art Anleitung")

# ----------------------
# Fertig-Screen
# ----------------------
if i >= total - 1:
    st.success("🎉 Fertig! Dein String Art Werk ist abgeschlossen.")
    st.balloons()
    st.stop()

# ----------------------
# Anzeige letzter → aktueller → nächster
# ----------------------
st.markdown(
    f"""
    <div style="text-align:center; font-size:40px;">
        <span style="opacity:0.5">{nails[i]}</span>
        &nbsp;➡️&nbsp;
        <strong style="font-size:70px;">{nails[i+1]}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(f"Schritt {i+1} von {total}")

# ----------------------
# Fortschritt
# ----------------------
st.progress((i + 1) / total)

# ----------------------
# Manuelle Steuerung
# ----------------------
colA, colB, colC = st.columns(3)

with colA:
    if st.button("⬅ Zurück") and i > 0:
        st.session_state.running = False
        st.session_state.index -= 1
        save_progress(st.session_state.index)

with colB:
    if st.button("➡ Weiter"):
        st.session_state.running = False
        st.session_state.index += 1
        save_progress(st.session_state.index)

with colC:
    if st.button("🔄 Reset"):
        st.session_state.show_reset_confirm = True

# ----------------------
# Reset Bestätigung
# ----------------------
if st.session_state.show_reset_confirm:
    st.warning("Willst du wirklich von vorne anfangen?")
    colR1, colR2 = st.columns(2)

    with colR1:
        if st.button("Ja, Reset"):
            st.session_state.index = 0
            st.session_state.running = False
            st.session_state.show_reset_confirm = False

    with colR2:
        if st.button("Abbrechen"):
            st.session_state.show_reset_confirm = False

# ----------------------
# Direkt springen
# ----------------------
st.divider()
jump = st.number_input(
    "🔢 Zu Schritt springen",
    min_value=1,
    max_value=total,
    value=i + 1
)

if jump - 1 != i:
    st.session_state.running = False
    st.session_state.index = jump - 1

# ----------------------
# Timer
# ----------------------
st.divider()
st.subheader("⏱ Automatischer Timer")

st.session_state.interval = st.slider(
    "Sekunden pro Schritt",
    1, 30, st.session_state.interval
)

colT1, colT2 = st.columns(2)

with colT1:
    if st.button("▶ Start"):
        st.session_state.running = True

with colT2:
    if st.button("⏸ Pause"):
        st.session_state.running = False

# ----------------------
# Automatik
# ----------------------
if st.session_state.running:
    time.sleep(st.session_state.interval)
    st.session_state.index += 1
    save_progress(st.session_state.index)
    st.rerun()

