# -*- coding: utf-8 -*-
import scrapy
from NCrawler.items import BiddingItem
import re

class AcailandiaSpider(scrapy.Spider):
    name = 'Acailandia'
    allowed_domains = ['acailandia.ma.gov.br']
    start_urls = ['https://www.acailandia.ma.gov.br/licitacoes?modalidade=&paginaView=&setor=2&status=&numero=&objeto=']

    def parse(self, response):

        for modalidade in response.css('div#ListModalidades a'):
            link = modalidade.css('a::attr(href)').extract_first()
            yield response.follow(link, self.parse_binding)

    def parse_binding(self, response):
        for licitacao in response.css('div.buscar_licitacao_anexos div.panel-default'):
            link = licitacao.css('div.panel-body a::attr(href)').extract_first()
            modalidade = ' '.join(licitacao.css('div.panel-heading strong::text').extract_first().split()[:-2])
            numerocp = "".join(licitacao.css('div.panel-heading strong::text').re(r'\d*[/|_]+\d*'))
            objetivo = licitacao.css('div.panel-body::text').getall()[4]
            yield BiddingItem(link=link, modalidade=modalidade, numerocp=numerocp, objetivo=objetivo)


