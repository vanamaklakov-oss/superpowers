# The dancing plague of 1518, Strasbourg. Sources: Britannica "Dancing plague of 1518"; National Geographic;
# History.com (E. Andrews); Public Domain Review; John Waller, "A Time to Dance, a Time to Die" (2008). Began July 1518
# with a woman (named Frau Troffea in most chronicles); ~3 dozen within a week; reports up to ~400 within a month;
# authorities hired musicians and set up a stage/guildhalls; deaths are reported but disputed; in September dancers were
# taken to the shrine of St Vitus in the mountains; leading theory: stress-induced mass psychogenic illness (Waller).
D, E, M = "dancer", "dancer2", "mayor"
SCENES = [
 (0, "Говорят, они танцевали до смерти.", [
    dict(bg="street", cast=[("dancer", 540, dict(expr="shock", arm_l=160, arm_r=160, lean=8, sweat=True))], cam=(1.5, 540, 1000), hook="ОНИ ТАНЦЕВАЛИ\nДО СМЕРТИ")]),
 (1, "В одном городе люди начали танцевать. И не могли остановиться.", [
    dict(bg="street", cast=[(D, 330, dict(expr="happy", arm_l=150, arm_r=150, bob=10)), (E, 750, dict(expr="worried", arm_l=150, arm_r=150, sweat=True))], cam=(1.1, 540, 1050)),
    dict(bg="street", cast=[(D, 540, dict(expr="shock", arm_l=160, arm_r=160, lean=8, sweat=True))], cam=(1.9, 540, 900))]),
 (2, "Страсбург, июль тысяча пятьсот восемнадцатого года. По хроникам, одна женщина вышла на улицу и начала танцевать.", [
    dict(bg="street", cast=[(D, 540, dict(expr="neutral"))], cam=(1.2, 540, 1050), sign="1518"),
    dict(bg="street", cast=[(D, 540, dict(expr="happy", arm_l=150, arm_r=150, lean=-6))], cam=(1.7, 540, 950))]),
 (3, "Она танцевала несколько дней подряд.", [
    dict(bg="street", cast=[(D, 540, dict(expr="worried", arm_l=160, arm_r=140, lean=6, sweat=True))], cam=(1.6, 540, 960))]),
 (4, "Через неделю к ней присоединились около трёх десятков человек.", [
    dict(bg="square", cast=[(D, 280, dict(expr="happy", arm_l=150, arm_r=150, lean=-5)), (E, 540, dict(expr="worried", arm_l=150, arm_r=150, lean=5)), ("villager", 800, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.0, 540, 1000), sign="~30")]),
 (5, "А через месяц, по некоторым данным, танцующих было уже до четырёхсот.", [
    dict(bg="square", cast=[(E, 330, dict(expr="worried", arm_l=160, arm_r=160, sweat=True)), ("villager2", 750, dict(expr="shock", arm_l=160, arm_r=160))], cam=(1.1, 540, 1000), sign="ДО 400")]),
 (6, "Власти решили, что это болезнь. И лечить её надо танцами.", [
    dict(bg="hall", cast=[(M, 540, dict(expr="smug", talk=True, arm_r=100))], cam=(1.4, 540, 1000), bubble=(0, "on")),
    dict(bg="hall", cast=[(M, 540, dict(expr="happy"))], cam=(1.8, 540, 930), fx="stamp", stamp_text="ТАНЦЕВАТЬ")]),
 (7, "Наняли музыкантов и даже построили сцену, чтобы люди вытанцевали болезнь.", [
    dict(bg="square", cast=[("friend2", 540, dict(expr="happy", arm_r=120, arm_l=60))], cam=(1.3, 540, 1050)),
    dict(bg="square", cast=[(D, 330, dict(expr="worried", arm_l=150, arm_r=150, sweat=True)), (E, 750, dict(expr="worried", arm_l=150, arm_r=150, sweat=True))], cam=(1.15, 540, 1000))]),
 (8, "Стало только хуже. Танцующих становилось всё больше.", [
    dict(bg="hall", cast=[(M, 540, dict(expr="shock", sweat=True))], cam=(1.9, 540, 900))]),
 (9, "По некоторым хроникам, люди падали от изнеможения.", [
    dict(bg="street", cast=[(E, 540, dict(expr="worried", sweat=True, lean=10))], cam=(1.6, 540, 960))]),
 (10, "В сентябре танцоров отвезли молиться в горную часовню святого Вита. И эпидемия закончилась.", [
    dict(bg="chapel", cast=[(D, 330, dict(expr="neutral")), (E, 750, dict(expr="neutral"))], cam=(1.1, 540, 1000)),
    dict(bg="chapel", cast=[(D, 540, dict(expr="happy"))], cam=(1.7, 540, 950))]),
 (11, "Что это было? По одной из версий — массовая истерия от голода и страха. Но точного ответа нет.", [
    dict(bg="room", cast=[("doctor", 540, dict(expr="neutral", talk=True))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ГОЛОД", "СТРАХ", "= ИСТЕРИЯ?"]),
    dict(bg="room", cast=[("doctor", 540, dict(expr="worried"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
