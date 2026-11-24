# The Green Children of Woolpit (12th c., Suffolk). Sources: Wikipedia "Green children of Woolpit"; Mental Floss;
# Canterbury Christ Church Univ. repository (Preternature article). Two chroniclers: William of Newburgh (Historia rerum
# Anglicarum, c. 1189–98) and Ralph of Coggeshall (Chronicum Anglicanum, c. 1220s); neither saw the children; reign of
# King Stephen (or Henry II); found by the wolf pits at harvest; green skin, unknown language, strange clothes; ate only
# raw broad beans at first; colour faded; the boy died; the girl was baptised, worked, married (King's Lynn); Ralph: their
# land was green and twilit. Proposed explanations: lost/starving Flemish orphans, chlorosis from poor diet, arsenic.
B, Gl, F = "greenboy", "greengirl", "peasant"
SCENES = [
 (0, "По легенде, из ямы вышли дети с зелёной кожей.", [
    dict(bg="pit", cast=[(B, 330, dict(expr="worried")), (Gl, 750, dict(expr="worried"))], cam=(1.5, 540, 1000), hook="ДЕТИ\nС ЗЕЛЁНОЙ КОЖЕЙ")]),
 (1, "Англия, двенадцатый век, деревня Вулпит.", [
    dict(bg="field", cast=[(F, 540, dict(expr="happy", arm_r=110))], cam=(1.2, 540, 1050), sign="XII ВЕК")]),
 (2, "Крестьяне на жатве находят у глубокой ямы двух детей, брата и сестру.", [
    dict(bg="pit", cast=[(F, 540, dict(expr="shock", sweat=True))], cam=(1.4, 540, 1000)),
    dict(bg="pit", cast=[(B, 330, dict(expr="shock")), (Gl, 750, dict(expr="worried"))], cam=(1.15, 540, 1000))]),
 (3, "Их кожа зелёного цвета. Говорят они на непонятном языке и одеты в странную одежду.", [
    dict(bg="field", cast=[(B, 540, dict(expr="talk", talk=True))], cam=(1.8, 540, 930)),
    dict(bg="field", cast=[(F, 540, dict(expr="shock"))], cam=(1.6, 540, 960), bubble=(0, "?"))]),
 (4, "Несколько дней дети ничего не едят. Пока не увидели сырые бобы.", [
    dict(bg="cottage", cast=[(Gl, 540, dict(expr="worried", sweat=True))], cam=(1.4, 540, 1000)),
    dict(bg="cottage", cast=[(Gl, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.8, 540, 930))]),
 (5, "Со временем они привыкли к обычной еде, и зелёный цвет кожи пропал.", [
    dict(bg="cottage", cast=[("agnes", 540, dict(expr="happy", arm_r=110))], cam=(1.3, 540, 1050))]),
 (6, "Мальчик вскоре умер. А девочка выросла, выучила язык и вышла замуж.", [
    dict(bg="church", cast=[("agnes", 540, dict(expr="worried"))], cam=(1.4, 540, 1000)),
    dict(bg="church", cast=[("agnes", 330, dict(expr="happy")), ("villager", 750, dict(expr="happy"))], cam=(1.15, 540, 1000))]),
 (7, "По её рассказу, на их родине всё было зелёным, а солнце там почти не светило.", [
    dict(bg="dark", cast=[("agnes", 540, dict(expr="talk", talk=True, arm_l=90))], cam=(1.5, 540, 970), bubble=(0, "?"))]),
 (8, "Эту историю записали два средневековых хрониста. Но сами они детей не видели.", [
    dict(bg="cottage", cast=[("missionary", 330, dict(expr="neutral", talk=True)), ("scholar", 750, dict(expr="smug"))], cam=(1.15, 540, 1000), fx="book", book_text="ХРОНИКА")]),
 (9, "Историки предлагают простое объяснение: потерявшиеся голодные дети, у которых от плохой еды кожа стала зеленоватой.", [
    dict(bg="field", cast=[("doctor", 540, dict(expr="smug", talk=True, arm_r=100))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["ГОЛОД", "= ЗЕЛЁНАЯ КОЖА?"])]),
 (10, "Правда это или красивая легенда, узнать уже невозможно.", [
    dict(bg="pit", cast=[], cam=(1.3, 540, 1000)),
    dict(bg="dark", cast=[("doctor", 540, dict(expr="neutral"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
