# Philosophical zombies. Sources: Stanford Encyclopedia of Philosophy "Zombies" (Kirk 1974; Chalmers 1996;
# conceivability argument; critics incl. Dennett); PhilPapers survey 2013 (Bourget & Chalmers).
# (n, narration, shots) ; each shot = dict(bg, cast=[(who, x, pose)], cam=(zoom, fx, fy), bubble, sign, fx)
# who: hero | twin | phil | critic | neighbour ; pose: rig.draw kwargs (+ "talk": True to lip-sync)
H, T = "hero", "twin"
SCENES = [
 (1, "Представь человека, который смеётся, говорит «мне больно» и спорит о смысле жизни.", [
    dict(bg="street", cast=[(H, 540, dict(expr="happy", arm_r=60))], cam=(1.25, 540, 1150)),
    dict(bg="street", cast=[(H, 540, dict(expr="talk", talk=True, arm_l=40))], cam=(1.9, 540, 900)),
    dict(bg="street", cast=[(H, 540, dict(expr="worried", talk=True, arm_r=120))], cam=(1.4, 540, 1050))]),
 (2, "Но внутри у него никого нет.", [
    dict(bg="dark", cast=[(H, 540, dict(expr="neutral"))], cam=(1.8, 540, 900), bubble=(0, "off"))]),
 (3, "Это философский зомби. Не мертвец из кино.", [
    dict(bg="dark", cast=[(T, 540, dict(expr="neutral"))], cam=(1.2, 540, 1100), sign="ФИЛОСОФСКИЙ\nЗОМБИ"),
    dict(bg="cinema", cast=[(T, 540, dict(expr="smug", arm_r=90))], cam=(1.3, 540, 1050), fx="nozombie")]),
 (4, "Он атом в атом такой же, как ты: тот же мозг, те же слова, то же поведение.", [
    dict(bg="lab", cast=[(H, 330, dict(expr="neutral")), (T, 750, dict(expr="neutral"))], cam=(1.0, 540, 960), sign="="),
    dict(bg="lab", cast=[(H, 330, dict(expr="talk", talk=True, arm_r=60)), (T, 750, dict(expr="talk", talk=True, arm_l=60))], cam=(1.5, 540, 950)),
    dict(bg="lab", cast=[(H, 330, dict(expr="happy", arm_l=150, arm_r=150)), (T, 750, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.15, 540, 1000))]),
 (5, "Обожжёт палец — отдёрнет руку и крикнет «ай!».", [
    dict(bg="lab", cast=[(T, 540, dict(expr="neutral", arm_r=50))], cam=(1.5, 600, 1100), fx="flame"),
    dict(bg="lab", cast=[(T, 540, dict(expr="shock", arm_r=160, talk=True, lean=-6))], cam=(1.9, 540, 900), fx="ouch")]),
 (6, "Но самой боли он не почувствует. Внутри — темнота.", [
    dict(bg="dark", cast=[(T, 540, dict(expr="shock", arm_r=160))], cam=(1.4, 540, 1000)),
    dict(bg="dark", cast=[(T, 540, dict(expr="neutral"))], cam=(2.1, 540, 880), bubble=(0, "off"))]),
 (7, "Термин придумал философ Роберт Кёрк в тысяча девятьсот семьдесят четвёртом году.", [
    dict(bg="library", cast=[("phil", 540, dict(expr="smug", talk=True, arm_r=110))], cam=(1.3, 540, 1050), sign="1974"),
    dict(bg="library", cast=[("phil", 540, dict(expr="happy", arm_r=110))], cam=(1.9, 540, 900))]),
 (8, "А знаменитым его сделал Дэвид Чалмерс в книге «Сознающий ум» в девяносто шестом.", [
    dict(bg="library", cast=[("phil2", 540, dict(expr="talk", talk=True, arm_l=70))], cam=(1.3, 540, 1050), fx="book"),
    dict(bg="library", cast=[("phil2", 540, dict(expr="smug"))], cam=(1.6, 540, 1000), sign="1996")]),
 (9, "Его довод: если такого зомби можно представить без противоречий, значит, сознание — это что-то сверх физики.", [
    dict(bg="lab", cast=[(H, 330, dict(expr="neutral")), (T, 750, dict(expr="neutral"))], cam=(1.0, 540, 960), bubble=(0, "on")),
    dict(bg="lab", cast=[(H, 330, dict(expr="neutral")), (T, 750, dict(expr="neutral"))], cam=(1.15, 540, 960), bubble=(1, "off")),
    dict(bg="dark", cast=[("phil2", 540, dict(expr="talk", talk=True, arm_r=130))], cam=(1.7, 540, 950), bubble=(0, "on"))]),
 (10, "Критики, например Дэниел Деннет, отвечают: на самом деле представить его нельзя. Нам это только кажется.", [
    dict(bg="library", cast=[("phil2", 300, dict(expr="worried")), ("critic", 780, dict(expr="angry", talk=True, arm_l=90))], cam=(1.1, 540, 1000)),
    dict(bg="library", cast=[("critic", 540, dict(expr="angry", talk=True, rage=0.6, steam=True, arm_l=110))], cam=(1.9, 540, 900)),
    dict(bg="library", cast=[("phil2", 300, dict(expr="shock")), ("critic", 780, dict(expr="smug"))], cam=(1.2, 540, 1000))]),
 (11, "Философы спорят до сих пор.", [
    dict(bg="library", cast=[("phil2", 300, dict(expr="angry", talk=True, arm_r=80)), ("critic", 780, dict(expr="angry", talk=True, arm_l=80))], cam=(1.25, 540, 1000))]),
 (12, "И вот что неприятно: ты не можешь доказать, что твой сосед не зомби.", [
    dict(bg="street", cast=[(H, 300, dict(expr="worried")), ("neighbour", 780, dict(expr="happy", arm_l=120))], cam=(1.1, 540, 1000)),
    dict(bg="street", cast=[("neighbour", 540, dict(expr="happy", arm_l=120))], cam=(1.8, 540, 900), bubble=(0, "?"))]),
 (13, "А он не может доказать это про тебя.", [
    dict(bg="street", cast=[("neighbour", 300, dict(expr="worried")), (H, 780, dict(expr="smug"))], cam=(1.2, 540, 1000)),
    dict(bg="dark", cast=[(H, 540, dict(expr="smug"))], cam=(2.2, 540, 870), bubble=(0, "?"))]),
]
