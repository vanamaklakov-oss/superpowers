# The Lost Colony of Roanoke. Sources: National Park Service (Fort Raleigh) "1590 Voyage" / "Major theories";
# National Geographic; NC Dept of Natural & Cultural Resources; Britannica; Wikipedia "Roanoke Colony".
# ~115–120 colonists (1587); Virginia Dare (born 18 Aug 1587) first English child born in the Americas; White's return
# delayed by the Anglo-Spanish war (Armada 1588); Aug 1590: houses taken down, "CROATOAN" carved on a post of the
# palisade, "CRO" on a tree; agreed sign of distress (a cross) absent; storms stopped the trip to Croatoan.
G = "governor"
SCENES = [
 (1, "Больше ста человек исчезли без следа. Осталось только одно слово.", [
    dict(bg="forest", cast=[(G, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="dark", cast=[(G, 540, dict(expr="worried"))], cam=(2.0, 540, 900), sign="CROATOAN")]),
 (2, "Тысяча пятьсот восемьдесят седьмой год. Англичане основывают колонию на острове Роанок в Северной Америке.", [
    dict(bg="harbor", cast=[(G, 330, dict(expr="happy", arm_r=140, talk=True)), ("villager", 750, dict(expr="happy"))], cam=(1.1, 540, 1000), sign="1587"),
    dict(bg="forest", cast=[(G, 540, dict(expr="smug"))], cam=(1.7, 540, 950))]),
 (3, "Среди колонистов была дочь губернатора Джона Уайта. Там родилась его внучка — первый английский ребёнок в Америке.", [
    dict(bg="forest", cast=[(G, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="forest", cast=[(G, 540, dict(expr="happy", talk=True))], cam=(1.9, 540, 900))]),
 (4, "Уайт уплывает в Англию за припасами. Но вернуться сразу не может: Англия воюет с Испанией, все корабли нужны флоту.", [
    dict(bg="sea", cast=[(G, 540, dict(expr="neutral", arm_r=80))], cam=(1.2, 540, 1050)),
    dict(bg="palace", cast=[("king", 540, dict(expr="angry", talk=True, arm_l=120))], cam=(1.5, 540, 970), fx="stamp", stamp_text="ВОЙНА")]),
 (5, "Он возвращается только через три года, в тысяча пятьсот девяностом.", [
    dict(bg="harbor", cast=[(G, 540, dict(expr="happy", arm_r=120))], cam=(1.3, 540, 1050), sign="1590")]),
 (6, "Поселение пусто. Дома разобраны. Людей нет.", [
    dict(bg="forest", cast=[(G, 540, dict(expr="neutral"))], cam=(1.25, 540, 1050)),
    dict(bg="forest", cast=[(G, 540, dict(expr="shock", sweat=True))], cam=(2.1, 540, 880))]),
 (7, "На столбе ограды вырезано одно слово: Кроатоан. А на дереве три буквы.", [
    dict(bg="forest", cast=[(G, 540, dict(expr="shock"))], cam=(1.3, 540, 1050), sign="CROATOAN"),
    dict(bg="forest", cast=[(G, 540, dict(expr="worried"))], cam=(1.8, 540, 930), sign="CRO")]),
 (8, "Колонисты договорились: если уходят в беде, рядом вырежут крест. Креста не было.", [
    dict(bg="dark", cast=[(G, 540, dict(expr="neutral", talk=True))], cam=(1.4, 540, 1000), sign="КРЕСТ = БЕДА"),
    dict(bg="forest", cast=[(G, 540, dict(expr="smug"))], cam=(1.6, 540, 960), bubble=(0, "on"))]),
 (9, "Кроатоан — так назывался соседний остров и дружественное племя. Но шторм не дал Уайту туда доплыть.", [
    dict(bg="sea", cast=[(G, 540, dict(expr="worried", sweat=True, lean=6))], cam=(1.3, 540, 1050)),
    dict(bg="sea", cast=[(G, 540, dict(expr="angry", rage=0.8, steam=True))], cam=(1.9, 540, 900))]),
 (10, "Он уплыл в Англию и больше никогда не увидел свою семью.", [
    dict(bg="sea", cast=[(G, 540, dict(expr="worried"))], cam=(1.8, 540, 930))]),
 (11, "Куда исчезли колонисты, историки спорят до сих пор.", [
    dict(bg="forest", cast=[], cam=(1.2, 540, 1000)),
    dict(bg="dark", cast=[(G, 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
