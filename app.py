import streamlit as st

st.set_page_config(page_title="Teste PLANAT", page_icon="✅")

st.title("✅ SISTEMA PLANAT 2026 - TESTE")
st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

if st.button("Clique aqui"):
    st.balloons()
    st.success("Funcionou!")