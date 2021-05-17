# webscraping-jobhunter

Processo de Web Scraping realizando a coleta de dados de vagas de emprego.

Tecnologias utilizadas:
- Scrapy 2.4.1
- Spacy 3.0.6 
- Matplotlib 3.3.4
- Numpy 1.19.5

Fluxograma:
![Fluxograma crawler](https://github.com/rafaelbcastilhos/webscraping-jobhunter/blob/main/model_infra.png?raw=true)

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

