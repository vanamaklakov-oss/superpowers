# Victor Lustig "sells" the Eiffel Tower, 1925 (a fraud, not a legal scheme). Sources: Wikipedia "Victor Lustig";
# Smithsonian Magazine "The Man Who Sold the Eiffel Tower"; History.com; FBI history (Lustig arrested 1935 for
# counterfeiting, sent to Alcatraz). Details differ by source: hotel (Crillon), buyer André Poisson, extra bribe,
# second attempt reported to police — told here with "по одной из версий".
L, P, D = "count", "dealer", "dealer2"
SCENES = [
 (1, "Один человек продал Эйфелеву башню. Причём два раза.", [
    dict(bg="paris", cast=[(L, 540, dict(expr="smug", arm_r=80))], cam=(1.3, 540, 1100)),
    dict(bg="paris", cast=[(L, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(2.0, 540, 900), fx="money")]),
 (2, "Париж, тысяча девятьсот двадцать пятый год. Мошенник Виктор Люстиг читает в газете: башня ветшает, её ремонт стоит огромных денег.", [
    dict(bg="cafe", cast=[(L, 540, dict(expr="neutral", arm_r=60))], cam=(1.2, 540, 1050), sign="1925"),
    dict(bg="cafe", cast=[(L, 540, dict(expr="smug"))], cam=(1.9, 540, 900), bubble=(0, "on"))]),
 (3, "Он выдаёт себя за чиновника и рассылает письма шести торговцам металлоломом.", [
    dict(bg="office", cast=[(L, 540, dict(expr="talk", talk=True, arm_r=90))], cam=(1.3, 540, 1050), fx="book", book_text="ПИСЬМО"),
    dict(bg="office", cast=[(L, 540, dict(expr="smug"))], cam=(1.7, 540, 950), sign="6")]),
 (4, "На тайной встрече в роскошном отеле он объявляет: башню снесут, а металл достанется тому, кто больше заплатит.", [
    dict(bg="hotel", cast=[(P, 280, dict(expr="shock")), (L, 540, dict(expr="talk", talk=True, arm_r=120)), (D, 800, dict(expr="shock"))], cam=(1.0, 540, 1000)),
    dict(bg="hotel", cast=[(L, 540, dict(expr="smug", arm_r=60))], cam=(1.9, 540, 900))]),
 (5, "И просит молчать: это государственная тайна.", [
    dict(bg="hotel", cast=[(L, 540, dict(expr="worried", talk=True))], cam=(2.1, 540, 880))]),
 (6, "Торговец Андре Пуассон мечтал попасть в высшее общество. И согласился.", [
    dict(bg="hotel", cast=[(P, 540, dict(expr="happy", arm_r=120))], cam=(1.3, 540, 1050), bubble=(0, "on")),
    dict(bg="hotel", cast=[(P, 330, dict(expr="happy")), (L, 750, dict(expr="smug"))], cam=(1.15, 540, 1000), fx="stamp", stamp_text="ПРОДАНО")]),
 (7, "По одной из версий, Люстиг взял деньги, да ещё и взятку сверху, и в тот же день уехал из страны.", [
    dict(bg="hotel", cast=[(L, 540, dict(expr="happy", arm_l=150, arm_r=150))], cam=(1.3, 540, 1050), fx="money"),
    dict(bg="station", cast=[(L, 540, dict(expr="smug", arm_r=90))], cam=(1.6, 540, 960))]),
 (8, "А Пуассону было так стыдно, что он даже не пошёл в полицию.", [
    dict(bg="paris", cast=[(P, 540, dict(expr="shock", sweat=True))], cam=(1.4, 540, 1000)),
    dict(bg="paris", cast=[(P, 540, dict(expr="worried"))], cam=(2.0, 540, 900))]),
 (9, "Через полгода Люстиг вернулся и попробовал продать башню снова.", [
    dict(bg="paris", cast=[(L, 540, dict(expr="smug", arm_r=80))], cam=(1.3, 540, 1050), sign="СНОВА"),
    dict(bg="hotel", cast=[(L, 330, dict(expr="talk", talk=True)), (D, 750, dict(expr="neutral"))], cam=(1.15, 540, 1000))]),
 (10, "Но новая жертва обратилась в полицию, и мошеннику пришлось бежать.", [
    dict(bg="hotel", cast=[(D, 540, dict(expr="angry", rage=0.8, steam=True, talk=True))], cam=(1.8, 540, 920)),
    dict(bg="station", cast=[(L, 540, dict(expr="shock", sweat=True, lean=-6))], cam=(1.3, 540, 1050))]),
 (11, "Позже его всё же поймали в Америке. За подделку денег он попал в тюрьму Алькатрас.", [
    dict(bg="prison", cast=[(L, 540, dict(expr="worried"))], cam=(1.3, 540, 1050)),
    dict(bg="prison", cast=[(L, 540, dict(expr="smug"))], cam=(2.2, 540, 870))]),
]
