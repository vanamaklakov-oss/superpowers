# The Flannan Isles lighthouse mystery, Dec 1900. Sources: National Records of Scotland "The Flannan Islands lighthouse:
# a disappearance" and blog (2023); Royal Museums Greenwich (2019) "What caused the disappearance of the Flannan Isle
# lighthouse keepers?"; Wikipedia "Flannan Isles Lighthouse"; Mental Floss. Archtor saw no light on 15 Dec; tender
# Hesperus delayed by weather until 26 Dec; whistle and rocket unanswered; keepers James Ducat, Thomas Marshall, Donald
# MacArthur missing; NLB superintendent Robert Muirhead investigated (29 Dec) and concluded they were most likely swept
# away by a huge wave at the west landing; rules required one keeper to stay in the lighthouse. Later embellishments
# (stopped clock, uneaten meal, overturned chair) come from fiction, e.g. W. W. Gibson's 1912 poem.
K, L, M = "keeper", "keeper2", "keeper3"
SCENES = [
 (0, "Три смотрителя маяка исчезли без следа.", [
    dict(bg="lighthouse", cast=[], cam=(1.5, 540, 1000), hook="3 СМОТРИТЕЛЯ\nИСЧЕЗЛИ")]),
 (1, "Шотландия, декабрь тысяча девятисотого года. Маяк на крошечном острове посреди океана.", [
    dict(bg="lighthouse", cast=[(K, 280, dict(expr="happy")), (L, 540, dict(expr="neutral", talk=True)), (M, 800, dict(expr="smug"))], cam=(1.0, 540, 1000), sign="1900")]),
 (2, "Пятнадцатого декабря проходящий пароход замечает: маяк не горит.", [
    dict(bg="sea", cast=[("captain", 540, dict(expr="shock", arm_r=140))], cam=(1.3, 540, 1050)),
    dict(bg="lighthouse", cast=[], cam=(1.7, 540, 950))]),
 (3, "Из-за штормов корабль с новой сменой добирается до острова только двадцать шестого.", [
    dict(bg="sea", cast=[("sailor", 540, dict(expr="worried", sweat=True, lean=6))], cam=(1.4, 540, 1000), sign="26.12")]),
 (4, "Капитан даёт гудок, пускает сигнальную ракету. Никто не отвечает.", [
    dict(bg="sea", cast=[("captain", 540, dict(expr="talk", talk=True, arm_r=160))], cam=(1.3, 540, 1050)),
    dict(bg="lighthouse", cast=[], cam=(2.0, 540, 900))]),
 (5, "На маяке пусто. Смотрители Джеймс Дукат, Томас Маршалл и Дональд Макартур исчезли.", [
    dict(bg="room", cast=[], cam=(1.3, 540, 1000)),
    dict(bg="room", cast=[("sailor", 540, dict(expr="shock", sweat=True))], cam=(1.9, 540, 900))]),
 (6, "Их искали по всему острову. И не нашли.", [
    dict(bg="lighthouse", cast=[("sailor", 330, dict(expr="worried")), ("sailor2", 750, dict(expr="worried", sweat=True))], cam=(1.1, 540, 1000), bubble=(0, "?"))]),
 (7, "Инспектор Роберт Мюирхед решил: скорее всего, троих смыло огромной волной с западной пристани.", [
    dict(bg="landing", cast=[("official", 540, dict(expr="neutral", talk=True, arm_r=110))], cam=(1.3, 540, 1050)),
    dict(bg="landing", cast=[], cam=(1.8, 540, 930))]),
 (8, "Странно лишь одно: по правилам один смотритель всегда должен был оставаться на маяке.", [
    dict(bg="room", cast=[("official", 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 960), bubble=(0, "?"))]),
 (9, "Позже вокруг этой истории появилось много выдумок: про остановившиеся часы и недоеденный обед.", [
    dict(bg="room", cast=[("doctor", 540, dict(expr="smug", talk=True))], cam=(1.3, 540, 1050), fx="stamp", stamp_text="ВЫДУМКА")]),
 (10, "Но что случилось на самом деле, никто не знает до сих пор.", [
    dict(bg="lighthouse", cast=[], cam=(1.3, 540, 1000)),
    dict(bg="dark", cast=[("doctor", 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
