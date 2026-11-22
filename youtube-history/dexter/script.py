# "Lord" Timothy Dexter (1747–1806), Newburyport, Massachusetts. Sources: Wikipedia "Timothy Dexter"; New England
# Historical Society "Timothy Dexter, the ridiculous millionaire who sold coals to Newcastle"; Britannica Kids; his own
# book "A Pickle for the Knowing Ones" (1802; 2nd ed. added a page of punctuation marks). The warming-pan and coal stories
# are legend/self-promotion — told with "по легенде". Mansion with wooden statues incl. himself.
X = "dexter"
SCENES = [
 (1, "Над этим человеком смеялся весь город. А он разбогател на их издевательских советах.", [
    dict(bg="street", cast=[("friend", 330, dict(expr="happy", talk=True, arm_r=150)), (X, 750, dict(expr="worried"))], cam=(1.1, 540, 1000)),
    dict(bg="mansion", cast=[(X, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.8, 540, 930), fx="money")]),
 (2, "Тимоти Декстер, Массачусетс, конец восемнадцатого века. Малограмотный выскочка, который мечтал стать знатью.", [
    dict(bg="street", cast=[(X, 540, dict(expr="smug", arm_r=90, talk=True))], cam=(1.2, 540, 1050), sign="1790-е"),
    dict(bg="street", cast=[(X, 540, dict(expr="happy"))], cam=(1.8, 540, 930))]),
 (3, "Купцы решили его разорить и посоветовали: отправь грелки для постели в тропики.", [
    dict(bg="street", cast=[("dealer", 330, dict(expr="smug", talk=True, arm_r=100)), (X, 750, dict(expr="neutral"))], cam=(1.15, 540, 1000)),
    dict(bg="street", cast=[("dealer", 540, dict(expr="happy"))], cam=(1.9, 540, 900), bubble=(0, "on"))]),
 (4, "Декстер так и сделал. Кто в жару купит грелку?", [
    dict(bg="harbor", cast=[(X, 540, dict(expr="happy", arm_r=140))], cam=(1.3, 540, 1050)),
    dict(bg="harbor", cast=[(X, 540, dict(expr="neutral"))], cam=(1.8, 540, 930), bubble=(0, "?"))]),
 (5, "По легенде, на островах грелки раскупили сахарные плантаторы. Как черпаки для патоки.", [
    dict(bg="harbor", cast=[("dealer2", 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050)),
    dict(bg="treasury", cast=[(X, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.25, 540, 1050), fx="money")]),
 (6, "Тогда ему посоветовали везти уголь в Ньюкасл — английский город угольщиков.", [
    dict(bg="street", cast=[("dealer", 540, dict(expr="smug", talk=True, arm_r=90))], cam=(1.5, 540, 970)),
    dict(bg="street", cast=[(X, 540, dict(expr="smug"))], cam=(1.3, 540, 1050), fx="calc", calc_lines=["УГОЛЬ В НЬЮКАСЛ", "= РАЗОРЕНИЕ?"])]),
 (7, "Это всё равно что продавать снег на Северном полюсе.", [
    dict(bg="street", cast=[("friend", 330, dict(expr="happy", arm_r=150)), ("friend2", 750, dict(expr="happy", arm_l=150))], cam=(1.1, 540, 1000))]),
 (8, "Но когда корабль пришёл, шахтёры Ньюкасла бастовали. И уголь раскупили втридорога.", [
    dict(bg="harbor", cast=[(X, 540, dict(expr="shock"))], cam=(1.4, 540, 1000)),
    dict(bg="harbor", cast=[(X, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.25, 540, 1050), fx="stamp", stamp_text="ПРОДАНО")]),
 (9, "Декстер купил особняк и поставил в саду десятки деревянных статуй. Среди них была и его собственная.", [
    dict(bg="mansion", cast=[(X, 540, dict(expr="smug", arm_r=120, talk=True))], cam=(1.2, 540, 1050)),
    dict(bg="mansion", cast=[(X, 330, dict(expr="happy")), (X, 750, dict(expr="neutral"))], cam=(1.15, 540, 1000))]),
 (10, "А ещё написал книгу совсем без знаков препинания. И добавил в конце страницу точек и запятых: расставляйте сами.", [
    dict(bg="room", cast=[(X, 540, dict(expr="smug", talk=True, arm_l=70))], cam=(1.3, 540, 1050), fx="book", book_text="БЕЗ\nТОЧЕК"),
    dict(bg="room", cast=[(X, 540, dict(expr="happy"))], cam=(1.7, 540, 950), sign=". , . , ; . ,")]),
 (11, "Историки сомневаются, что всё было именно так. Но сам Декстер эти истории рассказывал с удовольствием.", [
    dict(bg="mansion", cast=[(X, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
