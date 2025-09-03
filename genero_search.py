import discord
import requests
import random

# Lista de gêneros disponíveis
GENRES = [
    "Action", "Adventure", "Cars", "Comedy", "Dementia", "Demons",
    "Drama", "Ecchi", "Fantasy", "Game", "Harem", "Hentai",
    "Historical", "Horror", "Josei", "Kids", "Magic", "Martial Arts",
    "Mecha", "Military", "Music", "Mystery", "Parody", "Police",
    "Psychological", "Romance", "Samurai", "School", "Sci-Fi", "Seinen",
    "Shoujo", "Shoujo Ai", "Shounen", "Shounen Ai", "Slice of Life",
    "Space", "Sports", "Super Power", "Supernatural", "Thriller",
    "Vampire", "Yaoi", "Yuri"
]

# IDs de gênero corretos da Jikan API
GENRE_IDS = {
    "Action": 1,
    "Adventure": 2,
    "Cars": 3,
    "Comedy": 4,
    "Dementia": 5,
    "Demons": 6,
    "Drama": 8,
    "Ecchi": 9,
    "Fantasy": 10,
    "Game": 11,
    "Harem": 12,
    "Hentai": 13,
    "Historical": 14,
    "Horror": 16,
    "Josei": 17,
    "Kids": 18,
    "Magic": 19,
    "Martial Arts": 20,
    "Mecha": 21,
    "Military": 22,
    "Music": 23,
    "Mystery": 24,
    "Parody": 25,
    "Police": 26,
    "Psychological": 27,
    "Romance": 28,
    "Samurai": 29,
    "School": 30,
    "Sci-Fi": 31,
    "Seinen": 32,
    "Shoujo": 33,
    "Shoujo Ai": 34,
    "Shounen": 35,
    "Shounen Ai": 36,
    "Slice of Life": 37,
    "Space": 38,
    "Sports": 39,
    "Super Power": 40,
    "Supernatural": 41,
    "Thriller": 42,
    "Vampire": 43,
    "Yaoi": 44,
    "Yuri": 45
}

ITEMS_PER_PAGE = 22  # 22 gêneros por página

def get_genre_buttons(page: int):
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    genres_page = GENRES[start:end]

    view = discord.ui.View(timeout=None)

    # Botões de gênero
    for genre in genres_page:
        button = discord.ui.Button(
            label=genre,
            style=discord.ButtonStyle.primary,
            custom_id=f"genre_{genre}"
        )
        view.add_item(button)

    # Botões de navegação
    if page > 0:
        view.add_item(discord.ui.Button(
            label="⬅️ Página Anterior",
            style=discord.ButtonStyle.secondary,
            custom_id=f"prev_{page-1}"
        ))
    if end < len(GENRES):
        view.add_item(discord.ui.Button(
            label="➡️ Próxima Página",
            style=discord.ButtonStyle.secondary,
            custom_id=f"next_{page+1}"
        ))

    return view

async def handle_genre_interaction(interaction: discord.Interaction):
    cid = interaction.data["custom_id"]

    # Clique em gênero
    if cid.startswith("genre_"):
        genre = cid.split("_", 1)[1]
        genre_id = GENRE_IDS.get(genre)
        if not genre_id:
            await interaction.response.send_message(f"❌ Gênero desconhecido: {genre}", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        # Limites decrescentes: 50, 45, 40 ... até 5
        limits = list(range(100, 4, -5))
        data = []

        for limit in limits:
            url = f"https://api.jikan.moe/v4/anime?genres={genre_id}&order_by=score&sort=desc&limit={limit}"
            response = requests.get(url)
            if response.status_code == 200 and "data" in response.json():
                data = response.json()["data"]
                if data:
                    break  # achou resultados, sai do loop

        if not data:
            await interaction.followup.send(f"❌ Nenhum anime encontrado para o gênero \"{genre}\" mesmo testando limites menores.")
            return

        # Filtrar animes que correspondem ao gênero selecionado
        filtered_animes = []
        genre_lower = genre.lower()
        for anime in data:
            anime_genres = [g['name'].lower() for g in anime.get('genres', [])]
            anime_themes = [t['name'].lower() for t in anime.get('themes', [])]
            if genre_lower in anime_genres or genre_lower in anime_themes:
                filtered_animes.append(anime)

        if not filtered_animes:
            await interaction.followup.send(f"❌ Nenhum anime encontrado para o gênero \"{genre}\" após filtragem.")
            return

        # Embaralhar e pegar os 20 primeiros
        random.shuffle(filtered_animes)
        filtered_animes = filtered_animes[:20]

        animes = "\n".join([
            f"🎬 {anime['title']} (⭐ {anime.get('score', 'N/A')})"
            for anime in filtered_animes
        ])
        await interaction.followup.send(f"📚 20 animes aleatórios do gênero **{genre}**:\n{animes}")

    # Clique em navegação
    elif cid.startswith("prev_") or cid.startswith("next_"):
        page = int(cid.split("_", 1)[1])
        view = get_genre_buttons(page)
        await interaction.response.edit_message(content=f"📚 Selecione um gênero abaixo (Página {page+1}):", view=view)

async def handle_genero_command(client, message):
    view = get_genre_buttons(0)
    await message.channel.send("📚 Selecione um gênero abaixo (Página 1):", view=view)
