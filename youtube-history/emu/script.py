# The Emu War, Western Australia, Nov–Dec 1932. Sources: Wikipedia "Emu War"; Australian Geographic; Smithsonian;
# National Museum of Australia "Defining moments". Major G. P. W. Meredith, 7th Heavy Battery: two soldiers, two
# Lewis guns, 10 000 rounds; ~20 000 emus after breeding moved to cleared wheat land (Campion district); WWI veterans
# farmed there. First phase 2–8 Nov, resumed 13 Nov–10 Dec; ~9 860 rounds, 986 confirmed kills. Meredith compared
# the birds to tanks ("invulnerability of tanks").
M, S, F = "major", "soldier", "farmer"
SCENES = [
 (1, "Австралия однажды объявила войну птицам. И проиграла её.", [
    dict(bg="emus", cast=[(M, 540, dict(expr="smug", arm_r=70))], cam=(1.3, 540, 1100)),
    dict(bg="emus", cast=[(M, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (2, "Тысяча девятьсот тридцать второй год. Ветераны Первой мировой выращивают пшеницу в Западной Австралии.", [
    dict(bg="wheat", cast=[(F, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.2, 540, 1050), sign="1932"),
    dict(bg="farm", cast=[(F, 540, dict(expr="smug"))], cam=(1.7, 540, 950))]),
 (3, "И вдруг на поля приходят около двадцати тысяч эму. Они едят и топчут урожай.", [
    dict(bg="emus", cast=[], cam=(1.2, 540, 1000), sign="20 000"),
    dict(bg="emus", cast=[(F, 540, dict(expr="angry", rage=0.9, steam=True))], cam=(1.8, 540, 950))]),
 (4, "Фермеры просят помощи у армии.", [
    dict(bg="farm", cast=[(F, 330, dict(expr="worried", talk=True)), (M, 750, dict(expr="smug"))], cam=(1.15, 540, 1000))]),
 (5, "Приезжает майор Меридит: двое солдат, два пулемёта и десять тысяч патронов.", [
    dict(bg="camp", cast=[(S, 280, dict(expr="neutral")), (M, 540, dict(expr="smug", arm_r=120, talk=True)), ("soldier2", 800, dict(expr="neutral"))], cam=(1.0, 540, 1000), sign="10 000"),
    dict(bg="camp", cast=[(M, 540, dict(expr="happy"))], cam=(1.9, 540, 900))]),
 (6, "Казалось бы, всё просто. Но эму разбегаются маленькими группами во все стороны.", [
    dict(bg="emus", cast=[(M, 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1050)),
    dict(bg="emus", cast=[(M, 540, dict(expr="shock"))], cam=(2.0, 540, 900), bubble=(0, "?"))]),
 (7, "Пулемёт поставили на грузовик. Но на ухабах его трясло так, что прицелиться было невозможно.", [
    dict(bg="truck", cast=[(S, 540, dict(expr="worried", sweat=True, lean=6))], cam=(1.4, 540, 1000)),
    dict(bg="truck", cast=[(S, 540, dict(expr="shock", lean=-6))], cam=(1.8, 540, 930))]),
 (8, "Через неделю операцию свернули. Потом начали снова и воевали ещё почти месяц.", [
    dict(bg="camp", cast=[(M, 540, dict(expr="worried"))], cam=(1.3, 540, 1050), fx="stamp"),
    dict(bg="wheat", cast=[(M, 540, dict(expr="angry", rage=0.7, steam=True))], cam=(1.7, 540, 950))]),
 (9, "Ушли почти все патроны. А по официальным данным, удалось подстрелить меньше тысячи птиц.", [
    dict(bg="camp", cast=[(S, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1050), fx="calc"),
    dict(bg="emus", cast=[], cam=(1.6, 540, 960), sign="986")]),
 (10, "Майор признал: эму неуязвимы, как танки.", [
    dict(bg="camp", cast=[(M, 540, dict(expr="shock", talk=True, arm_l=110))], cam=(2.0, 540, 900))]),
 (11, "Армия уехала домой. А эму остались.", [
    dict(bg="truck", cast=[(M, 540, dict(expr="worried"))], cam=(1.3, 540, 1050)),
    dict(bg="emus", cast=[], cam=(1.3, 540, 1000))]),
]
