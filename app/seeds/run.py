import asyncio  # <--- Importante para ejecutar corrutinas
import typer

from app.seeds.service import run_all, run_users, run_brands, run_categories, run_articles

app = typer.Typer(help='Seeds: users, brands, categories, articles')


@app.command("all")
def all_():
    # asyncio.run crea el bucle de eventos, ejecuta la función asíncrona y lo cierra
    asyncio.run(run_all())
    typer.secho("🌱 Todos los seeds creados exitosamente", fg=typer.colors.GREEN, bold=True)


@app.command("users")
def users():
    asyncio.run(run_users())
    typer.secho("👤 Usuarios cargados", fg=typer.colors.WHITE)


@app.command("brands")
def brands():
    asyncio.run(run_brands())
    typer.secho("🏷️ Marcas cargadas", fg=typer.colors.CYAN)


@app.command("categories")
def categories():
    asyncio.run(run_categories())
    typer.secho("📌 Categorías cargadas", fg=typer.colors.BLUE)


@app.command("articles")
def articles():
    asyncio.run(run_articles())
    typer.secho("📦 Artículos cargados", fg=typer.colors.YELLOW) 


if __name__ == "__main__":
    app()