# webscraping-jobhunter

Processo de Web Scraping realizando a coleta e a raspagem de dados de vagas de emprego, utilizando 
expressões regulares, xpaths e reconhecimento de entidade mencionada utilizando processamento de linguagem natural.

Tecnologias utilizadas:
- Scrapy 2.4.1
- Spacy 3.0.6 
- Matplotlib 3.3.4
- Numpy 1.19.5

Instalar dependências:

    pip install -r requirements.txt

Listagem de spiders:

    scrapy list

Execução de única spider:

    scrapy crawl <spider_name>

Execução de todas spiders:

    python run_spiders.py

Fluxograma:
![Fluxograma crawler](https://raw.githubusercontent.com/rafaelbcastilhos/webscraping-jobhunter/main/model_infra.png)

Seeds utilizadas:
- [StackOverflow Jobs](https://stackoverflow.com/jobs)
- [Catho](https://www.catho.com.br/vagas/)  
- [Vagas.com](https://www.vagas.com.br)

Atributos coletados:
- Título da vaga;
- Nome da empresa contratante;
- Breve descrição da função;
- Hierarquia (estágio, junior, pleno, sênior, ...);
- Tipo da contratação (PJ, CLT, ...);
- Modalidade (home office, presencial, híbrido, ...);
- Salário;
- URL da página.

