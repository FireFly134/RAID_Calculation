import os
import statistics

import imgkit

from jinja2 import Template

import pandas as pd

from sqlalchemy import create_engine

engine = create_engine(os.getenv("DB_POSTGRESQL", ""))

path_img = "./media/imgs/statisstic_imgs/"


def get_df_filter_by_crystal(df: pd.DataFrame, crystal: str) -> pd.DataFrame:
    """input DataFrame and crystal, output DataFrame[:10]"""
    df = df[df["crystal"] == crystal][:10]
    return df


def get_data(df: pd.DataFrame) -> dict[str, int | float]:
    data: dict[str, int | float] = dict()
    list_crystal: list[str] = [
        "ancient",
        "dark",
        "sacred",
        "pristine",
        "pristine_mif",
    ]
    for c_name in list_crystal:
        info = get_df_filter_by_crystal(df=df, crystal=c_name)
        i = 1
        for idx, row in info.iterrows():
            data[f"{c_name}_{i}"] = row["quantity"]
            i += 1
        for j in range(i, 11):
            data[f"{c_name}_{j}"] = 0
        if not info.empty:
            data[f"{c_name}_mean"] = round(
                statistics.mean(info["quantity"].to_list()), 1
            )
        else:
            data[f"{c_name}_mean"] = 0

    return data


def get_statistics(chat_id: int) -> str:
    info: pd.DataFrame = pd.read_sql_query(
        """
        SELECT quantity, crystal FROM arrival_legend
        WHERE user_id = %(user_id)s
        ORDER BY id ASC;
        """,
        params={"user_id": chat_id},
        con=engine,
    )

    data = get_data(df=info)
    image_name = f"{chat_id}_statistic.jpeg"
    main(data, image_name=image_name)

    return path_img + image_name


def main(data: dict[str, int | float], image_name: str) -> None:
    if not os.path.isdir("./media/imgs/"):
        os.mkdir("./media/imgs/")
    if not os.path.isdir(path_img):
        os.mkdir(path_img)
    # HTML шаблон вашей таблицы
    with open("./media/statistics.html", "r") as html:
        html_template: str = html.read()

    # Заполняем HTML шаблон данными
    html_content = Template(html_template).render(data)

    # Путь для сохранения изображения
    image_path = path_img + image_name

    # Преобразуем HTML в изображение и сохраняем
    imgkit.from_string(html_content, image_path)
