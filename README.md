# SkyRulers
Школа математического моделирования 2023. Разработка модели машинного обучения для выявления зависимости признаков друг от друга по кейсу S7. 

## Ссылки
Google Disk: https://drive.google.com/drive/folders/13tYZweA7svbKJyfORBHVDFs0c54uxtZk?usp=sharing

Trello: https://trello.com/b/M6qpalEy/облако

Notion: https://www.notion.so/be5dc2bbfd66463888958a456f96b8e7?pvs=4

Отчет по анализу признаков: ![Alt text](https://docs.google.com/document/d/1VFu-uK7tnos7f2H5roqbkRfUW2aZlmt3yjotGooOckU/edit?usp=share_link)

Протестировать можно на "SkyRulers/data/cruise_CF34-8E.csv"

Демонстрация работы: ![Alt text](https://github.com/tainella/SkyRulers/blob/9a0f765df2eb4e53e46fb75f54fca578a54a27ba/data/demo.jfif)

Архитектура проекта: ![Alt text](https://github.com/tainella/SkyRulers/blob/59f33d04b226c2bd588314a11879dd899addbc10/data/arcitechture.png)

В процессе выполнения проекта применялся инструментарий ClearML
![Alt text](https://github.com/tainella/SkyRulers/blob/109196bd0ff6334784141a937379daaef79f81f3/data/screenshot.jfif)

## Установка и запуск проекта
sudo docker-compose up

По ссылке localhost:49903


## Описание структуры репозитория

Для данного проекта мы обeчили для каждого типа двигателя свой набор параметров и сохранили веса в папке ml/models. Также при обучении были выделены ключевые фичи которые  сохранены в data/{engine_family}_needed.json
для обработки данных для предсказания результатов.
