## Documentação do código do app My Polyglot

Este código Python utiliza a biblioteca `streamlit` para criar uma aplicação web interativa chamada \"My Polyglot\", com o objetivo de auxiliar no aprendizado de línguas. O programa utiliza o modelo de linguagem grande `Gemini` da Google AI para processar texto e áudio, oferecendo recursos de tradução, correção gramatical e avaliação de pronúncia. 

**Vamos analisar o código por partes:**

### Arquivo main.py

* **Importações:** O código inicia importando as bibliotecas necessárias, incluindo `streamlit` para a interface, `audio_recorder_streamlit` para gravação de áudio, `google.generativeai` para interagir com o modelo Gemini, `gTTS` para conversão de texto em fala e `settings` para configurações de idiomas e segurança. 

* **Configurações:** Define a chave da API para acesso ao modelo Gemini e configurações de segurança para evitar conteúdo inadequado. 

* **Remoção de arquivos:** Elimina arquivos de áudio existentes para evitar conflitos.

* **Funções:**
    * **`remove_files`:** Elimina arquivos de áudio existentes para evitar conflitos.
    * **`generate_random_phrase`:** Recebe o idioma desejado e gera uma curta frase usando o Gemini para ser utilizada no check de pronúncia.
    * **`transcribe_audio_to_text`:** Recebe um arquivo de áudio e o idioma/sotaque, transcreve o áudio em texto usando o Gemini e realiza uma avaliação da pronúncia, identificando erros e sugerindo recursos de estudo.
    * **`fix_writing`:** Recebe um texto e o idioma/sotaque, corrige erros gramaticais e explica as alterações realizadas, considerando a gramática do idioma escolhido.
    * **`convert_text_to_audio`:** Recebe um texto, o idioma de origem e o idioma/sotaque desejado, traduz o texto usando o Gemini e converte o texto traduzido em áudio utilizando o gTTS.

* **Função `main`:**
    * Configura a página do Streamlit com o título \"My Polyglot\" e layout amplo.
    * Cria uma barra lateral com informações sobre o aplicativo e seus recursos.
    * Permite ao usuário selecionar o idioma que deseja aperfeiçoar.
    * Cria três abas:
        * **Aba \"Escrita\":** Permite ao usuário inserir um texto e receber correções gramaticais com explicações.
        * **Aba \"Escuta\":** Permite ao usuário digitar um texto e ouvir a tradução falada no idioma e sotaque desejados.
        * **Aba \"Pronúncia\":** Permite ao usuário gravar sua voz falando no idioma que está aprendendo e receber feedback sobre sua pronúncia, com sugestões de melhoria.

### Arquivo settings.py

* **`safety_settings`:** Define parâmetros de segurança para bloquear conteúdo inadequado gerado pelo modelo Gemini. 
* **`dict_languages`:** Define um dicionário com os idiomas e sotaques suportados pelo aplicativo, incluindo parâmetros para o gTTS.
