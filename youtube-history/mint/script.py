# US Mint Direct Ship programme and the $1 coin credit-card loophole (2008–2011). Sources: NPR Planet Money
# "Free Money? How Some People Found a Way to Earn Frequent Flier Miles"; The Points Guy (history of the Mint deal);
# CoinNews / US Mint notice ending card payments July 2011; NPR Dec 2011 "Treasury halts presidential $1 coin
# production" (~$1.4 bn of unused coins stockpiled). Presidential $1 coins from 2007. Mint paid shipping.
T, B, C, O = "traveler", "banker", "clerk", "official"
SCENES = [
 (1, "Американцы летали бесплатно за счёт государства. И делали это совершенно законно.", [
    dict(bg="airport", cast=[(T, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="airport", cast=[(T, 540, dict(expr="smug", arm_r=60))], cam=(2.0, 540, 900))]),
 (2, "В две тысячи седьмом году Монетный двор США начал выпускать долларовые монеты с президентами.", [
    dict(bg="mint", cast=[(C, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.2, 540, 1050), sign="$1"),
    dict(bg="mint", cast=[(C, 540, dict(expr="smug"))], cam=(1.7, 540, 950))]),
 (3, "Но люди ими почти не пользовались. Монеты лежали без дела.", [
    dict(bg="office", cast=[(O, 540, dict(expr="worried", sweat=True))], cam=(1.5, 540, 1000))]),
 (4, "Тогда монеты стали продавать всем желающим по номиналу. С бесплатной доставкой. И с оплатой кредитной картой.", [
    dict(bg="office", cast=[(O, 540, dict(expr="talk", talk=True, arm_l=80))], cam=(1.3, 540, 1050), sign="ДОСТАВКА\nБЕСПЛАТНО"),
    dict(bg="office", cast=[(O, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.2, 540, 1050))]),
 (5, "Любители авиамиль сразу всё посчитали. Тысяча долларов на карте — это тысяча миль.", [
    dict(bg="home", cast=[(T, 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1100), fx="calc", calc_lines=["$1000 НА КАРТУ", "= 1000 МИЛЬ", "= ПЕРЕЛЁТ"]),
    dict(bg="home", cast=[(T, 540, dict(expr="smug"))], cam=(2.0, 540, 880), bubble=(0, "on"))]),
 (6, "Они заказывали коробки с монетами, получали их домой и, не открывая, несли в банк.", [
    dict(bg="home", cast=[(T, 540, dict(expr="happy", arm_r=130))], cam=(1.2, 540, 1050)),
    dict(bg="bank", cast=[(T, 330, dict(expr="smug", arm_r=90)), (B, 750, dict(expr="shock"))], cam=(1.15, 540, 1000))]),
 (7, "Банк зачислял деньги на счёт, этими деньгами гасили карту. А мили оставались.", [
    dict(bg="bank", cast=[(B, 540, dict(expr="neutral", talk=True))], cam=(1.4, 540, 1000), fx="money"),
    dict(bg="airport", cast=[(T, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050))]),
 (8, "Итог: ни одного потраченного доллара и бесплатные билеты. А за доставку платило государство.", [
    dict(bg="airport", cast=[(T, 540, dict(expr="smug"))], cam=(1.8, 540, 920), sign="$0"),
    dict(bg="mint", cast=[(C, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1050))]),
 (9, "Некоторые заказывали монет на десятки тысяч долларов.", [
    dict(bg="home", cast=[(T, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.2, 540, 1050), fx="money")]),
 (10, "В две тысячи одиннадцатом году Монетный двор заметил схему и запретил платить картами.", [
    dict(bg="office", cast=[(O, 540, dict(expr="angry", rage=0.8, steam=True, talk=True))], cam=(1.7, 540, 940)),
    dict(bg="office", cast=[(O, 540, dict(expr="angry"))], cam=(1.25, 540, 1050), fx="stamp", stamp_text="ЗАПРЕЩЕНО")]),
 (11, "А потом перестал чеканить такие монеты для обращения. На складах их скопилось больше чем на миллиард долларов.", [
    dict(bg="vault", cast=[(O, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1050), sign="$1 000 000 000+"),
    dict(bg="vault", cast=[(O, 540, dict(expr="worried"))], cam=(1.9, 540, 900))]),
 (12, "Никто ничего не украл. Просто правила писали без калькулятора.", [
    dict(bg="airport", cast=[(T, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
