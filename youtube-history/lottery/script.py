# The retiree who legally beat the state lottery (Jerry and Marge Selbee, Winfall / Cash WinFall, 2003–2012).
# Sources: CBS News "How a retired couple found lottery odds in their favor"; HuffPost Highline "Lotto winners";
# ClickOnDetroit (2019); Michigan Public (legislator closes loophole); Lottery USA. Totals differ by source:
# ~$26–27 M gross winnings, ~$7.75 M profit before tax. Roll-down when the jackpot is not won after growing big.
J, F, G, O, C = "jerry", "friend", "friend2", "official", "clerk"
SCENES = [
 (1, "Пенсионер нашёл законный способ обыгрывать государственную лотерею. И выиграл миллионы.", [
    dict(bg="town", cast=[(J, 540, dict(expr="smug", arm_r=40))], cam=(1.3, 540, 1100)),
    dict(bg="town", cast=[(J, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.8, 540, 900), fx="money")]),
 (2, "Джерри Сэлби жил в маленьком городке в Мичигане и всю жизнь любил математику.", [
    dict(bg="town", cast=[(J, 540, dict(expr="neutral", talk=True))], cam=(1.15, 540, 1050)),
    dict(bg="kitchen", cast=[(J, 540, dict(expr="smug", arm_r=70))], cam=(1.7, 540, 950))]),
 (3, "Однажды он внимательно прочитал правила местной лотереи. И заметил странное.", [
    dict(bg="store", cast=[(J, 540, dict(expr="neutral", arm_r=60))], cam=(1.3, 540, 1050)),
    dict(bg="store", cast=[(J, 540, dict(expr="shock"))], cam=(2.1, 540, 880))]),
 (4, "Если джекпот вырастал до большой суммы и его никто не выигрывал, деньги делили между мелкими выигрышами.", [
    dict(bg="store", cast=[(C, 540, dict(expr="talk", talk=True, arm_l=70))], cam=(1.3, 540, 1050), sign="ДЖЕКПОТ\nДЕЛЯТ"),
    dict(bg="store", cast=[(C, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.2, 540, 1050), fx="money")]),
 (5, "Джерри посчитал: в такие недели, если купить много билетов, выиграешь больше, чем потратишь.", [
    dict(bg="kitchen", cast=[(J, 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1100), fx="calc"),
    dict(bg="kitchen", cast=[(J, 540, dict(expr="smug"))], cam=(2.0, 540, 880))]),
 (6, "Он рискнул несколькими тысячами долларов. И остался в плюсе.", [
    dict(bg="store", cast=[(J, 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 950)),
    dict(bg="store", cast=[(J, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050))]),
 (7, "Вместе с женой Мардж он создал компанию, позвал друзей, и они покупали билеты тысячами.", [
    dict(bg="kitchen", cast=[(F, 280, dict(expr="happy")), (J, 540, dict(expr="talk", talk=True, arm_r=80)), (G, 800, dict(expr="smug"))], cam=(1.0, 540, 1000)),
    dict(bg="store", cast=[(J, 360, dict(expr="happy", arm_r=120)), (C, 760, dict(expr="shock", sweat=True))], cam=(1.2, 540, 1000))]),
 (8, "Когда Мичиган закрыл игру, они поехали в соседний Массачусетс, где была почти такая же лотерея.", [
    dict(bg="highway", cast=[(J, 540, dict(expr="smug", arm_r=60))], cam=(1.2, 540, 1050)),
    dict(bg="highway", cast=[(J, 540, dict(expr="happy"))], cam=(1.6, 540, 950))]),
 (9, "За девять лет через их руки прошло около двадцати шести миллионов долларов выигрышей.", [
    dict(bg="vault", cast=[(J, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.2, 540, 1050), sign="$26 000 000", fx="money")]),
 (10, "Власти устроили проверку. И признали: всё законно. Никакого обмана, только арифметика.", [
    dict(bg="office", cast=[(O, 540, dict(expr="angry", rage=0.7, steam=True, talk=True))], cam=(1.6, 540, 950)),
    dict(bg="office", cast=[(O, 360, dict(expr="worried", sweat=True)), (J, 760, dict(expr="smug"))], cam=(1.15, 540, 1000), fx="stamp")]),
 (11, "В двенадцатом году лотерею закрыли. А про пенсионеров позже сняли фильм.", [
    dict(bg="office", cast=[(O, 540, dict(expr="worried"))], cam=(1.3, 540, 1050)),
    dict(bg="cinema", cast=[(J, 540, dict(expr="happy", arm_r=120))], cam=(1.3, 540, 1050))]),
 (12, "Иногда, чтобы обыграть государство, достаточно внимательно прочитать его правила.", [
    dict(bg="kitchen", cast=[(J, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
