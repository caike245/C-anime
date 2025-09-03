import requests
from deep_translator import GoogleTranslator
from googlesearch import search
import discord

def get_valid_link(query, domain):
    for link in search(f"{query} site:{domain}", num_results=3, lang="pt"):
        if domain in link:
            return link
    return None

async def buscar_anime(client, message):
    anime_name = message.content[len('!anime '):].strip()
    if not anime_name:
        await message.channel.send('Por favor, digite o nome de um anime. Ex: `!anime One Piece`')
        return

    await message.channel.send(f'🔎 Procurando informações sobre **{anime_name}**...')
    try:
        url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
        response = requests.get(url).json()

        if "data" not in response or not response["data"]:
            await message.channel.send(f'❌ Não encontrei informações sobre "{anime_name}".')
            return

        anime = response["data"][0]
        title = anime.get("title", "Sem título")
        synopsis = anime.get("synopsis", "Sinopse não disponível.")
        image_url = anime["images"]["jpg"]["image_url"]
        mal_url = anime["url"]
        score = anime.get("score", "N/A")
        year = anime.get("year", "Desconhecido")

        try:
            synopsis_pt = GoogleTranslator(source="auto", target="pt").translate(synopsis)
        except:
            synopsis_pt = synopsis

        link_animesonline = get_valid_link(anime_name, "animesonlinecc.to")
        link_anitube = get_valid_link(anime_name, "anitube.vip")

        embed = discord.Embed(
            title=f"🎬 {title}",
            description=synopsis_pt[:500] + ("..." if len(synopsis_pt) > 500 else ""),
            color=discord.Color.blue(),
            url=mal_url
        )
        if image_url and str(image_url).startswith("http"):
            embed.set_thumbnail(url=image_url)

        embed.add_field(name="⭐ Nota", value=f"{score}", inline=True)
        embed.add_field(name="📅 Ano", value=f"{year}", inline=True)

        if link_animesonline:
            embed.add_field(name="🔗 Assistir Online (AnimesOnline)", value=f"[Clique aqui]({link_animesonline})", inline=False)
        if link_anitube:
            embed.add_field(name="🔗 Assistir Online (AniTube)", value=f"[Clique aqui]({link_anitube})", inline=False)

        embed.set_footer(text="Informações fornecidas por MyAnimeList + Google")
        await message.channel.send(embed=embed)

    except Exception as e:
        await message.channel.send('⚠️ Ocorreu um erro na busca. Tente novamente mais tarde.')
        print(f"Erro: {e}")
