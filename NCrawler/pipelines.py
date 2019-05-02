# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from NCrawler.services.filters import relevance
from scrapy.exceptions import DropItem


class FilterDatePipeline(object):

    def process_item(self, item, spider):
        now = datetime.now()
        date_licitacao = int(item['numerocp'].split('/')[-1])
        if int(date_licitacao) == now.year:
            print(date_licitacao)
            return item
        else:
            raise DropItem("Licitação fora do ano atual")


class SendMail(object):

    def open_spider(self, spider):
        print("######### Iniciando o spider... #########")

    def process_item(self, item, spider):
        print("######## Processando pipelines... ##########")
        self.modalidade = str(item['modalidade'])
        self.objetivo = str(item['objetivo'])
        self.numerocp = str(item['numerocp'])
        # self.link = item['link']
        return item

    def close_spider(self, spider):
        nomePrefeitura = spider.name
        linkPrefeitura = spider.start_urls

        from_email = "b89b239862ecb5"
        to_email = "to@smtp.mailtrap.io"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = 'Licitacoes da Prefeitura de ' + nomePrefeitura



        intro = "Licitacoes da Prefeitura de " + nomePrefeitura + '\n'
        linkPage = "Link para a página de licitacões: " + str(linkPrefeitura) + '\n'


        head = '======================================================================================================='
        foot = '======================================================================================================='

        # body = 'oi'
        body = intro + '\n' + linkPage + '\n' + '\n\n' + head + '\n' + 'Modalidade: ' + self.modalidade + '\n' + 'Objetivo: ' + " ".join((self.objetivo.split()))  + '\n'+ 'Numero CP: ' + self.numerocp + '\n' + foot + '\n\n'
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.mailtrap.io", 2525)
        server.starttls()
        server.login(from_email, "f20851757ed914")
        text = msg.as_string()
        print("###### Enviando Email...######")
        server.sendmail(from_email, to_email, text)
        print('Email Enviado!!')
        server.quit()
        print('######## Fechando spider...#########')


class FilterSimilarityPipeline(object):
    def process_item(self, item, spider):
        print(relevance(item['objetivo']))
        if relevance(item['objetivo']) >= 75.0:
            return item
        else:
            raise DropItem("Licitação não é relacionada a marketing")


