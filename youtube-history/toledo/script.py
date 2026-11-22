# The Toledo War, 1835–36. Sources: Wikipedia "Toledo War"; Michigan DMVA "The Toledo War"; History.com (E. Andrews);
# Library of Congress Maps blog "If you seek a pleasant peninsula, forget Toledo"; WorldAtlas. Mostly bloodless; one
# sheriff (Joseph Wood) lightly wounded. Congress made statehood conditional on giving up the strip; Michigan got the
# western Upper Peninsula, accepted Dec 1836 ("Frostbitten Convention"). Michigan led US copper output 1847–1887.
O, M = "ohio", "mich"
SCENES = [
 (1, "Мичиган проиграл спор за один город. И получил в награду край, полный меди.", [
    dict(bg="town", cast=[(M, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="mine", cast=[(M, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.9, 540, 900))]),
 (2, "Тысяча восемьсот тридцать пятый год. Огайо и Мичиган спорят о полоске земли с городом Толедо.", [
    dict(bg="town", cast=[(O, 330, dict(expr="angry", talk=True, arm_r=90)), (M, 750, dict(expr="angry", arm_l=90))], cam=(1.1, 540, 1000), sign="1835"),
    dict(bg="town", cast=[(O, 540, dict(expr="smug"))], cam=(1.8, 540, 930))]),
 (3, "Старые карты нарисовали с ошибкой, и каждая сторона считала Толедо своим.", [
    dict(bg="congress", cast=[(M, 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1050), bubble=(0, "?"))]),
 (4, "Обе стороны собрали ополчение и вышли к границе.", [
    dict(bg="forest", cast=[(O, 330, dict(expr="angry", rage=0.6, steam=True)), (M, 750, dict(expr="angry", rage=0.6, steam=True))], cam=(1.1, 540, 1000)),
    dict(bg="forest", cast=[("soldier", 540, dict(expr="worried", sweat=True))], cam=(1.8, 540, 930))]),
 (5, "Но войны почти не случилось. Единственным пострадавшим стал один шериф, и тот легко.", [
    dict(bg="forest", cast=[("soldier", 540, dict(expr="shock"))], cam=(1.4, 540, 1000), sign="1"),
    dict(bg="town", cast=[(O, 540, dict(expr="worried"))], cam=(1.3, 540, 1050))]),
 (6, "Спор решил Конгресс: Мичиган станет штатом, только если отдаст Толедо.", [
    dict(bg="congress", cast=[("official", 540, dict(expr="talk", talk=True, arm_l=80))], cam=(1.3, 540, 1050)),
    dict(bg="congress", cast=[(O, 330, dict(expr="happy", arm_r=140)), (M, 750, dict(expr="shock"))], cam=(1.15, 540, 1000), fx="stamp", stamp_text="ТОЛЕДО — ОГАЙО")]),
 (7, "А взамен он получит Верхний полуостров — дикий лес далеко на севере.", [
    dict(bg="forest", cast=[(M, 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1050)),
    dict(bg="forest", cast=[(M, 540, dict(expr="worried", sweat=True))], cam=(2.0, 540, 900))]),
 (8, "Мичиганцы возмущались: им подсунули глушь, где нет ничего ценного.", [
    dict(bg="forest", cast=[(M, 540, dict(expr="angry", rage=0.9, steam=True, talk=True))], cam=(1.7, 540, 940))]),
 (9, "В конце тысяча восемьсот тридцать шестого года они нехотя согласились.", [
    dict(bg="congress", cast=[(M, 540, dict(expr="worried", talk=True))], cam=(1.3, 540, 1050), sign="1836")]),
 (10, "А через несколько лет на полуострове нашли огромные залежи меди и железа.", [
    dict(bg="mine", cast=[("miner", 540, dict(expr="shock", arm_r=120))], cam=(1.3, 540, 1050)),
    dict(bg="mine", cast=[(M, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.25, 540, 1050), fx="money")]),
 (11, "Сорок лет Мичиган добывал больше всех меди в стране. Проигрыш оказался выигрышем.", [
    dict(bg="mine", cast=[(M, 540, dict(expr="smug"))], cam=(1.3, 540, 1050), sign="ПЕРВЫЙ\nПО МЕДИ"),
    dict(bg="town", cast=[(O, 540, dict(expr="worried"))], cam=(2.2, 540, 870))]),
]
