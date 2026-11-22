# The Voynich manuscript. Sources: Wikipedia "Voynich manuscript"; University of Arizona / EurekAlert (2011) on the 2009
# radiocarbon dating (Greg Hodgins; four leaves; 1404–1438); LiveScience; Yale Beinecke Library (MS 408, held since 1969).
# Bought by Wilfrid Voynich in 1912; studied by cryptographers incl. William Friedman. ~240 pages survive.
V, S = "voynich", "scholar"
SCENES = [
 (1, "Есть книга, которую не смог прочитать ни один человек на Земле.", [
    dict(bg="library", cast=[(S, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1100), fx="book", book_text="???"),
    dict(bg="library", cast=[(S, 540, dict(expr="shock"))], cam=(2.0, 540, 900), bubble=(0, "?"))]),
 (2, "Это рукопись Войнича. Около двухсот сорока страниц на неизвестном языке, с рисунками странных растений и звёзд.", [
    dict(bg="library", cast=[(S, 540, dict(expr="neutral", arm_r=90, talk=True))], cam=(1.2, 540, 1050), sign="РУКОПИСЬ\nВОЙНИЧА"),
    dict(bg="room", cast=[(S, 540, dict(expr="worried"))], cam=(1.8, 540, 930), sign="~240 СТРАНИЦ")]),
 (3, "В тысяча девятьсот двенадцатом году её купил торговец старинными книгами Вилфрид Войнич.", [
    dict(bg="office", cast=[(V, 540, dict(expr="happy", arm_r=120))], cam=(1.3, 540, 1050), sign="1912"),
    dict(bg="office", cast=[(V, 540, dict(expr="smug"))], cam=(1.8, 540, 930), fx="stamp", stamp_text="КУПЛЕНО")]),
 (4, "С тех пор её пытались расшифровать лингвисты, математики и военные криптографы.", [
    dict(bg="library", cast=[(S, 300, dict(expr="worried", talk=True)), ("doctor", 780, dict(expr="angry", rage=0.5, steam=True))], cam=(1.1, 540, 1000)),
    dict(bg="office", cast=[("major", 540, dict(expr="neutral", arm_r=80))], cam=(1.6, 540, 960), fx="calc", calc_lines=["ШИФР?", "ЯЗЫК?", "= ???"])]),
 (5, "Даже знаменитые взломщики военных шифров сдались.", [
    dict(bg="office", cast=[("major", 540, dict(expr="angry", rage=0.9, steam=True))], cam=(2.0, 540, 900))]),
 (6, "Многие решили, что это подделка. И сочинил её сам Войнич.", [
    dict(bg="library", cast=[(S, 330, dict(expr="smug", talk=True, arm_r=110)), (V, 750, dict(expr="shock", sweat=True))], cam=(1.15, 540, 1000)),
    dict(bg="room", cast=[(V, 540, dict(expr="worried"))], cam=(1.9, 540, 900))]),
 (7, "Но в две тысячи девятом году пергамент проверили радиоуглеродным методом.", [
    dict(bg="office", cast=[(S, 540, dict(expr="neutral", arm_r=100))], cam=(1.3, 540, 1050), sign="2009")]),
 (8, "Оказалось, его сделали между тысяча четыреста четвёртым и тысяча четыреста тридцать восьмым годом.", [
    dict(bg="office", cast=[(S, 540, dict(expr="shock"))], cam=(1.3, 540, 1050), sign="1404–1438"),
    dict(bg="library", cast=[(S, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (9, "За пятьсот лет до того, как Войнич её купил.", [
    dict(bg="room", cast=[(V, 540, dict(expr="smug", arm_l=120))], cam=(1.6, 540, 960), fx="stamp", stamp_text="НЕ ПОДДЕЛКА")]),
 (10, "Значит, книгу подделал не Войнич. Но кто её написал и что в ней сказано, до сих пор неизвестно.", [
    dict(bg="library", cast=[(S, 300, dict(expr="worried")), (V, 780, dict(expr="worried"))], cam=(1.1, 540, 1000), bubble=(0, "?")),
    dict(bg="dark", cast=[(S, 540, dict(expr="neutral"))], cam=(1.8, 540, 930), bubble=(0, "?"))]),
 (11, "Сегодня рукопись хранится в библиотеке Йельского университета. И всё ещё молчит.", [
    dict(bg="library", cast=[], cam=(1.3, 540, 1000)),
    dict(bg="library", cast=[(S, 540, dict(expr="neutral"))], cam=(2.2, 540, 870))]),
]
