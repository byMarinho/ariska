import streamlit as st

from ariska import delmp3, movie2mp3, validurl

st.write("Baixe músicas (mp3) dos vídeos do youtube")
st.title(":wolf: Ariska App")
st.subheader("Rápido e fácil...")

url = st.text_input("Cole a URL do vídeo aqui")

if st.button("Processar"):
    if not validurl(url):
        st.error("Ops. O link que colou é inválido! Cola o correto (^_^)")
    else:
        with st.spinner("É rapidinho, já estamos trabalhando..."):
            try:
                response = movie2mp3(url)

                if response['message'] == 'success':
                    with open(response['file'], 'rb') as music:
                        st.download_button(
                            f"Baixar Mp3 da Música - {response['title']}",
                            file_name=f"{response['title']}.mp3",
                            data=music,
                            mime='audio/mp3'
                        )

                    delmp3(response['file'])
                else:
                    st.error(response['message'])
            except:
                st.error(
                    "Ops... Não consegui processar esse link. Tente outro, por favor!")
