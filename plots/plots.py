import json
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import statistics
from jobs.jobs.regex import get_digits

with open('/home/rafael/Documentos/cco-ufsc/20.2/ine5454/projeto/jobs/jobs.json', encoding='utf8') as out:
    jobs = json.load(out)


def bar_hiring_type_and_mode():
    on_site = [0, 0]
    remote = [0, 0]

    for job in jobs:
        type = job["hiring_type"]
        mode = job["mode"]
        if type == "CLT":
            if mode == "Presencial":
                on_site[0] += 1
            if mode == "Remoto":
                on_site[1] += 1
        if type == "PJ":
            if mode == "Presencial":
                remote[0] += 1
            if mode == "Remoto":
                remote[1] += 1

    barWidth = 0.25
    br1 = np.arange(len(on_site))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, on_site, color='r', width=barWidth,
            edgecolor='grey', label='Presencial')
    plt.bar(br2, remote, color='g', width=barWidth,
            edgecolor='grey', label='Remoto')
    plt.xlabel('Tipo da contratação', fontweight='bold', fontsize=15)
    plt.ylabel('Quantidade da modalidade', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(on_site))], ['CLT', 'PJ'])

    plt.legend()
    plt.show()


def bar_salary_hierarchy():
    relation = {
        'Sênior': [],
        'Pleno': [],
        'Junior': [],
        'Estagiário': []
    }

    mean = []

    for job in jobs:
        salary = job["salary"]
        hierarchy = job["hierarchy"]
        if salary is not None and hierarchy is not None:
            digits = get_digits(salary)
            if digits != 0:
                if "£" in salary:
                    convert = (digits * 7000) / 13
                    if 500 < convert < 20000:
                        relation[hierarchy].append(convert)
                elif "€" in salary:
                    convert = (digits * 6000) / 13
                    if 500 < convert < 20000:
                        relation[hierarchy].append(convert)
                elif "US" in salary or "U$" in salary:
                    convert = (digits * 5000) / 13
                    if 500 < convert < 20000:
                        relation[hierarchy].append(convert)
                elif "R$" in salary:
                    if 500 < digits < 20000:
                        relation[hierarchy].append(digits)

    for k in relation.keys():
        print(relation.get(k))
        if len(relation.get(k)) == 0:
            relation.get(k).append(0)
        mean.append(statistics.mean(relation.get(k)))

    y_pos = np.arange(len(relation))
    plt.xlabel('Hierarquia', fontweight='bold', fontsize=15)
    plt.ylabel('Média salarial', fontweight='bold', fontsize=15)
    plt.xticks(y_pos, relation.keys())
    plt.bar(y_pos, mean)
    plt.show()


def salary_comparator():
    eu_na = []
    br = []

    for job in jobs:
        salary = job["salary"]
        if salary is not None:
            digits = get_digits(salary)
            if digits != 0:
                if "£" in salary:
                    convert = (digits * 7000) / 13
                    if 500 < convert < 20000:
                        eu_na.append(convert)
                elif "€" in salary:
                    convert = (digits * 6000) / 13
                    if 500 < convert < 20000:
                        eu_na.append(convert)
                elif "US" in salary or "U$" in salary or "k" in salary:
                    convert = (digits * 5000) / 13
                    if 500 < convert < 20000:
                        eu_na.append(convert)
                elif "R$" in salary:
                    if 500 < digits < 20000:
                        br.append(digits)

    salary_dict = {
        'Brasil': statistics.mean(br),
        'EU e NA': statistics.mean(eu_na)
    }

    y_pos = np.arange(len(salary_dict))
    plt.xlabel('Região', fontweight='bold', fontsize=15)
    plt.ylabel('Média salarial', fontweight='bold', fontsize=15)
    plt.bar(y_pos, salary_dict.values())
    plt.xticks(y_pos, salary_dict.keys())
    plt.show()


def pizza_mode():
    mode = {
        'Presencial': 0,
        'Remoto': 0
    }

    for job in jobs:
        m = job["mode"]
        if m == "Presencial" or m == "Remoto":
            mode[m] += 1

    fig1, ax1 = plt.subplots()
    ax1.pie(mode.values(), labels=mode.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90, explode=[0.1, 0])
    ax1.axis('equal')
    plt.show()


def words_frequency():
    all_words = []
    for job in jobs:
        title = job["title"]
        description = job["description"]
        if title is not None:
            for title_split in title.split():
                all_words.append(title_split.upper())
        if description is not None:
            for description_split in description.split():
                all_words.append(description_split.upper())

    counts = dict()
    for i in all_words:
        counts[i] = counts.get(i, 0) + 1

    text = " ".join([k * v for k, v in counts.items()])

    stopwords = ["PESSOA", "A", "E", "É", "O", "PARA", "TAMBÉM", "EM", "QUE", "UM", "NO", "DOS",
                 "DE", "|", "-", "VAGA", "DESCRIÇÃO", "ALGUÉM", "ALGUÉMPESSOA", "TO", "SEMPRE", "FAZ"]
    wordcloud = WordCloud(width=720, height=480, colormap="Blues", stopwords=stopwords).generate(text)

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


pizza_mode()
bar_hiring_type_and_mode()
bar_salary_hierarchy()
salary_comparator()
words_frequency()
