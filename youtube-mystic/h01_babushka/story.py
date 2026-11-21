# «Бабушка, о которой мне не говорили» — горизонтальный ролик ~5 мин, мультик-стиль toon.py (вымысел, рубрика «Страшные истории»).
VOICE = ("ru-RU-DmitryNeural", 6, 8)
STYLE = {"size": (1920, 1080), "capy": 790, "capsize": 84, "mood": "horror", "gap": 0.12, "tempo": 1.1}
GR = {"voice": ("ru-RU-SvetlanaNeural", -6, -10)}            # бабушка
GRW = {"voice": ("ru-RU-SvetlanaNeural", -4, -12), "fx": "whisper"}
OTHER = {"voice": ("ru-RU-SvetlanaNeural", -8, -18), "fx": "ghost"}
MOM = {"voice": ("ru-RU-SvetlanaNeural", 0, 4), "fx": "phone"}
MOMX = {"voice": ("ru-RU-SvetlanaNeural", -6, -8), "fx": "ghost"}
PET = {"voice": ("ru-RU-DmitryNeural", 12, 45)}

def A(who, x, **k): return {"who": who, "x": x, **k}
BOY = lambda x, **k: A("boy", x, **k)
NIGHT = {"night": True}
SCENES = [
    (1, "Мне было двенадцать, когда я узнал, что у меня есть бабушка. А через неделю родители отправили меня к ней на всё лето.", [
        {"k": "set", "bg": "house", "night": True, "cam": "in", "sfx": "sting", "actors": [A("granny", 0.5, y=900, s=0.8, e="dot", m="smile")]},
        {"at": "через", "k": "set", "bg": "flat", "cam": "r", "actors": [A("mom", 0.3), A("dad", 0.45), BOY(0.75, e="wide", m="o")]},
        {"at": "лето", "k": "set", "bg": "flat", "cam": "in", "focus": (0.75, 0.4), "amt": 0.3, "actors": [A("mom", 0.3), A("dad", 0.45), BOY(0.75, e="shock", m="o", a="up")]}]),
    (2, "Раньше о ней никто не говорил. Ни на праздниках, ни по телефону. Будто её никогда не было.", [
        {"k": "set", "bg": "flat", "cam": "l", "actors": [A("mom", 0.35, m="line"), A("dad", 0.55, m="line")]},
        {"at": "телефону", "k": "phone", "name": "Мама", "cam": "in"},
        {"at": "будто", "k": "photo", "cut": True, "cam": "out"}]),
    (3, "В нашем семейном альбоме есть одна странная фотография. Мама с папой, я совсем маленький на руках. А рядом кто-то третий. И его лицо аккуратно вырезано ножницами.", [
        {"k": "photo", "cut": True, "cam": "in", "amt": 0.1},
        {"at": "мама", "k": "photo", "cut": True, "cam": "in", "focus": (0.4, 0.5), "amt": 0.35},
        {"at": "третий", "k": "photo", "cut": True, "cam": "in", "focus": (0.6, 0.38), "amt": 0.5, "sfx": "sting"},
        {"at": "ножницами", "k": "photo", "cut": True, "cam": "in", "focus": (0.6, 0.38), "amt": 0.9}]),
    (4, "Я спросил маму, кто это. Она забрала альбом и сказала: тебе пора собирать вещи.", [
        {"k": "set", "bg": "flat", "cam": "in", "actors": [A("mom", 0.4, m="line"), BOY(0.65, e="dot", m="o", a="point", flip=True)]},
        {"at": "забрала", "k": "set", "bg": "flat", "cam": "in", "focus": (0.4, 0.4), "amt": 0.35, "actors": [A("mom", 0.4, e="angry", m="frown"), BOY(0.65, e="wide", m="line", flip=True)]}]),
    (5, "Ехали мы почти весь день. Папа молчал, мама смотрела в окно. А радио почему-то шипело всю дорогу.", [
        {"k": "car", "cam": "r", "sfx": "engine"},
        {"at": "папа", "k": "car", "cam": "in", "focus": (0.5, 0.55), "amt": 0.5},
        {"at": "радио", "k": "car", "cam": "in", "focus": (0.4, 0.55), "amt": 0.8, "static": True}]),
    (6, "Перед самой деревней мама протянула мне сложенный листок. Сказала: прочитай. И запомни.", [
        {"k": "car", "cam": "in", "focus": (0.5, 0.55), "amt": 0.6},
        {"at": "прочитай", "k": "note", "show": 0, "cam": "in", "sfx": "flip"}]),
    (7, "Там было три правила. Первое: после заката из дома не выходи.", [
        {"k": "note", "show": 0, "cam": "in"},
        {"at": "первое", "k": "note", "show": 1, "cam": "in", "focus": (0.5, 0.35), "sfx": "thud"}]),
    (8, "Второе: если ночью тебя позовут по имени, не отвечай. Даже если это бабушка.", [
        {"k": "note", "show": 2, "cam": "in", "focus": (0.5, 0.5), "sfx": "thud"},
        {"at": "даже", "k": "note", "show": 2, "cam": "in", "focus": (0.5, 0.52), "amt": 0.5, "sfx": "sting"}]),
    (9, "Третье: дверь никому не открывай. Даже нам.", [
        {"k": "note", "show": 3, "cam": "in", "focus": (0.5, 0.65), "sfx": "thud"},
        {"at": "даже", "k": "note", "show": 3, "cam": "in", "focus": (0.5, 0.68), "amt": 0.6}]),
    (10, "Деревня оказалась пустой. Заколоченные окна, заросшие огороды. И только в последнем доме у леса горел свет.", [
        {"k": "set", "bg": "village", "cam": "r", "sfx": "engine"},
        {"at": "заколоченные", "k": "set", "bg": "village", "cam": "in", "focus": (0.25, 0.45), "amt": 0.5},
        {"at": "последнем", "k": "set", "bg": "village", "cam": "in", "focus": (0.85, 0.45), "amt": 0.6}]),
    (11, "Папа даже не заглушил мотор. Мама обняла меня так крепко, что стало больно. Прошептала: три ночи, сынок. Продержись три ночи. И машина уехала.", [
        {"k": "set", "bg": "house", "cam": "in", "car": 0.15, "sfx": "engine", "actors": [A("mom", 0.42, e="closed", m="frown"), BOY(0.5, e="wide", m="line")]},
        {"at": "прошептала", "k": "set", "bg": "house", "cam": "in", "focus": (0.46, 0.4), "amt": 0.5, "actors": [A("mom", 0.42, e="closed", m="frown"), BOY(0.5, e="wide", m="line")]},
        {"at": "машина", "k": "set", "bg": "house", "cam": "out", "car": "leave", "sfx": "engine", "actors": [BOY(0.5, e="wide", m="frown")]}]),
    (12, "Калитка скрипнула сама. На крыльце стояла маленькая старушка в цветастом платке.", [
        {"k": "set", "bg": "house", "cam": "in", "focus": (0.2, 0.6), "sfx": "creak", "actors": [BOY(0.35, e="wide", m="o")]},
        {"at": "крыльце", "k": "set", "bg": "house", "cam": "in", "focus": (0.62, 0.45), "amt": 0.4, "actors": [A("granny", 0.62, y=860, s=0.9), BOY(0.35, e="wide", m="o")]}]),
    (13, "Вырос-то как. Проходи, внучек, я пирожков напекла.", [
        {"k": "set", "bg": "house", "cam": "in", "focus": (0.6, 0.4), "amt": 0.45, "actors": [A("granny", 0.62, y=860, s=0.9, a="hips"), BOY(0.35, e="dot", m="line")]}], GR),
    (14, "Внутри пахло печкой и яблоками. Всё было бы уютно, если бы не одно но.", [
        {"k": "set", "bg": "kitchen", "cam": "r", "actors": [BOY(0.45, e="dot", m="smile")]},
        {"at": "если", "k": "set", "bg": "kitchen", "cam": "in", "amt": 0.2, "actors": [BOY(0.45, e="wide", m="line")]}]),
    (15, "Все зеркала в доме были завешаны тканью. А часы на стене стояли. Без пяти три.", [
        {"k": "set", "bg": "kitchen", "cam": "in", "focus": (0.86, 0.4), "amt": 0.6},
        {"at": "часы", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.62, 0.25), "amt": 0.8},
        {"at": "без", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.62, 0.185), "amt": 1.4, "sfx": "sting"}]),
    (16, "А ещё бабушка накрыла стол на троих. Хотя кроме нас в доме никого не было.", [
        {"k": "set", "bg": "kitchen", "cam": "in", "focus": (0.5, 0.6), "amt": 0.5, "actors": [A("granny", 0.3)]},
        {"at": "хотя", "k": "set", "bg": "kitchen", "cam": "out", "actors": [A("granny", 0.3), BOY(0.7, e="wide", m="o", flip=True)]}]),
    (17, "Я спросил, кого мы ждём. Бабушка улыбнулась и ответила:", [
        {"k": "set", "bg": "kitchen", "cam": "in", "actors": [A("granny", 0.3), BOY(0.7, e="dot", m="o", a="point", flip=True)]},
        {"at": "улыбнулась", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.3, 0.4), "amt": 0.6, "actors": [A("granny", 0.3, e="closed", m="smile")]}]),
    (18, "Никого, внучек. Это я по привычке.", [
        {"k": "set", "bg": "kitchen", "cam": "in", "focus": (0.3, 0.4), "amt": 0.8, "actors": [A("granny", 0.3, e="closed", m="smile")]}], GR),
    (19, "Первая ночь. Я проснулся от того, что на кухне кто-то разговаривал.", [
        {"k": "title", "text": "НОЧЬ ПЕРВАЯ", "cam": "in", "sfx": "sting"},
        {"at": "проснулся", "k": "set", "bg": "bedroom", "night": True, "cam": "in", "door": "light", "actors": [BOY(0.7, bed=True, e="wide", m="o")]}]),
    (20, "Один голос был бабушкин. А второй... второй был мой. Он повторял за ней каждое слово. Только чуть позже.", [
        {"k": "set", "bg": "door", "night": True, "cam": "in", "door": "light"},
        {"at": "второй#2", "k": "set", "bg": "bedroom", "night": True, "cam": "in", "focus": (0.7, 0.5), "amt": 0.5, "door": "light", "sfx": "sting", "actors": [BOY(0.7, bed=True, e="shock", m="o", sweat=True)]},
        {"at": "повторял", "k": "set", "bg": "door", "night": True, "cam": "in", "amt": 0.4, "door": "feet", "sfx": "heart"}]),
    (21, "Я натянул одеяло на голову и не дышал до самого утра.", [
        {"k": "set", "bg": "bedroom", "night": True, "cam": "in", "focus": (0.7, 0.6), "amt": 0.3, "actors": [BOY(0.7, bed="hide")], "sfx": "heart"}]),
    (22, "Днём я сбежал к единственному живому дому в деревне. Там у забора сидел мальчишка, Петька.", [
        {"k": "set", "bg": "fence", "cam": "r", "sfx": "birds", "actors": [BOY(0.3, walk=(0.1, 0.35), e="dot", m="line")]},
        {"at": "петька", "k": "set", "bg": "fence", "cam": "in", "focus": (0.65, 0.5), "amt": 0.3, "actors": [BOY(0.35, e="dot", m="line"), A("petka", 0.65, m="smile", flip=True)]}]),
    (23, "Я сказал, что живу у бабушки в крайнем доме. Петька аж побледнел.", [
        {"k": "set", "bg": "fence", "cam": "in", "actors": [BOY(0.35, e="dot", m="smile", a="point"), A("petka", 0.65, m="smile", flip=True)]},
        {"at": "побледнел", "k": "set", "bg": "fence", "cam": "in", "focus": (0.65, 0.4), "amt": 0.6, "sfx": "sting", "actors": [BOY(0.35), A("petka", 0.65, e="shock", m="o", sweat=True, flip=True)]}]),
    (24, "В крайнем? Так бабка Нюра померла. Двенадцать лет назад. Мне мамка рассказывала.", [
        {"k": "set", "bg": "fence", "cam": "in", "focus": (0.65, 0.4), "amt": 0.4, "actors": [BOY(0.35, e="wide", m="o"), A("petka", 0.65, e="wide", m="o", a="point", flip=True)]},
        {"at": "двенадцать", "k": "set", "bg": "fence", "cam": "in", "focus": (0.35, 0.4), "amt": 0.6, "actors": [BOY(0.35, e="shock", m="scream", a="up", sweat=True), A("petka", 0.65, e="wide", m="o", flip=True)]}], PET),
    (25, "Двенадцать лет. Ровно столько, сколько мне.", [
        {"k": "title", "text": "12 ЛЕТ", "cam": "in", "sfx": "sting"}]),
    (26, "Я позвонил маме. Она ответила сразу, будто ждала звонка.", [
        {"k": "phone", "name": "Мама", "cam": "in", "sfx": "ring"},
        {"at": "ответила", "k": "phone", "name": "Мама", "call": True, "cam": "in", "amt": 0.3}]),
    (27, "Знаю, сынок. Слушайся бабушку. Она тебя защитит.", [
        {"k": "phone", "name": "Мама", "call": True, "cam": "in", "amt": 0.4},
        {"at": "защитит", "k": "set", "bg": "fence", "cam": "in", "focus": (0.35, 0.4), "amt": 0.5, "actors": [BOY(0.35, e="wide", m="line", a="rope")]}], MOM),
    (28, "И связь оборвалась.", [
        {"k": "phone", "name": "Мама", "lost": True, "cam": "in", "sfx": "thud"}]),
    (29, "Вторая ночь. Ровно без пяти три меня позвали из кухни.", [
        {"k": "title", "text": "НОЧЬ ВТОРАЯ", "cam": "in", "sfx": "sting"},
        {"at": "ровно", "k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.62, 0.185), "amt": 1.2, "sfx": "tick"},
        {"at": "позвали", "k": "set", "bg": "bedroom", "night": True, "door": "light", "cam": "in", "actors": [BOY(0.7, bed=True, e="wide", m="o")]}]),
    (30, "Внучек, иди сюда. Пирожки остыли.", [
        {"k": "set", "bg": "door", "night": True, "door": "light", "cam": "in", "amt": 0.3},
        {"at": "пирожки", "k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.3, 0.4), "amt": 0.5, "actors": [A("other", 0.3)]}], OTHER),
    (31, "Это был бабушкин голос. Я уже хотел ответить. Но тут из-за двери моей комнаты кто-то прошептал:", [
        {"k": "set", "bg": "bedroom", "night": True, "door": "light", "cam": "in", "actors": [BOY(0.7, bed=True, e="dot", m="o")]},
        {"at": "но", "k": "set", "bg": "door", "night": True, "door": "feet", "cam": "in", "amt": 0.5, "sfx": "sting"}]),
    (32, "Не отвечай. Это не я.", [
        {"k": "set", "bg": "door", "night": True, "door": "feet", "cam": "in", "amt": 0.8}], GRW),
    (33, "Два голоса. Одна бабушка на кухне. Другая за дверью. И обе звали меня по имени.", [
        {"k": "split", "cam": "in", "amt": 0.1},
        {"at": "одна", "k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.3, 0.4), "amt": 0.5, "actors": [A("other", 0.3)]},
        {"at": "другая", "k": "set", "bg": "door", "night": True, "door": "feet", "cam": "in", "amt": 0.5},
        {"at": "обе", "k": "split", "cam": "in", "amt": 0.2, "sfx": "heart"}]),
    (34, "Я вспомнил второе правило. Зажал рот ладонью и молчал.", [
        {"k": "note", "show": 2, "hl": 2, "cam": "in", "focus": (0.5, 0.5), "amt": 0.4, "sfx": "thud"},
        {"at": "зажал", "k": "set", "bg": "bedroom", "night": True, "cam": "in", "focus": (0.7, 0.45), "amt": 0.7, "sfx": "heart", "actors": [BOY(0.7, bed=True, e="shock", m="line", a="rope", sweat=True)]}]),
    (35, "Голос на кухне становился всё злее. Потом затих. А потом в окно постучали. Три раза.", [
        {"k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.3, 0.4), "amt": 0.6, "shake": 0.2, "actors": [A("other", 0.3, e="void", m="grin", a="up")]},
        {"at": "затих", "k": "set", "bg": "bedroom", "night": True, "cam": "out", "actors": [BOY(0.7, bed=True, e="wide", m="line")]},
        {"at": "постучали", "k": "set", "bg": "bedroom", "night": True, "cam": "in", "focus": (0.4, 0.35), "amt": 0.5, "sfx": "knock", "shake": 0.1, "hand": True, "actors": [BOY(0.7, bed=True, e="shock", m="o")]}]),
    (36, "Утром бабушка сидела у печки бледная, как простыня. И наконец рассказала правду.", [
        {"k": "set", "bg": "kitchen", "cam": "in", "sfx": "birds", "actors": [A("granny", 0.25, e="closed", m="frown", body=(190, 180, 180)), BOY(0.7, flip=True, m="line")]},
        {"at": "правду", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.25, 0.4), "amt": 0.6, "actors": [A("granny", 0.25, e="dot", m="line", body=(190, 180, 180))]}]),
    (37, "Когда ты родился, за тобой пришёл Тот, кто зовёт. Он говорит голосами родных. Кто откликнется, того и забирает.", [
        {"k": "flash", "cam": "in", "sfx": "sting"},
        {"at": "говорит", "k": "flash", "cam": "in", "focus": (0.75, 0.4), "amt": 0.5, "voices": True},
        {"at": "откликнется", "k": "flash", "cam": "in", "focus": (0.75, 0.35), "amt": 0.9, "shake": 0.3}], GR),
    (38, "Я тогда ответила ему вместо тебя. И осталась тут, между. Сторожить.", [
        {"k": "flash", "cam": "in", "focus": (0.35, 0.45), "amt": 0.5, "shield": True},
        {"at": "осталась", "k": "set", "bg": "house", "night": True, "cam": "out", "actors": [A("granny", 0.62, y=860, s=0.9, e="dot", m="line")]}], GR),
    (39, "Каждые двенадцать лет он возвращается. Если ты продержишься в моём доме три ночи, он больше никогда тебя не найдёт.", [
        {"k": "title", "text": "КАЖДЫЕ 12 ЛЕТ", "cam": "in"},
        {"at": "продержишься", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.4, 0.4), "amt": 0.4, "actors": [A("granny", 0.3, e="dot", m="line", a="point", body=(190, 180, 180)), BOY(0.6, e="wide", m="line", flip=True)]}], GR),
    (40, "Так вот кто был на фотографии. Вот чьё лицо вырезали.", [
        {"k": "photo", "cut": True, "cam": "in", "focus": (0.6, 0.38), "amt": 0.5},
        {"at": "чьё", "k": "photo", "cut": "ghost", "cam": "in", "focus": (0.6, 0.38), "amt": 0.9, "sfx": "sting"}]),
    (41, "Третья ночь была самой длинной. Ровно без пяти три зазвонил телефон. Мама.", [
        {"k": "title", "text": "НОЧЬ ТРЕТЬЯ", "cam": "in", "sfx": "sting"},
        {"at": "ровно", "k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.62, 0.185), "amt": 1.2, "sfx": "tick"},
        {"at": "зазвонил", "k": "phone", "name": "Мама", "night": True, "cam": "in", "sfx": "ring"}]),
    (42, "Сынок, мы приехали за тобой. Открой дверь, на улице холодно.", [
        {"k": "phone", "name": "Мама", "call": True, "night": True, "cam": "in", "amt": 0.3},
        {"at": "открой", "k": "set", "bg": "door", "night": True, "cam": "in", "amt": 0.5, "sfx": "knock"}], MOMX),
    (43, "Я посмотрел в окно. У калитки стояла наша машина. И мама с папой махали мне рукой.", [
        {"k": "winout", "cam": "in", "amt": 0.1},
        {"at": "машина", "k": "winout", "cam": "in", "focus": (0.45, 0.55), "amt": 0.5},
        {"at": "махали", "k": "winout", "cam": "in", "focus": (0.5, 0.5), "amt": 0.7, "wave": True}]),
    (44, "Только у них не было лиц. Гладкие, как вырезанное место на фотографии.", [
        {"k": "winout", "cam": "in", "focus": (0.5, 0.45), "amt": 1.3, "wave": True, "sfx": "sting", "shake": 0.1},
        {"at": "гладкие", "k": "photo", "cut": True, "cam": "in", "focus": (0.6, 0.38), "amt": 0.9}]),
    (45, "Бабушка встала между мной и дверью. Сказала тихо: не смотри. И погасила свет.", [
        {"k": "set", "bg": "door", "night": True, "cam": "in", "actors": [A("granny", 0.5, a="up", e="angry", m="line")]},
        {"at": "погасила", "k": "black", "cam": "in", "sfx": "thud"}]),
    (46, "Они стучали до самого рассвета. Я считал удары и молился, чтобы часы наконец пошли.", [
        {"k": "set", "bg": "door", "night": True, "cam": "in", "shake": 0.1, "dark": True, "sfx": "knock knock@2.2"},
        {"at": "считал", "k": "set", "bg": "bedroom", "night": True, "dark": True, "cam": "in", "focus": (0.7, 0.5), "amt": 0.5, "sfx": "heart", "actors": [BOY(0.7, bed=True, e="closed", m="frown", sweat=True)]},
        {"at": "часы", "k": "set", "bg": "kitchen", "night": True, "cam": "in", "focus": (0.62, 0.185), "amt": 1.3}]),
    (47, "С первыми петухами стук прекратился. А часы на стене вдруг затикали.", [
        {"k": "set", "bg": "house", "dawn": True, "cam": "out", "sfx": "birds"},
        {"at": "часы", "k": "set", "bg": "kitchen", "cam": "in", "focus": (0.62, 0.185), "amt": 1.2, "tick": True, "sfx": "tick"}]),
    (48, "Утром приехали настоящие родители. Мама плакала и не отпускала меня.", [
        {"k": "set", "bg": "house", "dawn": True, "car": 0.15, "cam": "in", "sfx": "engine", "actors": [A("dad", 0.32), A("mom", 0.44, e="closed", m="frown"), BOY(0.52, e="closed", m="smile")]},
        {"at": "плакала", "k": "set", "bg": "house", "dawn": True, "car": 0.15, "cam": "in", "focus": (0.48, 0.4), "amt": 0.6, "actors": [A("mom", 0.44, e="closed", m="frown", tears=True), BOY(0.52, e="closed", m="smile")]}]),
    (49, "Я обернулся, чтобы позвать бабушку. Но дом был пустой. Пыль, паутина, разбитые окна. Будто в нём никто не жил двенадцать лет.", [
        {"k": "set", "bg": "house", "dawn": True, "ruin": True, "cam": "in", "focus": (0.6, 0.45), "actors": [BOY(0.4, flip=True, e="wide", m="o")]},
        {"at": "пыль", "k": "set", "bg": "kitchen", "ruin": True, "cam": "r"},
        {"at": "будто", "k": "set", "bg": "kitchen", "ruin": True, "cam": "in", "amt": 0.3, "actors": [BOY(0.7, e="wide", m="o", flip=True)]}]),
    (50, "Только на столе стояла тарелка с пирожками. Ещё тёплыми.", [
        {"k": "set", "bg": "kitchen", "ruin": True, "pies": True, "cam": "in", "focus": (0.5, 0.62), "amt": 0.9}]),
    (51, "Дома я открыл альбом. На той фотографии больше не было дыры. Рядом с мамой стояла бабушка в цветастом платке. И улыбалась.", [
        {"k": "photo", "cut": True, "cam": "in"},
        {"at": "больше", "k": "photo", "cut": False, "cam": "in", "focus": (0.6, 0.38), "amt": 0.4, "sfx": "ding"},
        {"at": "улыбалась", "k": "photo", "cut": False, "cam": "in", "focus": (0.6, 0.38), "amt": 0.9}]),
    (52, "Мама до сих пор говорит, что бабушки у меня нет. Но каждый год в мой день рождения на подоконнике появляются тёплые пирожки.", [
        {"k": "set", "bg": "flat", "cam": "in", "actors": [A("mom", 0.35, m="line"), BOY(0.6, flip=True, m="line")]},
        {"at": "каждый", "k": "sill", "cam": "in", "amt": 0.4}]),
    (53, "А вы бы ответили, если бы вас позвали ночью голосом родных? Пишите в комментариях.", [
        {"k": "set", "bg": "house", "night": True, "cam": "in", "focus": (0.62, 0.4), "amt": 0.3, "actors": [A("granny", 0.62, y=860, s=0.9, e="dot", m="smile")]},
        {"at": "пишите", "k": "title", "text": "А ВЫ БЫ ОТВЕТИЛИ?", "cam": "in"}]),
]
YELLOW = {"бабушка", "бабушку", "бабушкин", "бабушки", "лето", "альбоме", "фотография", "третий", "лицо", "листок", "три", "правила", "первое",
          "второе", "третье", "заката", "имени", "свет", "последнем", "калитка", "платке", "пирожков", "пирожки", "зеркала", "часы", "пяти",
          "троих", "ночь", "первая", "петька", "двенадцать", "мама", "нюра", "ночи", "окно", "голосами", "родных", "сторожить", "рассвета", "пирожками", "тёплыми", "подоконнике", "улыбалась"}
RED = {"вырезано", "ножницами", "никого", "мой", "померла", "оборвалась", "не", "отвечай", "злее", "постучали", "забирает", "лиц", "пустой", "открой", "вырезали"}
META = {"title": "Я не знал, что у меня есть бабушка. Родители отправили меня к ней на лето",
        "desc": "Страшная история в мультике: три правила, три ночи и голоса родных. Вымысел. #страшилки #страшныеистории #мистика #бабушка #анимация"}
