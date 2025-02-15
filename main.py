import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import requests 
import feedparser


# carrega o arquivo .env
load_dotenv()

# carrega a variável de ambiente
TOKEN = os.getenv("DISCORD_TOKEN")

# verifica se o valor do token foi carregado
if TOKEN is None:
    print("Erro: Token não encontrado no arquivo .env.")
    exit(1)  # encerra o programa se o token não for encontrado
else:
    print(f"Token carregado: {TOKEN[:10]}...")  # mostra os primeiros 10 caracteres do token para garantir que foi carregado

# definir intenções
intents = discord.Intents.all()
intents.message_content = True  # habilita a leitura do conteúdo das mensagens

# inicializar o bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado com sucesso: {bot.user}')
    print(f'Comandos registrados: {[command.name for command in bot.commands]}')


    #COMANDOS


# frame (chamar o bot)

@bot.command(name='frame')  # !frame para chamar o bot
async def sensei(ctx):
    print(f'Comando "frame" chamado por {ctx.author}')  # Log para depuração
    await ctx.send('coe mlk')  # envia uma mensagem de resposta


#info do bot

@bot.command(name='info')  # comando !info
async def info(ctx):
    print(f'Comando "info" chamado por {ctx.author}')  # log para depuração
    embed = discord.Embed(
        title='🤖 sobre nosso bot',
        description='menos complicado que entender *donnie darko*!',
        color=discord.Color.gold()
    )
    embed.add_field(
        name='📜 Comandos disponíveis',
        value=(
            "🎲 !filmealeatorio - receba um filme aleatório\n"
            "🔍 !ondeassistir [nome do filme] - saiba onde assistir\n"
            "🎭 !recomendar [gênero] - recomendações por gênero\n"
            "🍿 !filmedodia - filme do dia\n"
            "🎬 !diretor [nome do diretor] - filmes do diretor\n"
            "🧓 !classicos - classicos que marcaram o cinema"
        ),
        inline=False
    )
    embed.set_footer(text='💡 Criado por Juscelino Komecheka')  # rodapé
    embed.set_thumbnail(url="https://i.pinimg.com/736x/db/b4/5b/dbb45b29a717fbbbcf6efb2363a31ee7.jpg")  # Adicione um ícone do bot aqui
    await ctx.send(embed=embed)



# chave da API do TMDb
TMDB_API_KEY = "0baa0ee114deef8351cccc4438de961d"

# dicionário para armazenar o último filme recomendado para cada usuário
ultimos_filmes = {}


# filme aleatorio

@bot.command(name='filmealeatorio')
async def filmealeatorio(ctx):
    pagina_aleatoria = random.randint(1, 500)
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=pt-BR&sort_by=popularity.desc&include_adult=false&include_video=false&page={pagina_aleatoria}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        filmes = response.json()["results"]
        filme = random.choice(filmes)
        titulo = filme["title"]
        sinopse = filme["overview"] or "sinopse não disponível."
        poster = filme["poster_path"]
        link = f"https://www.themoviedb.org/movie/{filme['id']}"
        ano_lancamento = filme["release_date"].split("-")[0]
        nota = filme["vote_average"]
        link = f"https://www.themoviedb.org/movie/{filme['id']}"

        
        ultimos_filmes[ctx.author.id] = filme['id']

        embed = discord.Embed(
            title=f"🍿 filme Aleatório: **{titulo}**",
            description=f"🎥 *{sinopse}*",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{poster}")
        embed.add_field(name="🔗 mais informações", value=f"[Assista aqui]({link})", inline=False)
        embed.add_field(name="⭐ avaliação", value=f"{nota}/10", inline=True)
        embed.set_footer(text="🎬 indicação do dia!")
        await ctx.send(embed=embed)
    
    except Exception as e:
        print(f"Erro ao buscar filme: {e}")
        await ctx.send("🚫 não consegui encontrar um filme agora. tente novamente mais tarde!")




#COMANDO RECOMENDAR GENERO


# dicionário de gêneros (nome: id)
generos = {
    "ação": 28,
    "aventura": 12,
    "animação": 16,
    "comédia": 35,
    "crime": 80,
    "documentário": 99,
    "drama": 18,
    "família": 10751,
    "fantasia": 14,
    "história": 36,
    "terror": 27,
    "musical": 10402,
    "mistério": 9648,
    "romance": 10749,
    "ficção científica": 878,
    "thriller": 53,
    "guerra": 10752,
    "faroste": 37
}

@bot.command(name='recomendar')
async def recomendar(ctx, genero: str):
    # converte o gênero para minúsculas e remove espaços extras
    genero = genero.lower().strip()
    
    # verifica se o gênero é válido
    if genero not in generos:
        await ctx.send(f"Gênero inválido. Gêneros disponíveis: {', '.join(generos.keys())}")
        return
    
    # obtém o ID do gênero
    genero_id = generos[genero]
    
    # gera um número aleatório para a página (1 a 20)
    pagina_aleatoria = random.randint(1, 20)
    
    # URL para buscar filmes do gênero especificado
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=pt-BR&sort_by=popularity.desc&include_adult=false&include_video=false&page={pagina_aleatoria}&with_genres={genero_id}"
    
    try:
        # faz a requisição à API
        response = requests.get(url)
        response.raise_for_status()  # verifica se a requisição foi bem-sucedida
        filmes = response.json()["results"]  # extrai a lista de filmes
        
        # escolhe um filme aleatório da página
        filme = random.choice(filmes)
        titulo = filme["title"]
        sinopse = filme["overview"]
        poster = filme["poster_path"]
        link = f"https://www.themoviedb.org/movie/{filme['id']}"
        ano_lancamento = filme["release_date"].split("-")[0]
        nota = filme["vote_average"]
        link = f"https://www.themoviedb.org/movie/{filme['id']}"



        ultimos_filmes[ctx.author.id] = filme['id']
        
        # cria uma embed com as informações do filme
        embed = discord.Embed(
            title=f"🎬 Recomendação de {genero.capitalize()}: {titulo}",
            description=sinopse,
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{poster}")
        embed.add_field(name="mais informações", value=f"[Clique aqui]({link})", inline=False)
        embed.add_field(name="⭐ avaliação", value=f"{nota}/10", inline=True)
            
        await ctx.send(embed=embed)
    
    except Exception as e:
        print(f"Erro ao buscar filme: {e}")
        await ctx.send("não consegui encontrar um filme agora. tente novamente mais tarde!")




 #COMANDO ONDE ASSISTIR               

@bot.command(name='ondeassistir')
async def ondeassistir(ctx, *, nome_filme: str = None):
    if nome_filme is None:
        if ctx.author.id in ultimos_filmes:
            filme_id = ultimos_filmes[ctx.author.id]
        else:
            await ctx.send("❗ você precisa especificar um nome de filme ou usar !recomendar ou !filmealeatorio primeiro.")
            return
    else:
        busca_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=pt-BR&query={nome_filme}"
        try:
            busca_response = requests.get(busca_url)
            busca_response.raise_for_status()
            resultados = busca_response.json()["results"]
            if resultados:
                filme_id = resultados[0]["id"]
            else:
                await ctx.send("🔍 não encontrei nenhum filme com esse nome.")
                return
        except Exception as e:
            print(f"erro ao buscar filme: {e}")
            await ctx.send("⚠️ ocorreu um erro ao procurar o filme.")
            return
    
    streaming_url = f"https://api.themoviedb.org/3/movie/{filme_id}/watch/providers?api_key={TMDB_API_KEY}"
    try:
        streaming_response = requests.get(streaming_url)
        streaming_response.raise_for_status()
        provedores = streaming_response.json()["results"].get("BR", {}).get("flatrate", [])
        
        if provedores:
            plataformas = [f"🎥 {provedor['provider_name']}" for provedor in provedores]
            plataformas_texto = "\n".join(plataformas)
            
            embed = discord.Embed(
                title="📺 onde assistir",
                description="disponível nas seguintes plataformas:",
                color=discord.Color.gold()
            )
            embed.add_field(name="Plataformas", value=plataformas_texto, inline=False)
            embed.set_footer(text="🎬 Aproveite o filme!")
            await ctx.send(embed=embed)
        else:
            await ctx.send("😢 esse filme não está disponível em nenhuma plataforma de streaming no Brasil.")
    except Exception as e:
        print(f"Erro ao buscar provedores de streaming: {e}")
        await ctx.send("⚠️ ocorreu um erro ao procurar as plataformas de streaming.")



# filme do dia (letterboxd based)

@bot.command(name='filmedodia')
async def filme_do_dia(ctx):
    # URL para buscar filmes em tendência
    trending_url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=pt-BR"
    
    try:
        # Requisição para obter os filmes em tendência
        response = requests.get(trending_url)
        response.raise_for_status()
        filmes = response.json()["results"]
        
        if filmes:
            # eleciona um filme aleatório da lista de tendências
            filme = random.choice(filmes)
            
            # extrai infos do filme
            titulo = filme["title"]
            descricao = filme.get("overview", "descrição não disponível.")
            poster_path = filme.get("poster_path", "")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            link_letterboxd = f"https://www.letterboxd.com/search/{titulo.replace(' ', '%20')}"
            ano_lancamento = filme["release_date"].split("-")[0]
            nota = filme["vote_average"]
            link = f"https://www.themoviedb.org/movie/{filme['id']}"


            ultimos_filmes[ctx.author.id] = filme['id']
            
            # embed para exibir as infos do filme
            embed = discord.Embed(
                title=f"🎬 filme do dia: {titulo}",
                description=descricao,
                url=link_letterboxd,
                color=discord.Color.gold()
            )
            embed.set_image(url=poster_url)
            embed.add_field(name="⭐ avaliação", value=f"{nota}/10", inline=True)
            embed.add_field(name="🔗 mais informações", value=f"[Saiba mais]({link})", inline=False)
            embed.set_footer(text="tendências de hoje no letterboxd")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("não foi possível obter os filmes em tendência no momento.")
    
    except Exception as e:
        print(f"erro ao buscar filmes em tendência: {e}")
        await ctx.send("ocorreu um erro ao procurar o filme do dia.")

# COMANDO DIRETOR

@bot.command(name='diretor')
async def diretor(ctx, *, nome_diretor: str = None):
    if nome_diretor is None:
        await ctx.send("você precisa especificar o nome de um diretor.")
        return
    
    # formata o nome do diretor para a API
    nome_diretor_formatado = nome_diretor.replace(" ", "%20")

    # URL para buscar o diretor
    diretor_url = f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&language=pt-BR&query={nome_diretor_formatado}"

    try:
        # requisição para encontrar o diretor
        response = requests.get(diretor_url)
        response.raise_for_status()  # verifica se a requisição foi bem-sucedida
        resultados = response.json().get("results", [])

        if resultados:
            diretor_id = resultados[0]["id"]
            
            # URL para buscar os filmes do diretor
            filmes_url = f"https://api.themoviedb.org/3/person/{diretor_id}/movie_credits?api_key={TMDB_API_KEY}&language=pt-BR"
            
            # Requisição para obter os filmes do diretor
            filmes_response = requests.get(filmes_url)
            filmes_response.raise_for_status()
            filmes = filmes_response.json().get("cast", [])
            
            if filmes:
                filmes_lista = "\n".join([f"**{filme['title']}** ({filme['release_date'][:4]})" for filme in filmes[:10]])  # pega os 10 primeiros filmes
                embed = discord.Embed(
                    title=f"🎬 filmes dirigidos por {nome_diretor}",
                    description=filmes_lista,
                    color=discord.Color.gold()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"não encontrei filmes dirigidos por {nome_diretor}.")
        else:
            await ctx.send(f"não encontrei nenhum diretor com o nome '{nome_diretor}'.")
    
    except requests.exceptions.RequestException as e:
        print(f"erro ao procurar o diretor ou filmes: {e}")
        await ctx.send("ocorreu um erro ao procurar os filmes do diretor.")


# Comando: classicos

@bot.command(name='classicos')
async def classicos(ctx):
    # Define as décadas icônicas
    decadas = ["1920-12-31", "1930-12-31", "1940-12-31", "1950-12-31", "1960-12-31", "1970-12-31"]
    ano_escolhido = random.choice(decadas)
    pagina_aleatoria = random.randint(1, 5)  # Para variar os filmes

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=pt-BR&sort_by=vote_average.desc&vote_count.gte=1000&include_adult=false&include_video=false&page={pagina_aleatoria}&primary_release_date.lte={ano_escolhido}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        filmes = response.json()["results"]
        filme = random.choice(filmes)
        titulo = filme["title"]
        sinopse = filme["overview"] or "sinopse não disponível."
        poster = filme["poster_path"]
        link = f"https://www.themoviedb.org/movie/{filme['id']}"
        ano_lancamento = filme["release_date"].split("-")[0]
        nota = filme["vote_average"]

        ultimos_filmes[ctx.author.id] = filme['id']

        embed = discord.Embed(
            title=f"🎬 clássico do cinema: **{titulo}** ({ano_lancamento})",
            description=f"📖 *{sinopse}*",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{poster}")
        embed.add_field(name="⭐ avaliação", value=f"{nota}/10", inline=True)
        embed.add_field(name="🔗 mais informações", value=f"[Saiba mais]({link})", inline=False)
        embed.set_footer(text="🎥 um marco na história do cinema!")
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"erro ao buscar filme clássico: {e}")
        await ctx.send("🚫 não consegui encontrar um clássico agora. tente novamente mais tarde!")






# inicia o bot
bot.run(TOKEN)