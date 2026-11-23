# The Amber Room. Sources: Smithsonian Magazine "A brief history of the Amber Room"; Wikipedia "Amber Room"; GIA Gems &
# Gemology (Winter 2018) "History and reconstruction of the Amber Room"; History.com; History Hit. Begun in Prussia
# (1701, for Frederick I); given by Frederick William I to Peter I in 1716; later installed in the Catherine Palace
# (Tsarskoye Selo); ~6 tonnes of amber; dismantled by German troops in 36 hours (1941) and shown at Königsberg Castle;
# vanished 1944–45; theories: destroyed in the castle (Scott-Clark & Levy 2004) or hidden; reconstruction 1979–2003.
SCENES = [
 (0, "Шесть тонн янтаря исчезли без следа.", [
    dict(bg="amber", cast=[], cam=(1.5, 540, 1000), hook="6 ТОНН ЯНТАРЯ\nИСЧЕЗЛИ")]),
 (1, "Целую комнату из янтаря украли во время войны. И её до сих пор ищут.", [
    dict(bg="amber", cast=[("scholar", 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="bunker", cast=[("scholar", 540, dict(expr="worried"))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (2, "Янтарную комнату начали делать в Пруссии в начале восемнадцатого века.", [
    dict(bg="palace", cast=[("fred", 540, dict(expr="smug", arm_r=110, talk=True))], cam=(1.2, 540, 1050), sign="1701")]),
 (3, "В тысяча семьсот шестнадцатом году прусский король подарил её Петру Первому.", [
    dict(bg="palace", cast=[("fred", 330, dict(expr="happy", arm_r=140)), ("peter", 750, dict(expr="shock"))], cam=(1.1, 540, 1000), sign="1716"),
    dict(bg="palace", cast=[("peter", 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.8, 540, 930))]),
 (4, "Позже её установили в Екатерининском дворце под Петербургом.", [
    dict(bg="amber", cast=[], cam=(1.2, 540, 1000))]),
 (5, "Шесть тонн янтаря, золото и зеркала. Её называли восьмым чудом света.", [
    dict(bg="amber", cast=[("scholar", 540, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050), sign="6 ТОНН"),
    dict(bg="amber", cast=[("scholar", 540, dict(expr="happy"))], cam=(1.9, 540, 900))]),
 (6, "В тысяча девятьсот сорок первом году германские войска разобрали её за тридцать шесть часов и увезли в Кёнигсберг.", [
    dict(bg="amber", cast=[("soldier", 330, dict(expr="neutral", arm_r=120)), ("soldier2", 750, dict(expr="neutral", arm_l=120))], cam=(1.1, 540, 1000), sign="36 ЧАСОВ"),
    dict(bg="castle", cast=[("soldier", 540, dict(expr="smug"))], cam=(1.6, 540, 960))]),
 (7, "Там её выставили в замке.", [
    dict(bg="castle", cast=[], cam=(1.3, 540, 1000))]),
 (8, "А в конце войны, при бомбардировках и штурме города, она исчезла.", [
    dict(bg="castle", cast=[("soldier", 540, dict(expr="shock", sweat=True))], cam=(1.4, 540, 1000)),
    dict(bg="castle", cast=[], cam=(1.9, 540, 900))]),
 (9, "С тех пор её искали в шахтах, бункерах и на дне озёр.", [
    dict(bg="bunker", cast=[("scholar", 540, dict(expr="neutral", arm_r=100))], cam=(1.3, 540, 1050)),
    dict(bg="lake", cast=[("scholar", 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 960))]),
 (10, "По одной из версий, она сгорела в замке. По другой, её где-то спрятали.", [
    dict(bg="castle", cast=[("doctor", 540, dict(expr="talk", talk=True, arm_r=90))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["СГОРЕЛА?", "СПРЯТАНА?"]),
    dict(bg="bunker", cast=[("doctor", 540, dict(expr="smug"))], cam=(1.8, 540, 930), bubble=(0, "?"))]),
 (11, "Сегодня во дворце стоит копия, которую делали больше двадцати лет. А оригинал так и не нашли.", [
    dict(bg="amber", cast=[("scholar", 540, dict(expr="neutral"))], cam=(1.3, 540, 1050), sign="КОПИЯ"),
    dict(bg="lake", cast=[], cam=(2.0, 540, 900))]),
]
