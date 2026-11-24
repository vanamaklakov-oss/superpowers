# The Phaistos Disc. Sources: Wikipedia "Phaistos Disc"; National Geographic "This ancient script has remained unsolved
# for over a century"; World History Encyclopedia; Nature (2008) 453:990. Found 3 Jul 1908 by Luigi Pernier at the
# Minoan palace of Phaistos; 241 (some count 242) stamped tokens, 45 distinct signs, spiral on both faces; too many signs
# for an alphabet, likely a syllabary; date disputed (often c. 1850–1600 BC); most archaeologists accept it as authentic,
# a minority suspect forgery; no proposed decipherment accepted; Heraklion Archaeological Museum.
P, S = "doctor", "scholar"
SCENES = [
 (0, "Двести сорок один знак. И ни одного понятного.", [
    dict(bg="museum", cast=[], cam=(1.5, 540, 1000), hook="241 ЗНАК\nНИ ОДНОГО ПОНЯТНОГО")]),
 (1, "Тысяча девятьсот восьмой год. Остров Крит, руины древнего дворца в Фесте.", [
    dict(bg="ruins", cast=[(P, 540, dict(expr="happy", arm_r=120))], cam=(1.2, 540, 1050), sign="1908")]),
 (2, "Итальянский археолог Луиджи Пернье находит небольшой глиняный диск.", [
    dict(bg="dig", cast=[(P, 540, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="dig", cast=[(P, 540, dict(expr="happy"))], cam=(1.9, 540, 900), bubble=(0, "on"))]),
 (3, "С двух сторон по спирали идут знаки: человечки, рыбы, птицы, щиты, растения.", [
    dict(bg="museum", cast=[(S, 540, dict(expr="neutral", talk=True, arm_r=90))], cam=(1.3, 540, 1050))]),
 (4, "Их не нарисовали, а отпечатали штампами. Как будто древняя печать.", [
    dict(bg="museum", cast=[(S, 540, dict(expr="shock"))], cam=(1.6, 540, 960), fx="stamp", stamp_text="ШТАМП")]),
 (5, "Всего двести сорок один знак, из них сорок пять разных.", [
    dict(bg="library", cast=[(S, 540, dict(expr="neutral"))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["241 ЗНАК", "45 РАЗНЫХ"])]),
 (6, "Для алфавита слишком много. Поэтому учёные думают, что каждый знак — это слог.", [
    dict(bg="library", cast=[(S, 540, dict(expr="smug", talk=True, arm_l=90))], cam=(1.5, 540, 970))]),
 (7, "Других надписей с такими штампами почти нет. Сравнивать не с чем.", [
    dict(bg="library", cast=[(S, 540, dict(expr="worried", sweat=True))], cam=(1.8, 540, 930), bubble=(0, "?"))]),
 (8, "Предлагались сотни расшифровок. Ни одну учёные не признали.", [
    dict(bg="library", cast=[(S, 330, dict(expr="angry", talk=True)), (P, 750, dict(expr="angry", rage=0.6, steam=True))], cam=(1.15, 540, 1000))]),
 (9, "Некоторые даже считают диск подделкой. Но большинство археологов уверены, что он настоящий.", [
    dict(bg="museum", cast=[(P, 540, dict(expr="smug", arm_r=90))], cam=(1.4, 540, 1000), fx="stamp", stamp_text="НАСТОЯЩИЙ?")]),
 (10, "Даже его возраст спорен. А сам диск хранится в музее на Крите и всё ещё молчит.", [
    dict(bg="crete", cast=[], cam=(1.2, 540, 1000)),
    dict(bg="museum", cast=[(S, 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
