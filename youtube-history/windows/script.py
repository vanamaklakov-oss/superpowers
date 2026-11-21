# The English window tax, 1696–1851. Sources: Wikipedia "Window tax"; The National Archives (UK) blog on the
# window tax; Mental Floss; Historic England. Introduced under William III to cover losses from clipped coinage /
# the Great Recoinage; flat 2 shillings + 4 s (10–20 windows) / + 8 s (over 20). Bricked-up windows still visible.
# Repealed in 1851 (replaced by house duty). Doctors and campaigners blamed it for disease in dark, airless homes.
# NOT used: the "daylight robbery" etymology myth.
K, X, V, R = "king", "taxman", "villager", "rich"
SCENES = [
 (1, "В Англии когда-то брали налог за солнечный свет. Точнее, за окна.", [
    dict(bg="street", cast=[(X, 540, dict(expr="smug", arm_r=70))], cam=(1.3, 540, 1100)),
    dict(bg="street", cast=[(X, 540, dict(expr="happy", arm_r=140))], cam=(2.0, 540, 900), fx="money")]),
 (2, "Тысяча шестьсот девяносто шестой год. Королю Вильгельму Третьему срочно нужны деньги.", [
    dict(bg="palace", cast=[(K, 540, dict(expr="worried", talk=True))], cam=(1.2, 540, 1050), sign="1696"),
    dict(bg="palace", cast=[(K, 540, dict(expr="angry", rage=0.6, steam=True))], cam=(1.9, 540, 900))]),
 (3, "Монеты в стране испорчены: мошенники срезали серебро с краёв. Перечеканка стоит огромных денег.", [
    dict(bg="treasury", cast=[(K, 540, dict(expr="shock", sweat=True))], cam=(1.4, 540, 1000)),
    dict(bg="treasury", cast=[(K, 540, dict(expr="worried"))], cam=(1.2, 540, 1050), fx="calc", calc_lines=["СРЕЗАЛИ СЕРЕБРО", "= ПЕРЕЧЕКАНКА", "= НУЖЕН НАЛОГ"])]),
 (4, "И придумали налог, который легко проверить снаружи.", [
    dict(bg="palace", cast=[(K, 540, dict(expr="smug", arm_r=90))], cam=(1.8, 540, 920), bubble=(0, "on"))]),
 (5, "Сборщику не нужно входить в дом. Встал на улице, посчитал окна и выписал счёт.", [
    dict(bg="street", cast=[(X, 540, dict(expr="neutral", arm_r=110))], cam=(1.3, 540, 1050)),
    dict(bg="street", cast=[(X, 330, dict(expr="smug", talk=True)), (V, 750, dict(expr="shock"))], cam=(1.15, 540, 1000), fx="stamp", stamp_text="ОПЛАТИТЬ")]),
 (6, "Чем больше окон, тем больше платишь. Больше десяти — дороже. Больше двадцати — ещё дороже.", [
    dict(bg="mansion", cast=[(R, 540, dict(expr="worried", sweat=True))], cam=(1.3, 540, 1050), sign="10+\n20+"),
    dict(bg="mansion", cast=[(R, 540, dict(expr="angry", rage=0.8, steam=True))], cam=(2.0, 540, 900))]),
 (7, "Англичане нашли выход. Они стали закладывать окна кирпичом.", [
    dict(bg="bricked", cast=[(V, 540, dict(expr="smug", arm_r=120))], cam=(1.3, 540, 1050)),
    dict(bg="bricked", cast=[(X, 540, dict(expr="shock"))], cam=(2.0, 540, 900))]),
 (8, "Такие заложенные окна до сих пор можно увидеть на старых домах.", [
    dict(bg="bricked", cast=[], cam=(1.25, 540, 900))]),
 (9, "А в домах бедняков стало темно и душно. Врачи жаловались, что люди болеют.", [
    dict(bg="room", cast=[(V, 540, dict(expr="worried", sweat=True))], cam=(1.5, 540, 1000)),
    dict(bg="room", cast=[(V, 330, dict(expr="worried")), ("doctor", 750, dict(expr="angry", talk=True, arm_l=90))], cam=(1.15, 540, 1000))]),
 (10, "Налог продержался больше ста пятидесяти лет. Его отменили только в тысяча восемьсот пятьдесят первом году.", [
    dict(bg="street", cast=[(X, 540, dict(expr="worried"))], cam=(1.3, 540, 1050), sign="1851"),
    dict(bg="street", cast=[(V, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050))]),
 (11, "Государство хотело денег. А получило страну с кирпичными окнами.", [
    dict(bg="bricked", cast=[(K, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
