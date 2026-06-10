import streamlit as st

try:
    import FSM
    st.write("FSM berhasil diimport")
    st.write(dir(FSM))
except Exception as e:
    st.error(f"ERROR: {type(e).__name__}: {e}")
