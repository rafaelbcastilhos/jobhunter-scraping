import re


def get_html_from_response(response):
    return ''.join(response.xpath("//body//text()").extract()).strip()


# regex para capturar a hierarquia/experiência
def search_hierarchy(html):
    if re.search(r'(?i)s[eêEÊ]nior', html):
        return "Sênior"

    elif re.search(r'(?i)pleno', html) or re.search(r'(?i)mid[-\s]?level', html):
        return "Pleno"

    elif re.search(r'(?i)j[uU]nior', html):
        return "Junior"

    elif re.search(r'(?i)est[aáAÁ]gi[(aáAÁ)rio]*', html) or re.search(r'(?i)trainee', html):
        return "Estagiário"

    else:
        return None


# regex para capturar o tipo da contratação
def search_hiring_type(html):
    if re.search(r'(?i)clt', html):
        return "CLT"

    elif re.search(r'(?i)pj', html):
        return "PJ"

    elif re.search(r'(?i)freela[ncer]?', html):
        return "Freelancer"

    else:
        return None


# regex para capturar o modo de trabalho
def search_mode(html):
    if re.search(r'(?i)presencial', html) or re.search(r'(?i)on[-\s]?site', html):
        return "Presencial"

    elif re.search(r'(?i)home[-\s]?office', html) or re.search(r'(?i)remot[eoEO]', html):
        return "Remoto"

    elif re.search(r'(?i)h[iíÍ]brido', html) or re.search(r'(?i)mixed', html):
        return "Híbrido"

    else:
        return None


# regex para capturar o salário com diferentes moedas e pontuação
def search_salary(html):
    salary = re.search(r'(?i)(R\$|€|£|USD|US\$)\s?(\d{1,4}(\.\d{3})?)(,\d{2})?(\.\d{2})?([kK])?', html)
    if salary:
        return salary.group()

    elif re.search(r'(?i)combinar', html):
        return "A combinar"

    else:
        return None


def get_digits(salary):
    digits = re.search(r'(?i)(\d+)', salary)
    if digits:
        return float(digits.group())
    else:
        return 0


# regex para capturar o título da vaga na tag title
def search_title(response):
    label_title = response.xpath('//title/text()').get()
    if label_title:
        return label_title

    else:
        return None


# regex para capturar a descrição da vaga quando possui a palavra chave "descrição || description"
def search_description(html):
    description = re.search(
        r'(?i)[\n\r][ \t]*((job)?descri[cCçÇpP][aAãÃtT][iI]?o[nN]?)[ \t]*([^n\r]*)[\r\n]+([^\r\n]+)', html)
    if description:
        return description.group()

    else:
        return None


keywords = [
    "engenheir", "desenvolvedor", "programador", "arquitet", "cientista", "back", "front", "analista", "sistema",
    "devops", "assistente", "ux", "designer", "engineer", "developer", "architect", "scientist", "software",
    "pcd", "full", "stack", "gerente", "gestor", "administrador", "manager", "marketing", "informática",
    "coordenador", "comercial", "talento", "executivo", "vendas", "estágio", "estagiári", "técnico", "especialista"
]


def regex_keyword_element(element):
    for word in keywords:
        regex = re.search(r'(?i)(%s)[ \t]*([^\n\r]*)[\r\n]+([^\r\n]+)' % str(word), element)
        if regex is not None:
            return regex.group()


def regex_keyword_label(label):
    for word in keywords:
        label_regex = re.search(r'(?i)(%s)' % str(word), label)
        if label_regex:
            return label


def search_general_title(response):
    label_title = response.xpath('//title/text()').get()
    label_regex = regex_keyword_label(label_title)
    if label_regex:
        return label_title

    h1_title = ''.join(response.xpath("//h1/text()").getall())
    h1_regex = None
    if label_regex is None:
        h1_regex = regex_keyword_element(h1_title)
        if h1_regex:
            return h1_regex

    h2_title = ''.join(response.xpath("//h2/text()").getall())
    h2_regex = None
    if h1_regex is None:
        h2_regex = regex_keyword_element(h2_title)
        if h2_regex is not None:
            return h2_regex

    h3_title = ''.join(response.xpath("//h3/text()").getall())
    h3_regex = None
    if h2_regex is None:
        h3_regex = regex_keyword_element(h3_title)
        if h3_regex is not None:
            return h3_regex

    a_title = ''.join(response.xpath("//a/text()").getall())
    a_regex = None
    if h3_regex is None:
        a_regex = regex_keyword_element(a_title)
        if a_regex is not None:
            return a_regex

    strong_title = ''.join(response.xpath("//strong/text()").getall())
    if a_regex is None:
        strong_regex = regex_keyword_element(strong_title)
        if strong_regex is not None:
            return strong_regex
