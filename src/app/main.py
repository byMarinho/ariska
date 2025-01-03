import requests
import streamlit as st

from api.core import config
from api.services.utility import FileMedia

API = config.ARISKA_API

st.set_page_config(
    page_title="Ariska",
    page_icon=":wolf:",
    layout="wide",
    initial_sidebar_state="auto",
)

# ocultar menu padrão do streamlit
hide_menu = """
    <style> 
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        #stDecoration {display:none;}
    </style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

# footer personalizado
footer_html = """
    <style>
        a:link , a:visited{
            color: white;
            background-color: transparent;
            text-decoration: underline;
        }

        a:hover,  a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
        }

        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0E1117;
            color: white;
            text-align: center;
        }
    </style>

    <div class="footer">
        <p><a href="http://localhost:8000/" target="_blank">API Integração</a> - <a href="mailto:me@bymario.dev" target="_blank">Contato</a> - <a href="https://github.com/byMarinho/ariska" target="_blank">Projeto Github</a></p>
        <p>Copyright 2024 | Desenvolvido com ❤️ <a href="https://github.com/byMarinho" target="_blank">byMario.dev</a></p>
    </div>    
"""

st.write("Baixe um arquivo ou playlist de músicas (mp3) ou vídeos (mp4) do Youtube")
st.title(":wolf: Ariska App")
st.subheader("Rápido e fácil...")

url = st.text_input(
    "Cole a URL do vídeo aqui",
    placeholder="https://www.youtube.com/watch?v=...",
    autocomplete="on",
)

if url:
    col1, col2 = st.columns([1, 3], vertical_alignment="bottom", gap="small")
    typeMedia = col1.selectbox("Tipo de Arquivo", ("Selecione", "Áudio", "Vídeo"))
    playlist = col2.toggle(
        label="Playlist", help="Ativar se o link for de uma playlist do youtube."
    )

    col3, col4 = st.columns([1, 3], vertical_alignment="bottom", gap="small")
    if typeMedia == "Áudio" or typeMedia == "Vídeo":
        resp = requests.get(API + "/resolutions?url=" + url)
        res = resp.json()

        if resp.status_code == 200:
            resolutions = (
                sorted(res["audio_resolutions"])
                if typeMedia == "Áudio"
                else sorted(res["video_resolutions"])
            )
            resolution = col3.selectbox("Escolha a Resolução", (resolutions))
        else:
            # TODO: Tratar melhor a mensagem de erro
            st.error("Error...", "Falha ao Obter Resoluções do Vídeo")

        if col4.button("Download"):
            with st.spinner("É rapidinho, já estamos trabalhando..."):
                try:
                    typeDownload = "audio" if typeMedia == "Áudio" else "video"
                    msgButton = (
                        "Baixar Mp3 da Música"
                        if typeMedia == "Áudio"
                        else "Baixar Mp4 do Vídeo"
                    )

                    if not playlist:
                        response = requests.get(
                            API
                            + "/download/"
                            + typeDownload
                            + "?url="
                            + url
                            + "&resolution="
                            + resolution
                        )
                        resStream = response.json()

                        if resStream["file"]["status_code"] == 200:
                            with open(resStream["file"]["path"], "rb") as midia:
                                st.download_button(
                                    f"{msgButton} - {resStream['title']}",
                                    file_name=f"{resStream['file']['filename']}",
                                    data=midia,
                                    mime=resStream["file"]["media_type"],
                                    type="primary",
                                    use_container_width=True,
                                )

                        clearStream = FileMedia()
                        clearStream.clearFile(resStream["file"]["path"])
                    elif playlist:
                        msgButtonPlaylist = (
                            "Baixar Playlist Mp3"
                            if typeMedia == "Áudio"
                            else "Baixar Playlist Mp4"
                        )

                        urplay, *listplay = url.split("&")
                        if not listplay:
                            st.toast(
                                "Esse link não é de uma playlist",
                                icon=":material/warning:",
                            )

                        playy = (
                            API
                            + "/download/playlist/"
                            + typeDownload
                            + "?url="
                            + urplay
                            + "&"
                            + listplay[0]
                            + "&resolution="
                            + resolution
                            + "&zip=true"
                        )
                        responsePlay = requests.get(playy)
                        playStream = responsePlay.json()

                        if playStream["file"]["status_code"] == 200:
                            with open(playStream["file"]["path"], "rb") as playMidia:
                                st.download_button(
                                    f"{msgButtonPlaylist} - {playStream['title']}",
                                    file_name=f"{playStream['file']['filename']}",
                                    data=playMidia,
                                    mime=playStream["file"]["media_type"],
                                    type="primary",
                                    use_container_width=True,
                                )

                        clearStream = FileMedia()
                        clearStream.clearFile(playStream["file"]["path"])
                    else:
                        # TODO: Tratar melhor a mensagem de erro
                        st.error("Erro ao baxar arquivo")
                except Exception as err:
                    # TODO: Tratar melhor a mensagem de erro
                    print(f"Ops... Não consegui processar esse link: {err}")

st.markdown(footer_html, unsafe_allow_html=True)
