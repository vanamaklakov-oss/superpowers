# Peter the Great's beard tax (1698; tokens from 1705). Sources: Wikipedia "Beard tax"; Smithsonian Magazine "Why Tsar
# Peter the Great established a beard tax"; JSTOR Daily; British Museum beard-token records (C_C-3701..3703).
# Rates differed by rank (up to 100 roubles a year for rich merchants; peasants paid a small fee on entering a town).
# Token inscription "ДЕНГИ ВЗЯТЫ". Revenue was low (~3 588 roubles a year 1705–08). Abolished 1772 (Catherine II).
P, B, G = "peter", "boyar", "boyar2"
SCENES = [
 (1, "Пётр Первый ввёл в России налог. На бороду.", [
    dict(bg="palace", cast=[(P, 540, dict(expr="smug", arm_r=70))], cam=(1.3, 540, 1100)),
    dict(bg="palace", cast=[(B, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (2, "Тысяча шестьсот девяносто восьмой год. Царь возвращается из Европы и решает: русские должны выглядеть как европейцы.", [
    dict(bg="palace", cast=[(P, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.2, 540, 1050), sign="1698"),
    dict(bg="palace", cast=[(P, 540, dict(expr="smug"))], cam=(1.8, 540, 930), bubble=(0, "on"))]),
 (3, "По рассказам современников, он сам брал бритву и брил бояр прямо на приёме.", [
    dict(bg="palace", cast=[(P, 330, dict(expr="happy", arm_r=150)), (B, 750, dict(expr="shock", sweat=True, lean=-6))], cam=(1.15, 540, 1000)),
    dict(bg="palace", cast=[(G, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (4, "Бояре были в ужасе: борода считалась частью веры и достоинства.", [
    dict(bg="room", cast=[(B, 330, dict(expr="worried", talk=True)), (G, 750, dict(expr="angry", rage=0.6, steam=True))], cam=(1.15, 540, 1000))]),
 (5, "Тогда Пётр придумал хитрее. Хочешь носить бороду? Плати.", [
    dict(bg="palace", cast=[(P, 540, dict(expr="smug", arm_r=90, talk=True))], cam=(1.6, 540, 960)),
    dict(bg="palace", cast=[(P, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.25, 540, 1050), fx="money")]),
 (6, "Богатые купцы платили до ста рублей в год. Огромные деньги по тем временам.", [
    dict(bg="treasury", cast=[(B, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1050), sign="100 РУБЛЕЙ\nВ ГОД"),
    dict(bg="treasury", cast=[(B, 540, dict(expr="angry", rage=0.9, steam=True))], cam=(2.0, 540, 900))]),
 (7, "А крестьяне платили небольшой сбор каждый раз, когда въезжали с бородой в город.", [
    dict(bg="street", cast=[(G, 540, dict(expr="worried", arm_r=60))], cam=(1.3, 540, 1050)),
    dict(bg="street", cast=[("soldier", 330, dict(expr="smug", arm_r=110)), (G, 750, dict(expr="worried", sweat=True))], cam=(1.15, 540, 1000))]),
 (8, "Заплатившему давали медный жетон — бородовой знак. На нём было выбито: «деньги взяты».", [
    dict(bg="treasury", cast=[(B, 540, dict(expr="neutral", arm_r=90))], cam=(1.4, 540, 1000), sign="ДЕНГИ\nВЗЯТЫ"),
    dict(bg="street", cast=[(B, 540, dict(expr="smug"))], cam=(1.8, 540, 930), fx="stamp", stamp_text="ОПЛАЧЕНО")]),
 (9, "Но вот поворот: денег налог принёс совсем мало.", [
    dict(bg="treasury", cast=[(P, 540, dict(expr="shock"))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ЖДАЛИ: МНОГО", "СОБРАЛИ: МАЛО", "= ПРОВАЛ"]),
    dict(bg="treasury", cast=[(P, 540, dict(expr="angry", rage=0.8, steam=True))], cam=(2.0, 540, 900))]),
 (10, "Бороды прятали, сбривали или просто не ездили в город.", [
    dict(bg="room", cast=[(B, 540, dict(expr="smug", arm_r=80))], cam=(1.4, 540, 1000)),
    dict(bg="room", cast=[(G, 540, dict(expr="happy"))], cam=(1.8, 540, 930))]),
 (11, "А отменили налог только при Екатерине Второй, больше чем через семьдесят лет.", [
    dict(bg="palace", cast=[(B, 330, dict(expr="happy", arm_l=150, arm_r=150)), (G, 750, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.15, 540, 1000), sign="1772"),
    dict(bg="palace", cast=[(B, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
