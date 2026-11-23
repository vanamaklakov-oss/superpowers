# Rongorongo (Rapa Nui / Easter Island). Sources: Wikipedia "Rongorongo" and "Decipherment of rongorongo"; Smithsonian
# Magazine (2024) "Research reveals the natives of Easter Island invented a written language from scratch" (Ferrara et al.,
# Scientific Reports); Live Science; Omniglot. Eugène Eyraud's report (stay 1864, published 1866) of carved tablets in
# houses; 1862 Peruvian slave raids and epidemics devastated the population; ~25–27 objects survive, none on the island.
# Undeciphered; debated whether true writing or mnemonic proto-writing.
I, M = "islander", "missionary"
SCENES = [
 (1, "На острове посреди океана нашли письменность, которую до сих пор никто не может прочитать.", [
    dict(bg="island", cast=[("scholar", 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="museum", cast=[], cam=(1.6, 540, 960), bubble=None)]),
 (2, "Это остров Пасхи, знаменитый каменными головами.", [
    dict(bg="island", cast=[(I, 540, dict(expr="happy", arm_r=120))], cam=(1.2, 540, 1050), sign="ОСТРОВ ПАСХИ")]),
 (3, "В тысяча восемьсот шестьдесят четвёртом году миссионер Эжен Эйро увидел в домах местных жителей деревянные дощечки со странными знаками.", [
    dict(bg="hut", cast=[(M, 540, dict(expr="neutral", talk=True, arm_r=80))], cam=(1.2, 540, 1050), sign="1864"),
    dict(bg="hut", cast=[(M, 540, dict(expr="shock"))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (4, "Знаки — птицы, рыбы, люди, растения. Ряд за рядом.", [
    dict(bg="hut", cast=[(I, 540, dict(expr="smug", arm_l=100))], cam=(1.5, 540, 970))]),
 (5, "Их называют ронго-ронго.", [
    dict(bg="museum", cast=[("scholar", 540, dict(expr="neutral", talk=True))], cam=(1.6, 540, 960), sign="РОНГО-РОНГО")]),
 (6, "Но прочитать их уже никто не мог. Незадолго до этого остров пережил набеги работорговцев и эпидемии.", [
    dict(bg="ocean", cast=[(I, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1050)),
    dict(bg="ocean", cast=[], cam=(1.6, 540, 960))]),
 (7, "Многие дощечки пропали или были уничтожены.", [
    dict(bg="hut", cast=[(I, 540, dict(expr="shock"))], cam=(1.8, 540, 930))]),
 (8, "Сегодня их осталось около двух с половиной десятков. И ни одной на самом острове.", [
    dict(bg="museum", cast=[("scholar", 540, dict(expr="worried"))], cam=(1.3, 540, 1050), sign="~25"),
    dict(bg="island", cast=[(I, 540, dict(expr="worried", sweat=True))], cam=(1.9, 540, 900), sign="0")]),
 (9, "Учёные больше ста лет пытаются их расшифровать. Безуспешно.", [
    dict(bg="library", cast=[("scholar", 330, dict(expr="angry", talk=True)), ("doctor", 750, dict(expr="worried", sweat=True))], cam=(1.15, 540, 1000), fx="calc", calc_lines=["СЛОВА?", "СЛОГИ?", "= ???"])]),
 (10, "Неизвестно даже, настоящее ли это письмо или подсказки для певцов.", [
    dict(bg="library", cast=[("scholar", 540, dict(expr="neutral"))], cam=(1.5, 540, 970), bubble=(0, "?"))]),
 (11, "По мнению учёных, если это письмо, его придумали на острове с нуля. Таких случаев в истории единицы.", [
    dict(bg="island", cast=[(I, 540, dict(expr="smug", arm_r=110))], cam=(1.3, 540, 1050)),
    dict(bg="museum", cast=[], cam=(2.0, 540, 900))]),
]
