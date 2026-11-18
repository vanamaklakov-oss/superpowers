# Five breakdown Shorts in Russian. Each scene: what is said, how, and what pops on screen.
# A cue is a word (the first spoken word starting with it, searched from the previous cue onward)
# or an int (frames after the voice starts). Facts and sources: README.md.

ORANGE, TEAL, PINK, YEL, LIME, BLUE, PURPLE, PEACH, MINT, RED = "#ff9f43", "#2ed3c6", "#ff6fb5", "#ffd84d", "#a6e34b", "#4da3ff", "#a77bff", "#ffb48a", "#6ee7b7", "#ff5a5a"

VIDEOS = {
"pc": dict(title="Потянет ли твой ПК GTA 6?", pal=dict(bg=["#1fb5c9", "#ff8a3d"], blobs=["#ffd84d", "#2ed3c6", "#ff6fb5", "#7b5cff"], accent=[ORANGE, TEAL, PINK, YEL]), scenes=[
  dict(say="Короче. Если GTA 6 выйдет на ПК — какой комп тебе понадобится? Смотрим на PS5: игру делали именно под неё.", rate="+6%", items=[
    dict(t="head", text="ПОТЯНЕТ ЛИ", cue=0, size=112), dict(t="head", text="ТВОЙ ПК GTA 6?", cue=6, size=112, color=YEL),
    dict(t="icon", name="console", cue="PS5", color=TEAL), dict(t="pills", pills=[dict(text="PS5 — ЭТАЛОН", cue="игру")])]),
  dict(say="Процессор. У PS5 восемь ядер Zen 2, до трёх с половиной гигагерц. На ПК это примерно Ryzen 7 3700X.", rate="+6%", items=[
    dict(t="head", text="ПРОЦЕССОР", cue=0), dict(t="big", text="8 ЯДЕР", count=8, suffix=" ЯДЕР", sub="ZEN 2 · ДО 3,5 ГГЦ", cue="восемь"),
    dict(t="icon", name="chip", cue="ПК", color=ORANGE, scale=0.85), dict(t="pills", pills=[dict(text="≈ RYZEN 7 3700X", cue="Ryzen", color=YEL)])]),
  dict(say="Видеокарта. Десять и три десятых терафлопса. Это где-то RX 6700 или RTX 2070 Super. И RTX 3060 тоже потянет.", rate="+6%", items=[
    dict(t="head", text="ВИДЕОКАРТА", cue=0), dict(t="big", text="10,3", count=10.3, dec=1, sub="ТЕРАФЛОПСА", cue="Десять"),
    dict(t="icon", name="gpu", cue="Это", color=PINK, scale=0.85),
    dict(t="pills", size=46, pills=[dict(text="RX 6700", cue="RX"), dict(text="RTX 2070 SUPER", cue="или")]),
    dict(t="pills", pills=[dict(text="RTX 3060", cue="И", color=MINT, mark="check")])]),
  dict(say="Память у PS5 общая — шестнадцать гигов. Значит, ставь шестнадцать гигов оперативки.", rate="+4%", items=[
    dict(t="head", text="ПАМЯТЬ", cue=0), dict(t="big", text="16 ГБ", count=16, suffix=" ГБ", sub="ОБЩАЯ GDDR6", cue="шестнадцать"),
    dict(t="icon", name="ram", cue="Значит", color=TEAL), dict(t="pills", pills=[dict(text="16 ГБ ОЗУ", cue="оперативки", color=YEL)])]),
  dict(say="А SSD у неё читает пять с половиной гигабайт в секунду. Так что жёсткий диск — мимо. Бери NVMe.", rate="+6%", items=[
    dict(t="head", text="НАКОПИТЕЛЬ", cue=0), dict(t="big", text="5,5 ГБ/С", count=5.5, dec=1, suffix=" ГБ/С", sub="СКОРОСТЬ ЧТЕНИЯ SSD", cue="пять"),
    dict(t="icon", name="hdd", cue="жёсткий", color="#c9b8ff", mark="cross", markCue="мимо", scale=0.8),
    dict(t="pills", pills=[dict(text="БЕРИ NVME SSD", cue="Бери", color=MINT)])]),
  dict(say="Вот твой минимум: Full HD и около тридцати кадров.", rate="+2%", items=[
    dict(t="head", text="МИНИМУМ", cue=0, color=YEL), dict(t="pills", pills=[dict(text="1080P · ~30 FPS", cue="Full")]),
    dict(t="list", rows=[dict(label="ЦП", text="RYZEN 7 3700X", cue=4), dict(label="ВИДЕО", text="RTX 3060 / RX 6700", cue=10), dict(label="ОЗУ", text="16 ГБ", cue=16), dict(label="SSD", text="NVME", cue=22)])]),
  dict(say="Хочешь шестьдесят кадров? Целься в RTX 4070 и тридцать два гига.", rate="+4%", items=[
    dict(t="head", text="ХОЧЕШЬ 60 FPS?", cue=0, color=MINT), dict(t="icon", name="gpu", cue="Целься", color=LIME),
    dict(t="pills", pills=[dict(text="RTX 4070", cue="RTX", color=LIME)]), dict(t="pills", pills=[dict(text="32 ГБ ОЗУ", cue="тридцать", color=YEL)])]),
  dict(say="Но это прикидки: версию для ПК ещё даже не анонсировали. Пиши свой сетап в комменты!", rate="+4%", items=[
    dict(t="head", text="ЭТО ПРИКИДКИ", cue=0, color=YEL), dict(t="text", text="ВЕРСИЮ ДЛЯ ПК ЕЩЁ НЕ АНОНСИРОВАЛИ", cue="версию", size=56),
    dict(t="head", text="ТВОЙ СЕТАП?", cue="Пиши", size=120), dict(t="arrow", cue="комменты")]),
]),

"40sec": dict(title="GTA 6 за 40 секунд", pal=dict(bg=["#ff5fa2", "#ffb347"], blobs=["#ffe66d", "#ff6fb5", "#7b5cff", "#2ed3c6"], accent=[YEL, PURPLE, TEAL, PINK]), scenes=[
  dict(say="GTA 6 выходит девятнадцатого ноября. Вот всё, что нужно знать, — за сорок секунд!", rate="+6%", items=[
    dict(t="head", text="GTA 6", cue=0, size=170, color=YEL), dict(t="icon", name="calendar", cue="девятнадцатого", color=PINK, scale=0.9),
    dict(t="big", text="19 НОЯБРЯ", cue="ноября"), dict(t="pills", pills=[dict(text="ВСЁ ЗА 40 СЕКУНД", cue="сорок")])]),
  dict(say="Тринадцать лет! Прошлая часть, GTA 5, вышла ещё в 2013 году.", rate="+4%", items=[
    dict(t="big", text="13 ЛЕТ", count=13, suffix=" ЛЕТ", cue=0), dict(t="icon", name="controller", cue="Прошлая", color=TEAL, scale=0.9),
    dict(t="pills", pills=[dict(text="GTA 5 · 2013", cue="2013"), dict(text="GTA 6 · 2026", cue=48, color=YEL)])]),
  dict(say="Релиз переносили дважды: с 2025-го — на май 2026-го. А потом — на девятнадцатое ноября.", rate="+4%", items=[
    dict(t="head", text="ДВА ПЕРЕНОСА", cue=0), dict(t="list", rows=[dict(label="БЫЛО", text="2025", cue="2025", mark="cross"), dict(label="ПОТОМ", text="МАЙ 2026", cue="май", mark="cross"), dict(label="ИТОГ", text="19 НОЯБРЯ 2026", cue="девятнадцатое", mark="check", color=MINT)])]),
  dict(say="Играем за Лусию и Джейсона — в штате Леонида. Это версия Флориды от Rockstar. Там же и Вайс-Сити.", rate="+4%", items=[
    dict(t="head", text="ГДЕ И ЗА КОГО", cue=0), dict(t="pills", pills=[dict(text="ЛУСИЯ", cue="Лусию", color=PINK), dict(text="ДЖЕЙСОН", cue="Джейсона", color=BLUE)]),
    dict(t="icon", name="pin", cue="Леонида", color=ORANGE, scale=0.9), dict(t="pills", size=46, pills=[dict(text="ЛЕОНИДА ≈ ФЛОРИДА", cue="Флориды"), dict(text="ВАЙС-СИТИ", cue="Вайс", color=TEAL)])]),
  dict(say="Выходит на PS5 и Xbox Series X и S. А версии для ПК — пока нет.", rate="+4%", items=[
    dict(t="head", text="ПЛАТФОРМЫ", cue=0), dict(t="pills", pills=[dict(text="PS5", cue="PS5", color=BLUE, mark="check")]),
    dict(t="pills", pills=[dict(text="XBOX SERIES X|S", cue="Xbox", color=MINT, mark="check")]), dict(t="pills", pills=[dict(text="ПК — ПОКА НЕТ", cue="ПК", color=RED, mark="cross")])]),
  dict(say="Первый трейлер за сутки собрал девяносто три миллиона просмотров на Ютубе. Это был рекорд.", rate="+4%", items=[
    dict(t="icon", name="eye", cue=0, color=TEAL, scale=0.9), dict(t="big", text="93 МЛН", count=93, suffix=" МЛН", sub="ПРОСМОТРОВ ЗА 24 ЧАСА", cue="девяносто"),
    dict(t="pills", pills=[dict(text="РЕКОРД", cue="рекорд", color=YEL)])]),
  dict(say="В день релиза будет стрим на сутки.", rate="+4%", items=[
    dict(t="icon", name="clock", cue=0, color=PINK), dict(t="pills", pills=[dict(text="СТРИМ ДНЯ РЕЛИЗА", cue="стрим", color=RED)]), dict(t="big", text="24 ЧАСА", count=24, suffix=" ЧАСА", cue="сутки")]),
  dict(say="Ну что — играешь в первый же день?", rate="+2%", items=[
    dict(t="head", text="ИГРАЕШЬ", cue=0, size=140, color=YEL), dict(t="head", text="В ДЕНЬ РЕЛИЗА?", cue="первый", size=110), dict(t="arrow", cue=30)]),
]),

"chrono": dict(title="13 лет ожидания GTA 6", pal=dict(bg=["#7b5cff", "#ff9a8b"], blobs=["#ffd1a6", "#a77bff", "#ff6fb5", "#6ee7b7"], accent=[PEACH, PURPLE, MINT, PINK]), scenes=[
  dict(say="Как мы ждали GTA 6 тринадцать лет. Вся хронология — за сорок секунд.", rate="+4%", items=[
    dict(t="head", text="13 ЛЕТ", cue=0, size=170, color=YEL), dict(t="head", text="ОЖИДАНИЯ", cue=8, size=120), dict(t="icon", name="clock", cue="хронология", color=PURPLE)]),
  dict(say="Сентябрь 2013-го. Выходит GTA 5. Все уверены: шестая будет через пару лет.", rate="+4%", items=[
    dict(t="pills", pills=[dict(text="СЕНТЯБРЬ 2013", cue=0, color=YEL)]), dict(t="big", text="GTA 5", cue="Выходит"), dict(t="text", text="«ШЕСТАЯ ЧЕРЕЗ ПАРУ ЛЕТ…»", cue="Все")]),
  dict(say="Годы идут. Пятую переиздают на новых консолях — а о шестой тишина.", rate="+2%", items=[
    dict(t="icon", name="controller", cue=0, color=TEAL, scale=0.9), dict(t="pills", pills=[dict(text="ПЕРЕИЗДАНИЯ GTA 5", cue="переиздают")]), dict(t="big", text="ТИШИНА…", cue="тишина")]),
  dict(say="Декабрь 2023-го: первый трейлер. Девяносто три миллиона просмотров за сутки!", rate="+4%", items=[
    dict(t="pills", pills=[dict(text="ДЕКАБРЬ 2023", cue=0, color=YEL)]), dict(t="icon", name="play", cue="первый", color=RED), dict(t="big", text="93 МЛН", count=93, suffix=" МЛН", sub="ЗА СУТКИ", cue="Девяносто")]),
  dict(say="Май 2025-го. Релиз переносят на май 2026-го, и выходит второй трейлер.", rate="+4%", items=[
    dict(t="pills", pills=[dict(text="МАЙ 2025", cue=0, color=YEL)]), dict(t="list", rows=[dict(label="ПЕРЕНОС", text="НА МАЙ 2026", cue="переносят", color=PEACH), dict(label="ТРЕЙЛЕР", text="ВТОРОЙ", cue="второй", color=MINT)])]),
  dict(say="Ноябрь 2025-го. Ещё один перенос — на девятнадцатое ноября 2026-го.", rate="+4%", items=[
    dict(t="pills", pills=[dict(text="НОЯБРЬ 2025", cue=0, color=YEL)]), dict(t="head", text="ЕЩЁ ПЕРЕНОС", cue="Ещё", color=PEACH), dict(t="icon", name="calendar", cue="девятнадцатое", color=PINK, scale=0.9)]),
  dict(say="Двенадцатое ноября: открывают предзагрузку для цифровых предзаказов.", rate="+4%", items=[
    dict(t="pills", pills=[dict(text="12 НОЯБРЯ 2026", cue=0, color=YEL)]), dict(t="icon", name="ssd", cue="открывают", color=MINT), dict(t="big", text="ПРЕДЗАГРУЗКА", cue="предзагрузку")]),
  dict(say="И вот — девятнадцатое ноября. Тринадцать лет, и мы дождались. А ты сколько ждал?", rate="+2%", items=[
    dict(t="big", text="19 НОЯБРЯ", cue=0), dict(t="head", text="МЫ ДОЖДАЛИСЬ", cue="мы", color=YEL), dict(t="head", text="А ТЫ СКОЛЬКО ЖДАЛ?", cue="А", size=86), dict(t="arrow", cue="ждал")]),
]),

"numbers": dict(title="GTA 6 в цифрах", pal=dict(bg=["#2b6bff", "#7ee081"], blobs=["#c6ff5e", "#4da3ff", "#ff6fb5", "#2ed3c6"], accent=[LIME, BLUE, YEL, TEAL]), scenes=[
  dict(say="GTA 6 в цифрах. Погнали!", rate="+6%", items=[
    dict(t="head", text="GTA 6", cue=0, size=170, color=YEL), dict(t="head", text="В ЦИФРАХ", cue="цифрах", size=130), dict(t="icon", name="controller", cue="Погнали", color=LIME)]),
  dict(say="Тринадцать — столько лет прошло после выхода GTA 5.", rate="+4%", items=[
    dict(t="big", text="13", count=13, sub="ЛЕТ ПОСЛЕ GTA 5", cue=0), dict(t="icon", name="clock", cue="лет", color=BLUE)]),
  dict(say="Девяносто три миллиона — столько просмотров набрал первый трейлер за сутки.", rate="+4%", items=[
    dict(t="big", text="93 МЛН", count=93, suffix=" МЛН", sub="ПЕРВЫЙ ТРЕЙЛЕР · 24 ЧАСА", cue=0), dict(t="icon", name="play", cue="первый", color=RED)]),
  dict(say="Четыреста семьдесят пять миллионов — это второй трейлер за первые сутки, на всех площадках сразу.", rate="+6%", items=[
    dict(t="big", text="475 МЛН", count=475, suffix=" МЛН", sub="ВТОРОЙ ТРЕЙЛЕР · ВСЕ ПЛОЩАДКИ", cue=0), dict(t="icon", name="eye", cue="второй", color=TEAL, scale=0.85)]),
  dict(say="Сорок миллиардов — столько просмотров у роликов про GTA 6 на Ютубе. И это ещё до релиза.", rate="+6%", items=[
    dict(t="big", text="40 МЛРД", count=40, suffix=" МЛРД", sub="ПРОСМОТРОВ РОЛИКОВ ПРО GTA 6", cue=0), dict(t="icon", name="phone", cue="роликов", color=LIME, scale=0.75), dict(t="pills", pills=[dict(text="ЕЩЁ ДО РЕЛИЗА", cue="ещё", color=YEL)])]),
  dict(say="Двадцать четыре часа — столько будет идти стрим Ютуба в день релиза.", rate="+4%", items=[
    dict(t="big", text="24 ЧАСА", count=24, suffix=" ЧАСА", sub="СТРИМ YOUTUBE В ДЕНЬ РЕЛИЗА", cue=0), dict(t="icon", name="clock", cue="стрим", color=RED)]),
  dict(say="Два — столько раз переносили релиз.", rate="+2%", items=[
    dict(t="big", text="2", count=2, sub="ПЕРЕНОСА РЕЛИЗА", cue=0), dict(t="icon", name="calendar", cue="переносили", color=BLUE, scale=0.9)]),
  dict(say="И одна дата: девятнадцатое ноября. Какая цифра удивила тебя? Пиши!", rate="+4%", items=[
    dict(t="big", text="19.11", cue="девятнадцатое"), dict(t="head", text="КАКАЯ ЦИФРА", cue="Какая", size=100), dict(t="head", text="УДИВИЛА ТЕБЯ?", cue="удивила", size=100, color=YEL), dict(t="arrow", cue="Пиши")]),
]),

"meme": dict(title="Откуда мем «раньше, чем GTA 6»", pal=dict(bg=["#13c296", "#d13cff"], blobs=["#6ee7b7", "#ff6fb5", "#ffd84d", "#7b5cff"], accent=[MINT, PINK, YEL, PURPLE]), scenes=[
  dict(say="Откуда взялся мем «раньше, чем GTA 6»? Сейчас расскажу.", rate="+6%", items=[
    dict(t="head", text="«РАНЬШЕ,", cue=0, size=130, color=YEL), dict(t="head", text="ЧЕМ GTA 6»", cue="чем", size=130), dict(t="pills", pills=[dict(text="ОТКУДА МЕМ?", cue="Сейчас")])]),
  dict(say="Июль 2023-го. В Конгрессе США — слушания про НЛО. Бывший сотрудник разведки рассказывает про неземные аппараты.", rate="+6%", items=[
    dict(t="pills", pills=[dict(text="ИЮЛЬ 2023", cue=0, color=YEL)]), dict(t="icon", name="capitol", cue="Конгрессе", color=MINT, scale=0.85), dict(t="text", text="СЛУШАНИЯ ПРО НЛО", cue="слушания")]),
  dict(say="А на следующий день тиктокер выкладывает видео: «Мы получили пришельцев раньше, чем GTA 6».", rate="+4%", items=[
    dict(t="icon", name="phone", cue="тиктокер", color=PINK, scale=0.75), dict(t="icon", name="alien", cue="пришельцев", color=LIME, scale=0.8), dict(t="text", text="«ПРИШЕЛЬЦЫ РАНЬШЕ GTA 6»", cue="раньше")]),
  dict(say="И понеслось. Формат прикладывают к любой новости: что угодно — лишь бы раньше GTA 6.", rate="+6%", items=[
    dict(t="head", text="И ПОНЕСЛОСЬ", cue=0, color=YEL), dict(t="pills", size=44, pills=[dict(text="НОВОСТИ", cue="любой"), dict(text="ПРИШЕЛЬЦЫ", cue="любой")]), dict(t="pills", size=44, pills=[dict(text="ЧТО УГОДНО", cue="угодно", color=YEL)]), dict(t="big", text="…РАНЬШЕ GTA 6", cue="лишь")]),
  dict(say="Похожие шутки встречались и раньше. Но массовым мем стал именно летом 2023-го.", rate="+4%", items=[
    dict(t="text", text="ШУТКИ БЫЛИ И РАНЬШЕ", cue=0), dict(t="head", text="НО ХИТОМ СТАЛ", cue="массовым", color=YEL), dict(t="pills", pills=[dict(text="ЛЕТО 2023", cue="летом", color=PINK)])]),
  dict(say="Девятнадцатого ноября GTA 6 выходит — и мем официально уходит на пенсию.", rate="+4%", items=[
    dict(t="big", text="19 НОЯБРЯ", cue=0), dict(t="icon", name="grave", cue="мем", color=PINK, scale=0.85), dict(t="pills", pills=[dict(text="МЕМ НА ПЕНСИИ", cue="пенсию", color=YEL)])]),
  dict(say="Тринадцать лет шуток. Прощай, легенда.", rate="+0%", items=[
    dict(t="big", text="13 ЛЕТ ШУТОК", cue=0), dict(t="head", text="ПРОЩАЙ, ЛЕГЕНДА", cue="Прощай", size=100, color=YEL)]),
  dict(say="А что ты получил раньше, чем GTA 6? Пиши в комменты!", rate="+4%", items=[
    dict(t="head", text="А ЧТО ТЫ ПОЛУЧИЛ", cue=0, size=92), dict(t="head", text="РАНЬШЕ GTA 6?", cue="раньше", size=120, color=YEL), dict(t="arrow", cue="Пиши")]),
]),
}

VIDEOS["fps30"] = dict(title="Почему GTA 6 только в 30 FPS", fx=dict(rays=True, bursts=True, doodles=16),
  pal=dict(bg=["#ff2e7e", "#6a2cff"], blobs=["#ffd84d", "#00e5ff", "#ff8a00", "#a6ff00", "#ff4fd8", "#3dffb0"], accent=[YEL, "#00e5ff", LIME, ORANGE, PINK]), scenes=[
  dict(say="GTA 6 на консолях будет в тридцати кадрах. Даже на PS5 Pro! Почему так? Разбираемся.", rate="+6%", items=[
    dict(t="head", text="ПОЧЕМУ GTA 6", cue=0, size=118), dict(t="head", text="ТОЛЬКО В", cue="тридцати", size=118, color=YEL),
    dict(t="big", text="30 FPS", count=30, suffix=" FPS", cue="тридцати", color="#ff2e7e"), dict(t="pills", pills=[dict(text="ДАЖЕ НА PS5 PRO", cue="Даже", color="#00e5ff")])]),
  dict(say="Десятого ноября Рокстар сама это подтвердила: цель — тридцать кадров на PS5, PS5 Pro и Xbox Series.", rate="+6%", items=[
    dict(t="pills", pills=[dict(text="10 НОЯБРЯ", cue=0, color=YEL)]), dict(t="text", text="ОФИЦИАЛЬНО ОТ ROCKSTAR", cue="Рокстар"),
    dict(t="icon", name="console", cue="цель", color="#00e5ff", scale=0.6),
    dict(t="pills", size=44, pills=[dict(text="PS5 · 30", cue="PS5"), dict(text="PS5 PRO · 30", cue="Pro"), dict(text="XBOX · 30", cue="Xbox")])]),
  dict(say="Зачем? Так студия сохраняет плотность мира и детализацию картинки.", rate="+4%", items=[
    dict(t="head", text="ЗАЧЕМ?", cue=0, size=150, color=YEL), dict(t="pills", pills=[dict(text="ПЛОТНЫЙ МИР", cue="плотность", color=LIME)]),
    dict(t="pills", pills=[dict(text="ДЕТАЛИЗАЦИЯ", cue="детализацию", color="#00e5ff")]), dict(t="icon", name="eye", cue="картинки", color=PINK, scale=0.9)]),
  dict(say="Посчитаем. При тридцати кадрах на один кадр есть тридцать три миллисекунды. А при шестидесяти — всего шестнадцать.", rate="+6%", items=[
    dict(t="head", text="ПОСЧИТАЕМ", cue=0), dict(t="icon", name="clock", cue="тридцати", color=ORANGE, scale=0.75),
    dict(t="big", text="33 МС", count=33, suffix=" МС", sub="НА КАДР ПРИ 30 FPS", cue="тридцать", color="#1d8f3a"),
    dict(t="big", text="16 МС", count=16, suffix=" МС", sub="НА КАДР ПРИ 60 FPS", cue="шестидесяти", color="#e0245e")]),
  dict(say="И главный тормоз — процессор. Он просчитывает каждого прохожего, машины, физику и полицию.", rate="+6%", items=[
    dict(t="head", text="ГЛАВНЫЙ ТОРМОЗ", cue=0), dict(t="icon", name="chip", cue="процессор", color=ORANGE, scale=0.85),
    dict(t="pills", size=46, pills=[dict(text="ПРОХОЖИЕ", cue="прохожего", color=PINK), dict(text="МАШИНЫ", cue="машины", color=YEL)]),
    dict(t="pills", size=46, pills=[dict(text="ФИЗИКА", cue="физику", color=LIME), dict(text="ПОЛИЦИЯ", cue="полицию", color="#00e5ff")])]),
  dict(say="А в PS5 Pro процессор почти тот же. Прокачали видеокарту, а не его.", rate="+4%", items=[
    dict(t="head", text="А ЧТО PS5 PRO?", cue=0, color=YEL),
    dict(t="list", rows=[dict(label="ЦП", text="ПОЧТИ ТОТ ЖЕ", cue="процессор", mark="cross", color=ORANGE), dict(label="ВИДЕО", text="СИЛЬНО МОЩНЕЕ", cue="Прокачали", mark="check", color=LIME)]),
    dict(t="icon", name="gpu", cue="видеокарту", color=LIME, scale=0.85)]),
  dict(say="Поэтому Pro получит не шестьдесят кадров, а картинку получше: апскейл PSSR и тени с трассировкой лучей.", rate="+6%", items=[
    dict(t="head", text="ЧТО ДАСТ PRO", cue=0), dict(t="pills", pills=[dict(text="60 FPS", cue="шестьдесят", color="#ff6b6b", mark="cross")]),
    dict(t="pills", pills=[dict(text="АПСКЕЙЛ PSSR", cue="апскейл", color="#00e5ff", mark="check")]), dict(t="pills", pills=[dict(text="RT-ТЕНИ", cue="тени", color=LIME, mark="check")])]),
  dict(say="А режим шестидесяти кадров пока даже не анонсировали. Тридцать кадров — норм или нет? Пиши!", rate="+4%", items=[
    dict(t="text", text="РЕЖИМ 60 FPS НЕ АНОНСИРОВАН", cue="режим", size=54), dict(t="head", text="30 FPS —", cue="Тридцать", size=140, color=YEL),
    dict(t="head", text="НОРМ ИЛИ НЕТ?", cue="норм", size=120), dict(t="arrow", cue="Пиши")]),
])
