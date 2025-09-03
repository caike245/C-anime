import discord
from googlesearch import search

def get_valid_link(query, domain):
    for link in search(f"{query} site:{domain}", num_results=3, lang="pt"):
        if domain in link:
            return link
    return None

async def buscar_serie(client, message):
    serie_name = message.content[len('!serie '):].strip()
    if not serie_name:
        await message.channel.send('Por favor, digite o nome de uma série. Ex: `!serie Dexter`')
        return

    await message.channel.send(f'🔎 Procurando informações sobre **{serie_name}**...')

    try:
        serie_link = get_valid_link(serie_name, "xilftenfilmes.com")
        if not serie_link:
            await message.channel.send(f'❌ Não encontrei informações sobre "{serie_name}".')
            return

        embed = discord.Embed(
            title=f"📺 {serie_name}",
            description="Clique no link abaixo para assistir.",
            color=discord.Color.green(),
            url=serie_link
        )
        embed.add_field(name="▶️ Assista Online", value=f"[Clique aqui]({serie_link})", inline=False)
        embed.set_footer(text="Informações fornecidas por XilftenFilmes")
        await message.channel.send(embed=embed)

    except Exception as e:
        await message.channel.send('⚠️ Ocorreu um erro na busca. Tente novamente mais tarde.')
        print(f"Erro: {e}")
