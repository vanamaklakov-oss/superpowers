# The Great Hanoi Rat Hunt, 1902 (the "cobra effect"). Sources: Michael G. Vann, "Of Rats, Rice, and Race: The Great
# Hanoi Rat Massacre", French Colonial History 4 (2003); Vann & Clarke, "The Great Hanoi Rat Hunt" (OUP 2019);
# Wikipedia "Great Hanoi Rat Massacre"; Atlas Obscura. Bounty 1 cent per tail; tailless rats seen; rat farms found
# outside the city; bounty scrapped. Peak catch ~20 000 rats a day (June 1902).
O, V, W = "colonial", "villager", "villager2"
SCENES = [
 (1, "Французские власти однажды платили людям за крыс. И крыс стало только больше.", [
    dict(bg="street", cast=[(O, 540, dict(expr="smug", arm_r=70))], cam=(1.3, 540, 1100), fx="money"),
    dict(bg="sewer", cast=[(O, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (2, "Ханой, тысяча девятьсот второй год. Французы строят здесь европейский квартал с новой канализацией.", [
    dict(bg="street", cast=[(O, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.15, 540, 1050), sign="1902"),
    dict(bg="street", cast=[(O, 540, dict(expr="smug"))], cam=(1.7, 540, 950))]),
 (3, "Но в тёплых трубах крысы расплодились в огромном количестве. А с крысами приходит чума.", [
    dict(bg="sewer", cast=[], cam=(1.2, 540, 1000)),
    dict(bg="sewer", cast=[(O, 540, dict(expr="worried", sweat=True))], cam=(1.8, 540, 950))]),
 (4, "Сначала наняли ловцов. В лучшие дни они ловили до двадцати тысяч крыс. А меньше их не становилось.", [
    dict(bg="sewer", cast=[(V, 540, dict(expr="neutral", arm_r=60, talk=True))], cam=(1.3, 540, 1050), sign="20 000\nВ ДЕНЬ"),
    dict(bg="office", cast=[(O, 540, dict(expr="angry", rage=0.6, steam=True, talk=True))], cam=(1.9, 540, 900))]),
 (5, "Тогда власти объявили награду: один цент за каждый крысиный хвост.", [
    dict(bg="office", cast=[(O, 540, dict(expr="talk", talk=True, arm_l=80))], cam=(1.3, 540, 1050), sign="1 ЦЕНТ\nЗА ХВОСТ"),
    dict(bg="office", cast=[(O, 540, dict(expr="smug"))], cam=(1.9, 540, 900), fx="calc")]),
 (6, "Местные жители взялись за дело с огромным энтузиазмом. Хвосты несли и несли.", [
    dict(bg="market", cast=[(V, 330, dict(expr="happy", arm_r=140)), (W, 750, dict(expr="happy", arm_l=140))], cam=(1.1, 540, 1000)),
    dict(bg="office", cast=[(O, 330, dict(expr="happy", arm_l=150, arm_r=150)), (V, 750, dict(expr="smug", arm_l=90))], cam=(1.2, 540, 1000), fx="money")]),
 (7, "Но вскоре чиновники заметили странное: по улицам бегали крысы без хвостов.", [
    dict(bg="street", cast=[(O, 540, dict(expr="neutral"))], cam=(1.3, 540, 1050)),
    dict(bg="street", cast=[(O, 540, dict(expr="shock"))], cam=(2.1, 540, 880), bubble=(0, "?"))]),
 (8, "Оказалось, хвост отрезали, а крысу отпускали. Пусть плодится и приносит новые хвосты.", [
    dict(bg="market", cast=[(V, 540, dict(expr="smug", arm_r=80, talk=True))], cam=(1.4, 540, 1000), bubble=(0, "on")),
    dict(bg="market", cast=[(V, 330, dict(expr="smug")), (W, 750, dict(expr="happy", arm_l=120))], cam=(1.15, 540, 1000))]),
 (9, "А за городом нашли настоящие крысиные фермы.", [
    dict(bg="farm", cast=[(O, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1050)),
    dict(bg="farm", cast=[(O, 540, dict(expr="angry", rage=0.9, steam=True))], cam=(2.0, 540, 900))]),
 (10, "Награду отменили. Деньги потратили, а крыс в городе меньше не стало.", [
    dict(bg="office", cast=[(O, 540, dict(expr="worried", talk=True))], cam=(1.3, 540, 1050), fx="stamp"),
    dict(bg="sewer", cast=[], cam=(1.7, 540, 950))]),
 (11, "Экономисты называют это эффектом кобры: если платить за проблему, её начнут разводить.", [
    dict(bg="dark", cast=[(O, 540, dict(expr="worried"))], cam=(1.2, 540, 1050), sign="ЭФФЕКТ\nКОБРЫ"),
    dict(bg="dark", cast=[(V, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
