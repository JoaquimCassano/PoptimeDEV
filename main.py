import twitter, ai, time, json
from tweety.types import Tweet

log = [
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
    {"role":"assistant", "content":"Eu entendi. Vou seguir tudo citado acima, exatamente como você deseja. Ou seja, não postarei sobre as tretas que eu mesmo já postei, não inventarei tretas sem sentido, e não farei posts sem sentido (como um post que diz que o lucianodiisouza criticou devs front-end, já que ele é front-end). Além disso, sei que tudo isso é um grupo de amigos e palavrões e piadas pesadas são algo comum, que não é absurdo e não deve ser noticiado. Por favor, me envie o json da timeline para que eu possa ou não gerar um tweet, sempre seguindo o json, ou mandando somente 'pass'"}
]

for index, i in enumerate(twitter.app.get_tweets("poptimedev")):
    if index > 10:
        break
    if type(i) == Tweet:
        log[0]['content'] += f'\n {i.text}' # type: ignore

def main():
    while True:
        tl = twitter.TimeLine()
        formatted_tl = []
        for index, tweet in enumerate(tl):
            if index > 10:
                break
            medias = []
            for media in tweet.media:
                if media.type == "photo":
                    medias.append(ai.Describe(media.media_url_https))
            formatted_tl.append({"id":tweet.id, "text":tweet.text, "author":f'@{tweet.author.username}', "medias":medias, "url": tweet.url})
        print(formatted_tl)
        log.append({"role":"user", "content":str(formatted_tl)})
        response = ai.AiResponse(log, model="gpt-3.5-turbo-16k")
        print(response)
        log.append({"role":"assistant", "content":response})
        if response.lower().lstrip() not in ["pass", '"pass"']:
            data = json.loads(response)
            confirm = input("Postar? [y/n]")
            if confirm.lower().strip() == "y":
                if type(data) == list:
                    for tweet in data:
                        print(twitter.Post(tweet["text"], tweet["medias"]))
                else:
                    print(twitter.Post(data["text"] , data['medias']))
        time.sleep(90)

if __name__ == "__main__":
    main()