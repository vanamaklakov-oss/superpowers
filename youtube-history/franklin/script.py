# Franklin's lost expedition, 1845. Sources: Royal Museums Greenwich "John Franklin's final North-West Passage
# expedition"; Britannica "Franklin expedition"; Parks Canada (Erebus found 2014 in Queen Maud Gulf; Terror 2016 in
# Terror Bay, after a tip from Inuk ranger Sammy Kogvik; Inuit oral history, e.g. Louie Kamookak); Smithsonian (2018)
# and Polar Record (2016) on lead poisoning being contested. 129 men; provisions for ~3 years; last seen by whalers in
# Baffin Bay, July 1845; Beechey Island graves (3 men, 1846); Victory Point note (found 1859): Franklin died 11 June 1847,
# ships deserted 22 April 1848; survivors marched south; none survived.
F, S = "franklin", "sailor"
SCENES = [
 (1, "Два британских корабля ушли во льды. Ни один из ста двадцати девяти человек не вернулся.", [
    dict(bg="ships", cast=[(F, 540, dict(expr="smug", arm_r=90))], cam=(1.3, 540, 1100), sign="129"),
    dict(bg="ice", cast=[], cam=(1.6, 540, 960))]),
 (2, "Тысяча восемьсот сорок пятый год. Экспедиция Джона Франклина ищет Северо-Западный проход — морской путь через Арктику.", [
    dict(bg="port", cast=[(F, 540, dict(expr="happy", arm_r=130, talk=True))], cam=(1.2, 540, 1050), sign="1845"),
    dict(bg="ice", cast=[(F, 540, dict(expr="smug"))], cam=(1.7, 540, 950), bubble=(0, "on"))]),
 (3, "Корабли «Эребус» и «Террор» — одни из лучших во флоте. Еды взяли на три года.", [
    dict(bg="port", cast=[(S, 330, dict(expr="happy", arm_r=140)), ("sailor2", 750, dict(expr="happy"))], cam=(1.1, 540, 1000), sign="ЕДА НА 3 ГОДА")]),
 (4, "Последний раз их видели китобои летом того же года.", [
    dict(bg="ice", cast=[(S, 540, dict(expr="neutral", arm_r=150))], cam=(1.3, 540, 1050))]),
 (5, "Потом корабли исчезли.", [
    dict(bg="ice", cast=[], cam=(1.9, 540, 900))]),
 (6, "Их искали десятки спасательных экспедиций.", [
    dict(bg="office", cast=[("official", 540, dict(expr="worried", talk=True))], cam=(1.3, 540, 1050)),
    dict(bg="ice", cast=[("major", 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 960), bubble=(0, "?"))]),
 (7, "На острове Бичи нашли три могилы. А позже записку: Франклин умер, корабли брошены во льдах.", [
    dict(bg="camp", cast=[("major", 540, dict(expr="shock"))], cam=(1.3, 540, 1050), sign="1847"),
    dict(bg="camp", cast=[("major", 540, dict(expr="worried", sweat=True))], cam=(1.9, 540, 900), fx="book", book_text="ЗАПИСКА")]),
 (8, "Моряки пошли пешком на юг. Не дошёл никто.", [
    dict(bg="ice", cast=[(S, 330, dict(expr="worried", sweat=True)), ("sailor2", 750, dict(expr="worried", sweat=True))], cam=(1.1, 540, 1000)),
    dict(bg="ice", cast=[], cam=(1.4, 540, 1000))]),
 (9, "Местные инуиты рассказывали, где видели корабли. Но им долго не верили.", [
    dict(bg="ice", cast=[("inuk", 540, dict(expr="talk", talk=True, arm_r=120))], cam=(1.3, 540, 1050)),
    dict(bg="office", cast=[("official", 540, dict(expr="smug"))], cam=(1.6, 540, 960))]),
 (10, "Только в две тысячи четырнадцатом году нашли «Эребус», а в две тысячи шестнадцатом — «Террор». Помогли рассказы инуитов.", [
    dict(bg="underwater", cast=[], cam=(1.2, 540, 1000), sign="2014 · 2016"),
    dict(bg="ice", cast=[("inuk", 540, dict(expr="smug", arm_r=90))], cam=(1.8, 540, 930))]),
 (11, "Но почему погибли все, спорят до сих пор: холод, голод, болезни или свинец из консервных банок.", [
    dict(bg="camp", cast=[("doctor", 540, dict(expr="neutral", talk=True))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ХОЛОД?", "ГОЛОД?", "СВИНЕЦ?"]),
    dict(bg="ice", cast=[("doctor", 540, dict(expr="worried"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
