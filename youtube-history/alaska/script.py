# The Alaska Purchase, 1867. Sources: Office of the Historian (history.state.gov) "Purchase of Alaska, 1867"; Library of
# Congress "Today in History: March 30"; Wikipedia "Alaska Purchase"; History.com. $7.2 M, ~2 cents an acre; critics'
# nicknames "Seward's Folly", "Seward's Icebox", "Johnson's polar bear garden" (the first may be later). Klondike (Yukon)
# gold rush 1896–98 went through Alaska; Nome gold 1899; oil (Prudhoe Bay, 1968).
T, S = "tsar", "seward"
SCENES = [
 (1, "Америка купила землю, над которой смеялась вся страна. А потом там нашли золото.", [
    dict(bg="snow", cast=[(S, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="gold", cast=[(S, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.9, 540, 900), fx="money")]),
 (2, "Тысяча восемьсот шестьдесят седьмой год. Россия продаёт Аляску Соединённым Штатам.", [
    dict(bg="palace", cast=[(T, 540, dict(expr="neutral", talk=True, arm_r=80))], cam=(1.2, 540, 1050), sign="1867"),
    dict(bg="office", cast=[(S, 540, dict(expr="smug"))], cam=(1.7, 540, 950))]),
 (3, "Цена — семь миллионов двести тысяч долларов. Примерно два цента за акр.", [
    dict(bg="office", cast=[(T, 330, dict(expr="smug", arm_r=120)), (S, 750, dict(expr="happy", arm_l=120))], cam=(1.15, 540, 1000), sign="$7 200 000"),
    dict(bg="office", cast=[(S, 540, dict(expr="neutral"))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["1 АКР", "= 2 ЦЕНТА"])]),
 (4, "Сделку заключил госсекретарь Уильям Сьюард.", [
    dict(bg="office", cast=[(S, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.6, 540, 960), fx="stamp", stamp_text="КУПЛЕНО")]),
 (5, "Критики издевались: «холодильник Сьюарда», «сад для белых медведей».", [
    dict(bg="office", cast=[("friend", 330, dict(expr="happy", talk=True, arm_r=150)), ("friend2", 750, dict(expr="happy", arm_l=150))], cam=(1.1, 540, 1000)),
    dict(bg="snow", cast=[(S, 540, dict(expr="angry", rage=0.7, steam=True))], cam=(1.8, 540, 930), sign="ХОЛОДИЛЬНИК\nСЬЮАРДА")]),
 (6, "Многие считали, что за ледяную пустыню отдали слишком много.", [
    dict(bg="snow", cast=[(S, 540, dict(expr="worried", sweat=True))], cam=(1.4, 540, 1000))]),
 (7, "Почти тридцать лет на Аляске было тихо и почти безлюдно.", [
    dict(bg="snow", cast=[], cam=(1.2, 540, 1000)),
    dict(bg="snow", cast=[("miner", 540, dict(expr="neutral"))], cam=(1.6, 540, 960))]),
 (8, "А в конце века рядом, на канадском Клондайке, нашли золото. И через Аляску хлынули десятки тысяч старателей.", [
    dict(bg="harbor", cast=[("miner", 330, dict(expr="happy", arm_r=140)), ("friend", 750, dict(expr="happy", arm_l=140))], cam=(1.1, 540, 1000)),
    dict(bg="mine", cast=[("miner", 540, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.6, 540, 960))]),
 (9, "Вскоре золото нашли и на самой Аляске, в городке Ном.", [
    dict(bg="gold", cast=[("miner", 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050), fx="money")]),
 (10, "А в двадцатом веке там нашли ещё и нефть.", [
    dict(bg="snow", cast=[("miner", 540, dict(expr="shock"))], cam=(1.6, 540, 960), sign="НЕФТЬ")]),
 (11, "Сегодня ту покупку называют одной из самых выгодных сделок в истории.", [
    dict(bg="gold", cast=[(S, 540, dict(expr="smug"))], cam=(1.3, 540, 1050)),
    dict(bg="palace", cast=[(T, 540, dict(expr="worried", sweat=True))], cam=(2.2, 540, 870))]),
]
