# The Princes in the Tower, 1483. Sources: Historic Royal Palaces blog "Charles II and the discovery of the Princes in
# the Tower in 1674"; Westminster Abbey "Edward V & Richard Duke of York"; Historic UK; Wikipedia "Princes in the Tower".
# Edward IV died Apr 1483; Edward V aged 12; Titulus Regius declared the boys illegitimate; Richard III crowned; the boys
# seen less and less (Mancini). Bones of two children found under a staircase in the White Tower, 1674; interred in
# Westminster Abbey by Charles II (urn 1678). 1933 exam (Tanner & Wright): sex/date not determinable; DNA testing refused.
P, Q, U = "prince", "prince2", "uncle"
SCENES = [
 (1, "Два принца вошли в лондонский Тауэр. И больше их никто не видел.", [
    dict(bg="tower", cast=[(P, 330, dict(expr="happy")), (Q, 750, dict(expr="happy"))], cam=(1.1, 540, 1050)),
    dict(bg="room", cast=[], cam=(1.8, 540, 930))]),
 (2, "Тысяча четыреста восемьдесят третий год. Умирает король Англии Эдуард Четвёртый.", [
    dict(bg="palace", cast=[("king", 540, dict(expr="worried"))], cam=(1.3, 540, 1050), sign="1483")]),
 (3, "Королём должен стать его двенадцатилетний сын Эдуард.", [
    dict(bg="palace", cast=[(P, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="palace", cast=[(P, 540, dict(expr="smug"))], cam=(1.9, 540, 900))]),
 (4, "Мальчика и его младшего брата поселили в Тауэре. Тогда это была королевская крепость, а не только тюрьма.", [
    dict(bg="tower", cast=[(P, 330, dict(expr="neutral", talk=True)), (Q, 750, dict(expr="happy"))], cam=(1.1, 540, 1050)),
    dict(bg="room", cast=[(Q, 540, dict(expr="worried"))], cam=(1.7, 540, 950))]),
 (5, "А их дядя Ричард объявил племянников незаконнорождёнными и сам стал королём.", [
    dict(bg="palace", cast=[(U, 540, dict(expr="smug", arm_r=110, talk=True))], cam=(1.3, 540, 1050), fx="stamp", stamp_text="КОРОЛЬ"),
    dict(bg="palace", cast=[(U, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.9, 540, 900))]),
 (6, "Сначала мальчиков видели во дворе крепости. Потом всё реже. А потом они исчезли.", [
    dict(bg="tower", cast=[(P, 330, dict(expr="happy", arm_r=120)), (Q, 750, dict(expr="happy", arm_l=120))], cam=(1.1, 540, 1050)),
    dict(bg="tower", cast=[(Q, 540, dict(expr="worried"))], cam=(1.3, 540, 1050)),
    dict(bg="tower", cast=[], cam=(1.6, 540, 960))]),
 (7, "Многие обвиняли дядю. Но прямых доказательств нет до сих пор.", [
    dict(bg="palace", cast=[(U, 540, dict(expr="worried", sweat=True))], cam=(1.6, 540, 960), bubble=(0, "?"))]),
 (8, "Почти через двести лет, в тысяча шестьсот семьдесят четвёртом году, под лестницей в Тауэре нашли кости двух детей.", [
    dict(bg="room", cast=[("villager", 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1050), sign="1674"),
    dict(bg="dark", cast=[("villager", 540, dict(expr="worried"))], cam=(1.9, 540, 900))]),
 (9, "Король Карл Второй велел похоронить их в Вестминстерском аббатстве как останки принцев.", [
    dict(bg="palace", cast=[("king", 540, dict(expr="neutral", talk=True, arm_r=90))], cam=(1.3, 540, 1050))]),
 (10, "В тысяча девятьсот тридцать третьем году кости осмотрели. Но не смогли установить даже пол и век.", [
    dict(bg="library", cast=[("doctor", 540, dict(expr="neutral", arm_r=90))], cam=(1.3, 540, 1050), sign="1933"),
    dict(bg="library", cast=[("doctor", 540, dict(expr="worried", sweat=True))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (11, "Анализ ДНК мог бы всё решить. Но вскрывать урну так и не разрешают.", [
    dict(bg="library", cast=[("doctor", 540, dict(expr="smug", talk=True))], cam=(1.4, 540, 1000), sign="ДНК?"),
    dict(bg="palace", cast=[("official", 540, dict(expr="angry"))], cam=(1.8, 540, 930), fx="stamp", stamp_text="ЗАПРЕЩЕНО")]),
]
