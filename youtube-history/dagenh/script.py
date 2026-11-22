# Dagen H, Sweden, 3 September 1967. Sources: Wikipedia "Dagen H" and "1955 Swedish driving side referendum";
# Popular Science; Amusing Planet; Sveriges Radio. 1955 referendum: ~83 % against; switch made anyway (decided 1963).
# Non-essential traffic banned overnight; cars moved to the right at 04:50–05:00. Accidents fell at first (157 minor on
# the day; Monday after: 125 vs 130–198 usual), back to normal within weeks (~6 weeks by some accounts).
D, E, O = "driver", "driver2", "official"
SCENES = [
 (1, "Целая страна за одну ночь пересела на другую сторону дороги.", [
    dict(bg="highway", cast=[(D, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="highway", cast=[(D, 540, dict(expr="worried", lean=6))], cam=(1.9, 540, 900))]),
 (2, "До шестьдесят седьмого года шведы ездили по левой стороне. А все соседи — по правой.", [
    dict(bg="town", cast=[(D, 540, dict(expr="happy", arm_l=140, talk=True))], cam=(1.2, 540, 1050), sign="ШВЕЦИЯ:\nСЛЕВА"),
    dict(bg="town", cast=[(E, 540, dict(expr="smug", arm_r=140))], cam=(1.2, 540, 1050), sign="СОСЕДИ:\nСПРАВА")]),
 (3, "В пятьдесят пятом году провели референдум. Восемьдесят три процента сказали: не надо.", [
    dict(bg="town", cast=[(D, 330, dict(expr="angry", talk=True)), (E, 750, dict(expr="angry", arm_l=120))], cam=(1.15, 540, 1000), sign="83% ПРОТИВ"),
    dict(bg="office", cast=[(O, 540, dict(expr="neutral"))], cam=(1.6, 540, 960))]),
 (4, "Но правительство всё равно решило переходить.", [
    dict(bg="office", cast=[(O, 540, dict(expr="smug", arm_r=90, talk=True))], cam=(1.6, 540, 960), fx="stamp", stamp_text="ПЕРЕХОДИМ")]),
 (5, "Третьего сентября тысяча девятьсот шестьдесят седьмого года, рано утром, движение по стране почти остановили.", [
    dict(bg="highway", cast=[(O, 540, dict(expr="neutral", arm_l=150))], cam=(1.2, 540, 1050), sign="3.09.1967"),
    dict(bg="highway", cast=[], cam=(1.4, 540, 1000))]),
 (6, "И все машины медленно переехали с левой полосы на правую.", [
    dict(bg="highway", cast=[(D, 300, dict(expr="worried", sweat=True, lean=-6))], cam=(1.1, 540, 1000)),
    dict(bg="highway", cast=[(D, 780, dict(expr="happy", lean=6))], cam=(1.1, 540, 1000))]),
 (7, "Все ждали аварий и хаоса.", [
    dict(bg="kitchen", cast=[(E, 540, dict(expr="shock", sweat=True))], cam=(1.8, 540, 930))]),
 (8, "А случилось обратное: в первые дни аварий стало даже меньше.", [
    dict(bg="office", cast=[(O, 540, dict(expr="shock"))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ЖДАЛИ: ХАОС", "ВЫШЛО: МЕНЬШЕ АВАРИЙ"]),
    dict(bg="office", cast=[(O, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.25, 540, 1050))]),
 (9, "Водители так боялись ошибиться, что ездили предельно осторожно.", [
    dict(bg="highway", cast=[(D, 540, dict(expr="worried", sweat=True))], cam=(1.9, 540, 900))]),
 (10, "Правда, через несколько недель всё вернулось к обычному уровню.", [
    dict(bg="town", cast=[(E, 540, dict(expr="smug"))], cam=(1.3, 540, 1050))]),
 (11, "Оказалось, лучший способ сделать водителей осторожными — немного их напугать.", [
    dict(bg="highway", cast=[(D, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
