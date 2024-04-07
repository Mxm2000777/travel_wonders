from contextlib import asynccontextmanager
import flet as ft
import flet_fastapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from MetaXdb import POSTGRESQL
db = POSTGRESQL(password="-464906404postgresql", dbname="travel_wonders").load_table("attractions")
att = db.get_column("id")
lst = {(db.get(id, "avab") +(int(db.get(id, "costb"))/5) + 1) * (1 if db.get(id, "unikb") is None else int(db.get(id, "unikb"))): id for id in att}
x = sorted(lst.keys(), reverse=True)[:10]
dump = [db.get_row(lst[i]) for i in x]
templates = Jinja2Templates(directory="templates")
@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()
app = FastAPI(lifespan=lifespan)
async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    async def route_change(route):
        troute = ft.TemplateRoute(page.route)
        page.views.clear()
        if page.route == "/":
            print("AAA")
            await page.go_async("/map")
        elif troute.match("/attr/:id"):
            dump = db.get_row(troute.id)
            chart = ft.BarChart(
                bar_groups=[
                    ft.BarChartGroup(
                        x=0,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=dump[17],
                                width=40,
                                color=ft.colors.AMBER,
                                tooltip=dump[8],
                                border_radius=0,
                            ),
                        ],
                    ),
                    ft.BarChartGroup(
                        x=1,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=dump[18],
                                width=40,
                                color=ft.colors.BLUE,
                                tooltip=dump[11],
                                border_radius=0,
                            ),
                        ],
                    ),
                    ft.BarChartGroup(
                        x=2,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=dump[19],
                                width=40,
                                color=ft.colors.RED,
                                tooltip="UNIKB",
                                border_radius=0,
                            ),
                        ],
                    ),
                ],
                border=ft.border.all(1, ft.colors.GREY_400),
                left_axis=ft.ChartAxis(
                    labels_size=40, title=ft.TextButton(":)", on_click=await page.go_async("rating")), title_size=40
                ),
                bottom_axis=ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=0, label=ft.Container(ft.Text("AVAB"), padding=10)
                        ),
                        ft.ChartAxisLabel(
                            value=1, label=ft.Container(ft.Text("COSTB"), padding=10)
                        ),
                        ft.ChartAxisLabel(
                            value=2, label=ft.Container(ft.Text("UNIKB"), padding=10)
                        ),
                    ],
                    labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
                max_y=15,
                interactive=True,
                expand=True,
            )

            page.views.append(
                ft.View(
                    page.route,
                    [
                        ft.Text(dump[1]), chart
                    ]
                )
            )
        elif page.route == "/rating":
            if True:
                chart = ft.BarChart(
                bar_groups=[ft.BarChartGroup(
                        x=2,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=i,
                                width=40,
                                color=ft.colors.RED,
                                tooltip=db.get(lst[i], "name"),
                                border_radius=0,
                            ) for i in x],),
                ],
                border=ft.border.all(1, ft.colors.GREY_400),
                left_axis=ft.ChartAxis(
                    labels_size=40, title=ft.TextButton(":)", on_click=await page.go_async("rating")), title_size=40
                ),
                bottom_axis=ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=db.get(lst[i], "vid"), label=ft.Container(ft.Text(db.get(lst[i], "name")), padding=10)
                        ) for i in x],
                    labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
                max_y=200,
                interactive=True,
                expand=True,
            )
                page.views.append(
                ft.View(
                    page.route,
                    [
                        chart
                    ]
                )
            )
        else:
              page.views.append(
                ft.View(
                    page.route,
                    [
                    ft.Text("Инвалид роут")
                    ]
                )
            )
        print("Обновление страницы...", page.route)
        await page.update_async()

    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async(page.route)
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
@app.get("/map",response_class=HTMLResponse)
async def mapy(request: Request):
    return templates.TemplateResponse("map.html", {"request":request, "dump": dump})
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", flet_fastapi.app(main, assets_dir="C:\\Users\\mxm20\\my_projects\\travel_wonders\\assets"))