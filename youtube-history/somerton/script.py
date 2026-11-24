# The Somerton Man (Tamam Shud case), Adelaide 1948. Sources: Wikipedia "Somerton Man"; Smithsonian Magazine (2022)
# "Have scholars finally identified the mysterious Somerton Man?"; UPI / InDaily (26–27 Jul 2022). Found 1 Dec 1948 on
# Somerton beach; no ID, clothing labels removed; cause of death undetermined; scrap "Tamám Shud" ("it is ended") from
# Omar Khayyam's Rubaiyat in a fob pocket; the matching book had pencilled letters ("the code"), never deciphered.
# 2022: Prof. Derek Abbott & Colleen Fitzpatrick named Carl "Charles" Webb (b. 1905, Melbourne) via DNA from hair in the
# death mask; South Australia Police have not officially confirmed it.
D, A = "detective", "doctor"
SCENES = [
 (0, "Его имя искали семьдесят четыре года.", [
    dict(bg="beach", cast=[], cam=(1.5, 540, 1000), hook="ИМЯ ИСКАЛИ\n74 ГОДА")]),
 (1, "Декабрь тысяча девятьсот сорок восьмого года. На пляже Сомертон в Австралии находят умершего мужчину в аккуратном костюме.", [
    dict(bg="beach", cast=[(D, 540, dict(expr="worried", arm_r=80))], cam=(1.2, 540, 1050), sign="1948"),
    dict(bg="beach", cast=[(D, 540, dict(expr="shock", sweat=True))], cam=(1.9, 540, 900))]),
 (2, "У него нет документов, а с одежды срезаны все бирки.", [
    dict(bg="morgue", cast=[(D, 540, dict(expr="neutral", talk=True))], cam=(1.4, 540, 1000), bubble=(0, "?"))]),
 (3, "Причину смерти так и не установили.", [
    dict(bg="morgue", cast=[(A, 540, dict(expr="worried", sweat=True))], cam=(1.7, 540, 950), fx="stamp", stamp_text="НЕИЗВЕСТНО")]),
 (4, "А в крошечном потайном кармашке брюк нашли клочок бумаги с двумя словами: «Тамам шуд».", [
    dict(bg="morgue", cast=[(D, 540, dict(expr="shock", arm_r=110))], cam=(1.3, 540, 1050), sign="TAMÁM SHUD"),
    dict(bg="morgue", cast=[(D, 540, dict(expr="neutral"))], cam=(1.9, 540, 900))]),
 (5, "С персидского это значит «конец». Так заканчивается сборник стихов Омара Хайяма.", [
    dict(bg="library", cast=[(A, 540, dict(expr="talk", talk=True, arm_l=80))], cam=(1.3, 540, 1050), fx="book", book_text="ОМАР\nХАЙЯМ")]),
 (6, "Позже нашли и саму книгу, из которой вырвали этот клочок. А в ней — карандашные строчки из непонятных букв.", [
    dict(bg="street", cast=[(D, 540, dict(expr="happy", arm_r=130))], cam=(1.2, 540, 1050)),
    dict(bg="library", cast=[(D, 540, dict(expr="shock"))], cam=(1.8, 540, 930), sign="WRGOABABD"),
    dict(bg="library", cast=[(A, 540, dict(expr="worried"))], cam=(1.5, 540, 970), bubble=(0, "?"))]),
 (7, "Эти строчки не расшифрованы до сих пор.", [
    dict(bg="library", cast=[(A, 540, dict(expr="angry", rage=0.7, steam=True))], cam=(1.9, 540, 900))]),
 (8, "Шпион, несчастный влюблённый, отравление — версий были десятки.", [
    dict(bg="morgue", cast=[(D, 540, dict(expr="talk", talk=True, arm_r=90))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ШПИОН?", "ЛЮБОВЬ?", "ЯД?"])]),
 (9, "А в две тысячи двадцать втором году профессор Дерек Эбботт объявил: по ДНК из волоса удалось найти имя.", [
    dict(bg="library", cast=[(A, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050), sign="2022"),
    dict(bg="library", cast=[(A, 540, dict(expr="smug", talk=True))], cam=(1.8, 540, 930), bubble=(0, "on"))]),
 (10, "По его данным, это инженер из Мельбурна Карл Уэбб.", [
    dict(bg="street", cast=[(A, 540, dict(expr="smug", arm_r=110))], cam=(1.4, 540, 1000), sign="КАРЛ УЭББ?")]),
 (11, "Полиция эту версию официально не подтвердила. А что значат таинственные строчки, неизвестно до сих пор.", [
    dict(bg="morgue", cast=[(D, 540, dict(expr="neutral"))], cam=(1.3, 540, 1050), fx="stamp", stamp_text="НЕ ПОДТВЕРЖДЕНО"),
    dict(bg="beach", cast=[], cam=(2.0, 540, 900))]),
]
