# The Antikythera mechanism. Sources: Antikythera Mechanism Research Project; CACM "The Antikythera mechanism";
# History.com (J. Greenspan); Science Museum blog; DPMA; Freeth et al. Nature 2006 (CT, 2005 imaging). Wreck found by
# sponge divers ~1900 sheltering from a storm; fragments recovered 1901; gears noticed 1902 (Spyridon Stais).
# ~30 surviving bronze gears; showed Sun/Moon positions, lunar phases, eclipse prediction. Dated ~2nd–1st c. BC.
# "Nothing as complex for over a millennium" is the common scholarly view (told as "по мнению учёных").
D, S = "diver", "scholar"
SCENES = [
 (1, "Ныряльщики нашли на дне моря компьютер, которому больше двух тысяч лет.", [
    dict(bg="sea", cast=[(D, 540, dict(expr="shock", sweat=True))], cam=(1.3, 540, 1100)),
    dict(bg="dark", cast=[(S, 540, dict(expr="shock"))], cam=(2.0, 540, 900), sign="2000+ ЛЕТ")]),
 (2, "Около тысяча девятисотого года греческие ловцы губок пережидают шторм у острова Антикитера и находят на дне древний корабль.", [
    dict(bg="sea", cast=[(D, 330, dict(expr="worried", talk=True)), ("sailor", 750, dict(expr="worried"))], cam=(1.1, 540, 1000), sign="1900"),
    dict(bg="sea", cast=[(D, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.7, 540, 950))]),
 (3, "Со дна поднимают статуи, монеты, посуду. И бесформенный кусок позеленевшей бронзы.", [
    dict(bg="treasury", cast=[(D, 540, dict(expr="happy", arm_r=120))], cam=(1.3, 540, 1050), fx="money"),
    dict(bg="treasury", cast=[(D, 540, dict(expr="neutral"))], cam=(1.9, 540, 900), bubble=(0, "?"))]),
 (4, "Сначала на него почти не обратили внимания. А потом разглядели внутри шестерёнки.", [
    dict(bg="office", cast=[(S, 540, dict(expr="neutral"))], cam=(1.3, 540, 1050)),
    dict(bg="office", cast=[(S, 540, dict(expr="shock", sweat=True))], cam=(2.0, 540, 900))]),
 (5, "Десятки лет учёные спорили, что же это такое.", [
    dict(bg="library", cast=[(S, 330, dict(expr="angry", talk=True, arm_r=90)), ("doctor", 750, dict(expr="angry", talk=True, arm_l=90))], cam=(1.15, 540, 1000))]),
 (6, "А в две тысячи пятом году его просветили рентгеном и разглядели всё устройство.", [
    dict(bg="office", cast=[(S, 540, dict(expr="happy", arm_r=120, talk=True))], cam=(1.3, 540, 1050), sign="2005"),
    dict(bg="office", cast=[(S, 540, dict(expr="shock"))], cam=(1.8, 540, 930), bubble=(0, "on"))]),
 (7, "Внутри было около тридцати крошечных бронзовых шестерёнок.", [
    dict(bg="office", cast=[(S, 540, dict(expr="shock", arm_l=150, arm_r=150))], cam=(1.6, 540, 960), sign="~30 ШЕСТЕРЁНОК")]),
 (8, "Повернёшь ручку, и механизм покажет, где на небе Солнце и Луна, фазы Луны и даже затмения.", [
    dict(bg="dark", cast=[(S, 540, dict(expr="talk", talk=True, arm_r=130))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["СОЛНЦЕ", "ЛУНА", "ЗАТМЕНИЯ"]),
    dict(bg="dark", cast=[(S, 540, dict(expr="happy"))], cam=(1.8, 540, 930))]),
 (9, "По мнению учёных, ничего столь же сложного люди потом не делали больше тысячи лет.", [
    dict(bg="library", cast=[(S, 540, dict(expr="smug", arm_r=90))], cam=(1.4, 540, 1000), sign="1000+ ЛЕТ"),
    dict(bg="library", cast=[(S, 540, dict(expr="worried"))], cam=(2.0, 540, 900))]),
 (10, "Кто его сделал и сколько таких машин было на самом деле, неизвестно до сих пор.", [
    dict(bg="dark", cast=[(S, 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
