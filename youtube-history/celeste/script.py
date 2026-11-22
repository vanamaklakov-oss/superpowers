# The Mary Celeste, 1872. Sources: Royal Museums Greenwich "The mystery of the Mary Celeste"; Smithsonian Magazine;
# Britannica; History.com; Wikipedia "Mary Celeste". Found by the Dei Gratia ~400 miles east of the Azores, early Dec
# 1872; 1,701 barrels of (industrial) alcohol; yawl missing; Capt. Briggs, wife Sarah, daughter Sophia + 7 crew.
# Gibraltar inquiry found no foul play. Conan Doyle, "J. Habakuk Jephson's Statement" (1884), fictionalised the case
# ("Marie Celeste"). Leading theory (unproven): fear of alcohol fumes exploding -> abandoned ship.
C, X = "captain", "sailor"
SCENES = [
 (1, "В океане нашли корабль, на котором не было ни одного человека.", [
    dict(bg="sea", cast=[(X, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="sea", cast=[], cam=(1.6, 600, 950))]),
 (2, "Декабрь тысяча восемьсот семьдесят второго года. Восточнее Азорских островов моряки замечают странное судно.", [
    dict(bg="sea", cast=[(X, 540, dict(expr="neutral", arm_r=130, talk=True))], cam=(1.2, 540, 1050), sign="1872"),
    dict(bg="sea", cast=[(X, 540, dict(expr="worried"))], cam=(1.8, 540, 930), bubble=(0, "?"))]),
 (3, "Корабль дрейфует, на сигналы никто не отвечает.", [
    dict(bg="sea", cast=[(X, 540, dict(expr="talk", talk=True, arm_l=150, arm_r=150))], cam=(1.5, 540, 970))]),
 (4, "Это бригантина «Мэри Селест». Моряки поднимаются на борт.", [
    dict(bg="harbor", cast=[(X, 330, dict(expr="worried")), ("sailor2", 750, dict(expr="worried", sweat=True))], cam=(1.1, 540, 1000), sign="MARY CELESTE")]),
 (5, "Груз на месте: больше тысячи семисот бочек спирта. Вещи команды не тронуты.", [
    dict(bg="harbor", cast=[(X, 540, dict(expr="shock"))], cam=(1.3, 540, 1050), sign="1700+ БОЧЕК"),
    dict(bg="room", cast=[(X, 540, dict(expr="worried", sweat=True))], cam=(1.8, 540, 930))]),
 (6, "Пропали только люди. И одна шлюпка.", [
    dict(bg="sea", cast=[(X, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (7, "А на борту были капитан, его жена, маленькая дочь и семь матросов.", [
    dict(bg="harbor", cast=[(C, 540, dict(expr="happy", arm_r=110))], cam=(1.3, 540, 1050), sign="10 ЧЕЛОВЕК"),
    dict(bg="dark", cast=[(C, 540, dict(expr="neutral"))], cam=(1.8, 540, 930))]),
 (8, "Суд в Гибралтаре подозревал бунт, пиратов и обман страховой. Но доказательств не нашёл.", [
    dict(bg="office", cast=[("official", 540, dict(expr="angry", talk=True, arm_l=90))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["БУНТ?", "ПИРАТЫ?", "СТРАХОВКА?"]),
    dict(bg="office", cast=[("official", 540, dict(expr="worried"))], cam=(1.8, 540, 930), fx="stamp", stamp_text="НЕ ДОКАЗАНО")]),
 (9, "А через двенадцать лет молодой Артур Конан Дойл написал по этой истории рассказ.", [
    dict(bg="library", cast=[("doctor", 540, dict(expr="smug", talk=True, arm_l=70))], cam=(1.3, 540, 1050), fx="book", book_text="1884")]),
 (10, "Он придумал много деталей, и люди стали принимать выдумку за правду.", [
    dict(bg="library", cast=[("doctor", 540, dict(expr="happy", arm_r=120))], cam=(1.7, 540, 950)),
    dict(bg="library", cast=[("friend", 330, dict(expr="shock")), ("friend2", 750, dict(expr="shock"))], cam=(1.15, 540, 1000))]),
 (11, "По одной из версий, капитан испугался, что пары спирта взорвутся, и велел всем сесть в шлюпку. Но правды мы так и не знаем.", [
    dict(bg="sea", cast=[(C, 540, dict(expr="worried", sweat=True, talk=True))], cam=(1.4, 540, 1000)),
    dict(bg="dark", cast=[(C, 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
