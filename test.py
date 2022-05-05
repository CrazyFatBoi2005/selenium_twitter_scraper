search_base = [
    ['01-31', '02-01'],
    ['03-05', '03-06'],
    ['03-21', '03-22'],
    ['03-25', '03-26'],
    ['03-27', '03-28'],
    ['04-21', '04-22'],
    ['05-28', '05-29'],
    ['08-01', '08-02'],
    ['08-11', '08-12'],
]
print(search_base)

for key in search_base:
    search_term = f"(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-{key[0]} since:2020-{key[1]}"
    print(search_term)

m = "(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-02-01 since:2020-01-31"
b = "(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-01-31 since:2020-02-01"
k = "(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-02-01 since:2020-01-31(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-03-06 since:2020-03-05(#Covid OR #Covid19 OR #Covid-19 OR #Пандемия OR #Коронавирус OR #Ковид) lang:ru until:2020-03-22 since:2020-03-21"