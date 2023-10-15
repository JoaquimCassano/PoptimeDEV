import ocrspace, openai
from typing import Literal
from gradio_client import Client
import json ; secrets = json.load(open('secrets.json'))
api = ocrspace.API(api_key=secrets['ocrspace'])

openai.api_base = "https://api.naga.ac/v1"

def Describe(url:str) -> tuple[str, str, str]:
    """
    Generates a description of an image and performs OCR on the given URL.

    Args:
        url (str): The URL of the image to be described.

    Returns:
        tuple[str, str, str]: A tuple containing the generated caption for the image, the extracted text from OCR, and the URL of the image.
    """
    DESCRIBING_MODEL = "https://soumnerd-blip-image-captioning-large-space.hf.space/"

    def describeIMG():

        client = Client(DESCRIBING_MODEL, verbose=False)
        result = client.predict(
                        url,	# str (filepath or URL to image) in '请选择一张图片' Image component
                        api_name="/predict"
        )
        return result
    caption = describeIMG()
    text = api.ocr_url(url)
    return (caption, text, url)

def AiResponse(messages:list, model:Literal["gpt-3.5-turbo-0613", "gpt-4", "gpt-4-32k", "gpt-3.5-turbo-16k"]) -> str: # type: ignore
    openai.api_key = secrets["naga"]
    resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
    )
    return resp['choices'][0]['message']['content'] # type: ignore

    


if __name__ == "__main__":
    print(Describe('https://pbs.twimg.com/media/F64BSE7W8AABYON.jpg'))
    
    print(AiResponse(
        model="gpt-3.5-turbo-16k",
        messages=  [
    {"role":"user", "content":"""Vamos imaginar que você é o back-end de um bot de twitter, mais especificamente um bot de fofocas para um grupo de amigos programadores, chamado "choqueidabolha". Você receberá diversos tweets da sua timeline, e irá analisar quando temos 'tretas'. Quando tivermos tretas, você irá criar um tweet noticiando a mesma. Como sabemos que você não tem capacidade de ver imagens, você sempre receberá uma tupla invés delas.  A tupla tem respectivamente: a descrição da imagem, todo o texto nela (via ocr), e por útlimo o url dela. 
     Como você é o back-end, suas respostas precisam ser muito específicas e precisas. Sua resposta pode ser exatamente "pass", caso não tenha nenhuma treta e nada de interessante pra postar, ou o seguinte json, para fazer o post:
     {
        "text":"🚨 TRETA: srProgrammer critica arquitetos de software, dizendo não serem programadores de verdade.",
        "medias":["https://pbs.twimg.com/media/F64BSE7W8AABYON.jpg"]

     },

     Explicando o json acima: Text é o texto do tweet, e medias um array com os urls das imagens. 
        Abaixo, segue um texto com as personalidades das principais pessoas da bolha dev, que você irá participar e receber tweets:
     
     - @onlyanerd2: Criador da choqueidabolha, é um dev python back-end de 13 anos, engraçado, porém meio da paz, não se mete muito em tretas.
     - @pedroperegrinaa : O bobo da corte. Costuma se meter muito em tretas, faz muitas piadas, e é amado por todos, por conta de suas piadas. Ele costuma fazer piadas relativamente pesadas, mas que todos concordam e gostam.
     - @ImNickGabe : Tem 18 anos, cabelo rosa, e é dev fullstack, focado em react native e typescript. Ele é amado por todos, e é grande amigo do pedro peregrina. Ele costuma ser relativamente da paz, e ama ajudar os outros. todos gostam dele por sua educação e empatia.
     - @lucianodiisouza: Conhecido como "o primo dev". Dev front-end, colecionador de teclados mecânicos, costuma ser "riquinho", mas é gente boa. Ele se mete muito em tretas.
     
     Lembre-se sempre de considerar as personalidades de cada um antes de anunciar algo. Por exemplo, um dev front-end como o lucianodiisouza não criticaria devs front-end
     
     Caso tenhamos tweets maneiros, como threads etc. Também vale a pena postar, para ajudar a engajar. Nesses casos, coloque o link do tweet no conteúdo do post. Mas só fale de threads sobre programação
     Por favor, considere tudo isso dito acima, é importantíssimo que você obedeça rigorosamente a essas regras.
    Gere somente um twet
     
    Por favor, raciocine antes de postar. Evite inventar informações que não estiverem explícitas em alguma parte do json. Você consegue, leve o tempo que precisar.     
    Em caso de nenhuma treta ou algo interessante:
        Resposta ruim, que você NUNCA DEVE REPLICAR:
            "Pass, não há nenhum tweet"
        Resposta boa, que você deve usar:
            "pass"
        Siga exatamente as regras. Lembre que você é um back-end pra um software, e não queremos quebrar toda a produção

     
     Lembre que o tweet precisam ser muito curtos. frases pequenas
     Nunca faça mais de um post da mesma treta. Tretas já comentadas, portanto NÃO POSTE SOBRE O QUE ESTÁ A SEGUIR:

     """},
    {"role":"assistant", "content":"Eu entendi. Vou seguir tudo citado acima, exatamente como você deseja. Ou seja, não postarei sobre as tretas que eu mesmo já postei, não inventarei tretas sem sentido, e não farei posts sem sentido (como um post que diz que o lucianodiisouza criticou devs front-end, já que ele é front-end). Além disso, sei que tudo isso é um grupo de amigos e palavrões e piadas pesadas são algo comum, que não é absurdo e não deve ser noticiado. Por favor, me envie o json da timeline para que eu possa ou não gerar um tweet, sempre seguindo o json, ou mandando somente 'pass'"},
    {"role":"user", "content":r"[{'id': '1712746470061797582', 'text': 'Coisas que eu NÃO entendo: shows fora da praia \n\nTipo ????? Como que termina um show sem tirar foto do nascer do sol???? https://t.co/Mw6LEa7Guz', 'author': '@pedroperegrinaa', 'medias': [('people are standing in front of a stage with a crowd of people', '', 'https://pbs.twimg.com/media/F8Tl1NIWYAAuKd4.jpg'), ('people walking on the beach at sunset with a few people standing on the sand', '', 'https://pbs.twimg.com/media/F8Tl1NIXQAAip4M.jpg')], 'url': 'https://twitter.com/pedroperegrinaa/status/1712746470061797582'}, {'id': '1712655218138046680', 'text': 'não tinha Bis naquela época ... (não aguentei, sorry kkkk)', 'author': '@AkitaOnRails', 'medias': [], 'url': 'https://twitter.com/AkitaOnRails/status/1712655218138046680'}, {'id': '1712452203053449687', 'text': 'só não entendi o “1 ano de garantia grátis”\n\ncarro usado comprado da localiza não tem garantia??\n\n(desculpa, nao entendo de carros, nunca gostei) https://t.co/jyhAJBMkug', 'author': '@lucianodiisouza', 'medias': [('a close up of a text message from a person on a cell phone', 'Today, 09:01\r\nLOCALIZA SEMINOVOS: LOJAS\r\nABERTAS NO FERIADO c/ Transferencia\r\ngratis + BONUS troca/finan de 3MlL ou 1\r\nANO de garantia gratis. SO HOJE!!\r\nhttps/./bit.ly/3RaRdgg\r\n', 'https://pbs.twimg.com/media/F8PaM1UWcAADzec.jpg')], 'url': 'https://twitter.com/lucianodiisouza/status/1712452203053449687'}, {'id': '1712774916682973679', 'text': 'Sex to u\n\nSextouuuuu', 'author': '@programador_who', 'medias': [], 'url': 'https://twitter.com/programador_who/status/1712774916682973679'}, {'id': '1712695523398885779', 'text': '🚨GRAVE: Homem ameaça dois pescadores que invadiram sua propriedade para pescar no seu lago.\n\nO vídeo rapidamente viralizou nas redes sociais e dividiu opiniões. https://t.co/YTHXwRajQg', 'author': '@diretodomiolo', 'medias': [], 'url': 'https://twitter.com/diretodomiolo/status/1712695523398885779'}, {'id': '1712786403321389414', 'text': 'muito bom TER UM CELULAR p registrar momentos, amo rever os vídeos do Menos é Mais, achar que o cara não tá vivendo o momento por não gravar o rolê é pensamento de velho chato', 'author': '@danielvieiraarr', 'medias': [], 'url': 'https://twitter.com/danielvieiraarr/status/1712786403321389414'}, {'id': '1712776206787940561', 'text': 'Faço isso com meu celular também \nSó tirar o carro do canto.', 'author': '@programador_who', 'medias': [], 'url': 'https://twitter.com/programador_who/status/1712776206787940561'}, {'id': '1712548078711099517', 'text': 'Na Sky News, o ex-PM israelense Naftali Bennett foi questionado pelo jornalista: \n- E quanto aos bebês nas incubadoras em Gaza, cujo suporte foi desligado porque os israelitas cortaram a energia?\nBennett : Você está perguntando sobre os civis palestinos? Qual o seu problema?', 'author': '@UrbanNathalia', 'medias': [], 'url': 'https://twitter.com/UrbanNathalia/status/1712548078711099517'}, {'id': '1712796227069223296', 'text': 'Não ligo de esperar 2s pro meu Gmail carregar não.', 'author': '@raisi_exception', 'medias': [], 'url': 'https://twitter.com/raisi_exception/status/1712796227069223296'}, {'id': '1712782930626388143', 'text': 'erika vc é a mãe que eu nunca tive \U0001faf6\U0001faf6', 'author': '@agustvick', 'medias': [], 'url': 'https://twitter.com/agustvick/status/1712782930626388143'}, {'id': '1712664757335908621', 'text': 'Passando pra lembrar a todos que NÃO olhem diretamente pro Sol durante o eclipse!\n\nO que pode:\n✅ óculos especial para eclipse\n✅ vidro de soldador >14\n✅ telescópio com filtro solar\n\nO que não pode:\n❌ óculos de sol\n❌ chapa de raio x\n❌ filme fotográfico https://t.co/UeRrsPyXIK', 'author': '@astroaline', 'medias': [('texts written in spanish and english are displayed on a table', 'Esse eclipse ai é amanhä?\r\n21:29\r\n21:33\r\nPode olhar de oculos escuros meia\r\nboca? Rsrs\r\nsåbado\r\n21:32 u\r\nNÄo\r\n21:33 u\r\npelo amor de deus\r\n', 'https://pbs.twimg.com/media/F8SbhBQX0AAAJln.jpg')], 'url': 'https://twitter.com/astroaline/status/1712664757335908621'}]"}
]
    ))