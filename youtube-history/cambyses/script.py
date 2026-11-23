# The Lost Army of Cambyses (c. 524 BC). Sources: Herodotus, Histories 3.25–26; Wikipedia "Lost Army of Cambyses";
# Leiden University / Phys.org (2014) on Olaf Kaper's theory (defeat by rebel Petubastis III at Dakhla, cover-up by
# Darius I); Archaeology.org; NBC (2009) on the Castiglioni brothers' claim, dismissed by Egypt's Supreme Council of
# Antiquities as unfounded. Herodotus: 50,000 men sent against the Ammonians/oracle of Amun; reached "Oasis" after 7
# days, then vanished; Ammonians said a sandstorm buried them during a meal.
K, P = "cambyses", "persian"
SCENES = [
 (0, "Пятьдесят тысяч солдат. И ни одного так и не нашли.", [
    dict(bg="storm", cast=[], cam=(1.5, 540, 1000), hook="50 000 СОЛДАТ\nИСЧЕЗЛИ")]),
 (1, "Они ушли в пустыню и пропали без следа.", [
    dict(bg="desert", cast=[(P, 540, dict(expr="smug", arm_r=90))], cam=(1.3, 540, 1100), sign="50 000"),
    dict(bg="desert", cast=[], cam=(1.6, 540, 960))]),
 (2, "Шестой век до нашей эры. Персидский царь Камбис завоёвывает Египет.", [
    dict(bg="throne", cast=[(K, 540, dict(expr="smug", arm_r=120, talk=True))], cam=(1.2, 540, 1050), sign="525 ДО Н. Э."),
    dict(bg="temple", cast=[(K, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.7, 540, 950))]),
 (3, "По рассказу Геродота, он отправил армию к далёкому оазису, чтобы разрушить храм оракула Амона.", [
    dict(bg="throne", cast=[(K, 540, dict(expr="angry", rage=0.7, steam=True, talk=True))], cam=(1.7, 540, 940)),
    dict(bg="desert", cast=[(P, 330, dict(expr="neutral")), ("persian", 750, dict(expr="worried"))], cam=(1.1, 540, 1000))]),
 (4, "Через семь дней пути солдат видели в одном оазисе. Дальше — тишина.", [
    dict(bg="oasis", cast=[(P, 540, dict(expr="happy", arm_r=110))], cam=(1.3, 540, 1050), sign="7 ДНЕЙ"),
    dict(bg="desert", cast=[], cam=(1.3, 540, 1000))]),
 (5, "По легенде, во время привала поднялась песчаная буря и засыпала всех.", [
    dict(bg="storm", cast=[(P, 540, dict(expr="shock", sweat=True, lean=-6))], cam=(1.4, 540, 1000)),
    dict(bg="storm", cast=[], cam=(1.8, 540, 930))]),
 (6, "Больше двух тысяч лет люди искали в песках их оружие и кости.", [
    dict(bg="desert", cast=[("scholar", 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1050)),
    dict(bg="desert", cast=[("scholar", 540, dict(expr="worried", sweat=True))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (7, "В две тысячи девятом году итальянские исследователи заявили, что нашли следы армии. Но египетские власти назвали это необоснованным.", [
    dict(bg="desert", cast=[("friend", 540, dict(expr="happy", arm_l=150, arm_r=150, talk=True))], cam=(1.3, 540, 1050), sign="2009"),
    dict(bg="office", cast=[("official", 540, dict(expr="angry", talk=True))], cam=(1.6, 540, 960), fx="stamp", stamp_text="НЕ ДОКАЗАНО")]),
 (8, "А голландский египтолог Олаф Капер предложил другую версию.", [
    dict(bg="temple", cast=[("doctor", 540, dict(expr="smug", arm_r=100, talk=True))], cam=(1.4, 540, 1000), bubble=(0, "on"))]),
 (9, "По его мнению, бури не было. Армию разбил египетский повстанец Петубастис.", [
    dict(bg="temple", cast=[("doctor", 540, dict(expr="talk", talk=True, arm_l=90))], cam=(1.3, 540, 1050)),
    dict(bg="oasis", cast=[("villager", 330, dict(expr="angry", rage=0.6, steam=True)), (P, 750, dict(expr="shock", sweat=True))], cam=(1.15, 540, 1000))]),
 (10, "А следующий царь, Дарий, будто бы придумал легенду про бурю, чтобы скрыть позор.", [
    dict(bg="throne", cast=[("king", 540, dict(expr="smug", arm_r=90))], cam=(1.6, 540, 960), fx="book", book_text="БУРЯ"),
    dict(bg="storm", cast=[], cam=(1.3, 540, 1000))]),
 (11, "Кто прав, неизвестно. Пятидесяти тысяч солдат так и не нашли.", [
    dict(bg="desert", cast=[("doctor", 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
