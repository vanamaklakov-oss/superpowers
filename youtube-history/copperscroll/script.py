# The Copper Scroll (3Q15). Sources: Wikipedia "Copper Scroll"; USC West Semitic Research Project "The Copper Scroll";
# Hebrew University Virtual Qumran; Biblical Archaeology Society. Found 14 Mar 1952 in Cave 3 at Qumran; engraved on
# copper; too corroded to unroll, cut into strips (1955–56) to be read; an inventory of ~64 hiding places, 63 with gold
# and silver (one entry: 900 talents); descriptions like cisterns, tombs, steps; John Allegro and others searched but
# found nothing; explanations: removed long ago, never existed, or still hidden.
G = "digger"
SCENES = [
 (0, "Список сокровищ на меди. Ни одно не найдено.", [
    dict(bg="treasure", cast=[], cam=(1.5, 540, 1000), hook="КАРТА СОКРОВИЩ\nИЗ МЕДИ")]),
 (1, "Тысяча девятьсот пятьдесят второй год. Пещеры у Мёртвого моря, где уже нашли знаменитые древние свитки.", [
    dict(bg="cliffs", cast=[(G, 540, dict(expr="happy", arm_r=120))], cam=(1.2, 540, 1050), sign="1952")]),
 (2, "В одной из пещер археологи находят странный свиток. Не из кожи, а из меди.", [
    dict(bg="cave", cast=[(G, 540, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="cave", cast=[(G, 540, dict(expr="neutral"))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (3, "Металл так окислился, что развернуть его было невозможно.", [
    dict(bg="office", cast=[(G, 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 960))]),
 (4, "Через несколько лет свиток аккуратно разрезали на полосы и наконец прочитали.", [
    dict(bg="office", cast=[("doctor", 540, dict(expr="neutral", arm_r=100))], cam=(1.3, 540, 1050)),
    dict(bg="office", cast=[("doctor", 540, dict(expr="shock"))], cam=(1.9, 540, 900))]),
 (5, "Это оказался не священный текст, а список.", [
    dict(bg="office", cast=[("doctor", 540, dict(expr="smug", talk=True))], cam=(1.5, 540, 970), fx="book", book_text="СПИСОК")]),
 (6, "Шестьдесят с лишним тайников с золотом и серебром.", [
    dict(bg="treasure", cast=[(G, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050), sign="64 ТАЙНИКА", fx="money")]),
 (7, "Если перевести древние меры, получаются тонны драгоценного металла.", [
    dict(bg="treasure", cast=[(G, 540, dict(expr="shock", sweat=True))], cam=(1.8, 540, 930), fx="calc", calc_lines=["ЗОЛОТО", "СЕРЕБРО", "= ТОННЫ?"])]),
 (8, "Описания такие: под ступенями, у гробницы, в цистерне.", [
    dict(bg="cliffs", cast=[(G, 540, dict(expr="talk", talk=True, arm_r=90))], cam=(1.3, 540, 1050))]),
 (9, "Но ориентиры давно исчезли. Искатели годами копали в указанных местах и не нашли ни монеты.", [
    dict(bg="dig", cast=[(G, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1050)),
    dict(bg="dig", cast=[(G, 540, dict(expr="angry", rage=0.8, steam=True))], cam=(1.9, 540, 900))]),
 (10, "Может, сокровища давно забрали. Может, их не было вовсе. А может, они всё ещё там.", [
    dict(bg="cliffs", cast=[(G, 540, dict(expr="neutral"))], cam=(1.4, 540, 1000), bubble=(0, "?")),
    dict(bg="treasure", cast=[], cam=(2.0, 540, 900))]),
]
