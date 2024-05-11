import streamlit as st
from audio_recorder_streamlit import audio_recorder
import google.generativeai as genai
from gtts import gTTS
import settings
import os

API_KEY = 'COLOQUE SUA API KEY AQUI'

genai.configure(api_key=API_KEY)

#removendo os arquivos iniciai
def remove_files():
    list_files_to_remove = ["my_app/pronunciation_audio.mp3","my_app/text_converted_to_audio.mp3"]
    for file_path in list_files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)


def generate_random_phrase(language_and_accent:str):
    generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=settings.safety_settings)

    language_treated = language_and_accent.split("-")[0] #pegando somente a lingua


    convo = model.start_chat(history=[])
    convo.send_message(f"""Gere uma frase curta aleatória em {language_treated}. Me envie SOMENTE a frase.""")
    response = convo.last.text

    return response


def transcribe_audio_to_text(speech_file_path: str, language_and_accent:str, random_phrase_to_check_pronunciation:str):
    ####
    # FUNCAO PARA CONVERTER AUDIO EM TEXTO E FAZER A AVALIACAO
    ####

    generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 2048,
    }
    system_instruction = "Voce é uma ferramenta focada em línguas, sua principal função avaliar a pronuncia de audios em diversas linguas diferentes"
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=settings.safety_settings)

    language_treated = language_and_accent.split("-")[0] #pegando somente a lingua


    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": [genai.upload_file("my_app/few_shot_pronunciation_error.mp3")]
    },
    {
        "role": "user",
    	"parts": [f"""question: Considerando o audio como "I saw a bird in his nest", avalie se a pronúncia  em {language_treated} está correta ou errada.
                       Siga os seguintes requerimentos:
                       - Transcreva os textos que estão com pronúncias erradas e explique o por quê.
                       - Analise somente as pronúncias das palavras na frase.

                       Me envie com a seguinte estrutura:
                       Avaliação da pronúncia em inglês:
                       trecho com erro: justificativa do erro"""]
    },
    {
        "role": "model",
        "parts": ["## Avaliação da pronúncia em inglês:\n\n**Trecho com erro:** \"a bird\".\n\n**Justificativa do erro:** A pronúncia de \"bird\" está incorreta. O usuário pronunciou a palavra como \"beard\", que soa como a palavra inglesa para barba. A pronúncia correta de \"bird\" soa como \"bərd\", com o som de \"e\" mais curto, como em \"bed\". \n\nPratique a diferença entre vogais curtas e longas em inglês. Isso pode ser feito através de exercícios de repetição e escuta de falantes nativos pronunciando as palavras corretamente."]   
    },
        {
        "role": "user",
        "parts": [genai.upload_file("my_app/few_shot_pronunciation_correct.mp3")]
    },
    {
        "role": "user",
    	"parts": [f"""question: Considerando o audio como "The quick brown fox jumps over the lazy dog.", avalie se a pronúncia  em {language_treated} está correta ou errada.
                       Siga os seguintes requerimentos:
                       - Transcreva os textos que estão com pronúncias erradas e explique o por quê.
                       - Analise somente as pronúncias das palavras na frase.

                       Me envie com a seguinte estrutura:
                       Avaliação da pronúncia em inglês:
                       trecho com erro: justificativa do erro"""]
    },
    {
        "role": "model",
        "parts": ["## Avaliação da pronúncia em inglês:\n\nA pronúncia da frase está correta, todas as palavras foram faladas no aúdio com uma boa pronúncia.\n\n"]   
    },
    {
        "role": "user",
        "parts": [genai.upload_file(speech_file_path)]
    }])
    
    convo.send_message(f"""question: Considerando o audio como "{random_phrase_to_check_pronunciation}", avalie se a pronúncia  em {language_treated} está correta ou errada.
                       Siga os seguintes requerimentos:
                       - Transcreva os textos que estão com pronúncias erradas e explique o por quê.
                       - Analise somente as pronúncias das palavras na frase.

                       Me envie com a seguinte estrutura:
                       Avaliação da pronúncia em inglês:
                       trecho com erro: justificativa do erro""")
    response = convo.last.text
    return response



def fix_writing(text_to_check: str, language_and_accent:str):
    ####
    # FUNCAO AJUSTAR TEXTOS ESCRITOS E TRADUZI-LOS
    ####
    generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 8048,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=settings.safety_settings)

    language_treated = language_and_accent.split("-")[0] #pegando somente a lingua

    convo = model.start_chat(history=[
                    {
                    "role": "user",
                    "parts": ["""Voce é uma ferramenta focada em línguas, sua principal função é traduzir e corrigir textos em diversas linguas diferentes. Corrija os erros gramaticais de {language_treated} no texto enviado e explique cada ajuste.\n
                       texto: My name are Claudio"""]
                    },
                    {
                    "role": "model",
                    "parts": ["O erro na sentença \"My name are Claudio\" é uma questão de concordância sujeito-verbo.  \n\n*   **\"My name\"** é um substantivo singular, portanto requer um verbo singular. \n*   **\"Are\"** é um verbo plural e deve ser substituído pelo verbo singular **\"is\"**.\n\nA frase correta deve ser: **\"My name is Claudio\"**"]
                    },
                    ]
                            )
    
    convo.send_message(f"""Voce é uma ferramenta focada em línguas, sua principal função é traduzir e corrigir textos em diversas linguas diferentes. Corrija os erros gramaticais de {language_treated} no texto enviado e explique cada ajuste.\n
                       texto: {text_to_check}""")
    response = convo.last.text
    # print(response)

    return response



def convert_text_to_audio(text_to_read_voice: str, language_text:str, language:str, accent:str):
    ####
    # FUNCAO PARA CONVERTER TEXTO PARA AUDIO
    ####

    generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 8048,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=settings.safety_settings)


    #comecando com few-shot
    convo = model.start_chat(history=[
                    {
                    "role": "user",
                    "parts": ["Você é uma ferramenta especialista em linguas e precisa responder ao usuário de forma didática.\n Traduza o texto para English.\n texto: Meu amigo é legal, gosto muito de sair com ele para as festas"]
                    },
                    {
                        "role": "model",
                        "parts": ["My friend is cool, I like so much to hang out with him to parties"]
                    }
                    ]
                            )
    
    convo.send_message(f"""Você é uma ferramenta especialista em linguas e precisa responder ao usuário de forma didática.
                       Traduza o texto para {language_text}.\n
                       texto: {text_to_read_voice}""")
    response = convo.last.text
    # print(response)

    file_text_converted_to_audio = "my_app/text_converted_to_audio.mp3"
    my_text_converted_to_audio = gTTS(text=response, lang=language, tld=accent, slow=False)
    my_text_converted_to_audio.save(file_text_converted_to_audio)

    return response, file_text_converted_to_audio


def main():
    st.set_page_config("My Polyglot 🌎", layout="wide")
    st.header("My Polyglot 🌎", divider=True)

    with st.sidebar:

        st.image("my_app/logo_my_polyglot_app.png")

        st.markdown("""
        ## Bem vindo ao *My Polyglot*.
        ## O seu assistente perfeito para ajudar a aprender novas línguas.
        ------------------------------------------
        ## Recursos
        * **Escrita:**
            * Insira um texto e receba correções gramaticais com explicações detalhadas.
            * Aprenda com seus erros e melhore sua escrita no idioma escolhido.
        * **Escuta:**
            * Digite um texto em seu idioma nativo e ouça a tradução falada no idioma e sotaque que você deseja aprender.
            * Familiarize-se com a pronúncia correta e a entonação natural do idioma.
        * **Pronúncia:**
            * Grave sua voz falando no idioma que está aprendendo.
            * Receba feedback sobre sua pronúncia, identificando erros e sugerindo pontos de melhoria.
            * Acesse links de estudo direcionados para aperfeiçoar sua pronúncia.
    """)
    
    #removendo arquivos remanescentes
    remove_files()

    option_language = st.selectbox("Qual língua você deseja aperfeiçoar?", tuple(set([x.split(" - ")[0] for x in settings.dict_languages.keys()])))

    tab_escrita, tab_escuta, tab_pronuncia = st.tabs(["Escrita", "Escuta", "Pronúncia"])


    with tab_escrita:
        text_to_check = None
        st.subheader("Vamos checar sua escrita, me envie um texto/frase e irei te ajudar com os erros gramaticais.")
        text_to_check = st.text_area("Escreva aqui seu texto/frase")
        if text_to_check:
            response = fix_writing(text_to_check = text_to_check, language_and_accent = option_language)
            st.divider()
            st.write(response)

    with tab_escuta:
        text_to_read_voice = None
        st.subheader("Precisa saber a tradução e pronúncia algo? O Polyglot pode ajudar você.")
        option_accent = st.selectbox("Você quer ouvir o sotaque de qual país?", tuple([lang.split(" - ")[1] for lang in settings.dict_languages.keys() if option_language in lang]))
        text_to_read_voice = st.text_input("Escreva aqui na sua língua nativa alguma tradução que deseja ouvir")
        if text_to_read_voice:
            language_and_accent = option_language + " - " + option_accent
            language = settings.dict_languages[language_and_accent]["language_param"]
            accent = settings.dict_languages[language_and_accent]["accent_param"]

            response, file_text_converted_to_audio = convert_text_to_audio(text_to_read_voice=text_to_read_voice, language_text = option_language, language = language, accent = accent)
            
            st.divider()
            st.markdown(response)
            st.audio(file_text_converted_to_audio, format="audio/mpeg")


    with tab_pronuncia:
        recorded_audio=None
        st.subheader("Vamos checar se sua pronúncia está boa?")
        generate_phrase_bt = st.button("Gere uma Frase")
    
        #Initialize session state
        if "generate_phrase_state" not in st.session_state:
            st.session_state.generate_phrase_state = ""

        recorded_audio = audio_recorder(pause_threshold=10000)

        if generate_phrase_bt:
            #removendo arquivos remanescentes
            remove_files()
            recorded_audio = None
            st.session_state.generate_phrase_state = generate_random_phrase(language_and_accent=option_language)
        
            st.write("Clique no microfone para mandar um audio falando a seguinte frase: \n" + "* " + st.session_state.generate_phrase_state)

        if recorded_audio:
            if generate_phrase_bt==False:
                st.write("Clique no microfone para mandar um audio falando a seguinte frase: \n" + "* " + st.session_state.generate_phrase_state)
            audio_file="my_app/pronunciation_audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)
            text = transcribe_audio_to_text(speech_file_path = audio_file, language_and_accent = option_language, random_phrase_to_check_pronunciation = st.session_state.generate_phrase_state)
            st.audio(audio_file, format="audio/mpeg")
            st.divider()
            st.write(text)
            generate_phrase_bt = None

if __name__== "__main__":
    main()