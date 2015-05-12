#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#-----------------------------------------------------------------------------
# Incluimos los módulos necesarios.
#-----------------------------------------------------------------------------
from urllib2 import urlopen
import urllib2
from BeautifulSoup import BeautifulSoup
import math
from PyQt4.uic.uiparser import QtGui
import pyExcelerator
from PyQt4 import QtWebKit
import sys
import requests
from Menu import *
from excel import Excel



class WebViewCreator(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui =Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"),self.getAllData)

    def getAllData(self):
        i=0
        cont =1
        url = "http://www.paginasamarillas.es/search/alojamientos/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/hotel/all-ct/1?what=Hotel"
        url =str(url)
        soup2 = BeautifulSoup(urlopen(url))
        totpag = soup2.find("span",{"class":"m-header--count"}).contents[0]
        totpag = totpag.split("resultados")
        result = float(totpag[0].strip())
        #result = int(math.ceil(result/15))
        result = int(3)
        lista=[]
        while cont < 20:
            uri ="http://www.paginasamarillas.es/search/alojamientos/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/hotel/all-ct/"+str(cont)+"?what=Hotel"
            uri = str(uri)
            headers = { 'User-Agent' : 'Mozilla/5.0' }
            html = urllib2.urlopen(urllib2.Request(uri, None, headers)).read()
            if url != "":
                header = ['Nombre', 'Telefono', 'Email']
                excel = Excel()
                excel.write_with_format(header, bold=True)
                soup = BeautifulSoup(urlopen(uri))
                #Recogemos cada uno de los li que contengan estas clases
                total = soup.findAll("li",{"class":["m-results-business m-results-business-advert","m-results-business"]})
                #Recorremos la lista una a  una
                for i in total:
                    #Buscamos la cabecera para recoger el nombre (NO DUPLICA)
                    nombre =i.find("h3", {"class": "m-results-business--name"}).span.contents[0]
                    #Buscamos el li 'is-omega' que contiene la info del telefono
                    stotal =i.findAll("li", {"class": "is-omega"})
                    stotal = filter(None, stotal)
                    for j in stotal:
                    #Recogemos el valor del campo span (NO DUPLICA)
                        tlf= j.find("span", {"class": "m-icon--single-phone"}).contents[0]
                    #Recogemos el valor de 'is-maxi' que contiene el mail
                    email=i.findAll("li", {"class": "is-maxi"})
                    for j in email:
                    #recogemos el href de a y lo parseamos para generar un email correcto
                        parsemail=j.find("a").get("href")
                        parsemail = parsemail.split('=')
                        prueba = parsemail[1].split('&')
                        fin= prueba[0].replace("%40","@")
                    #Creamos el registro
                    datos=[nombre,tlf,fin]
                    lista.append(datos)

            cont+=1
        for i in lista:
            #Escribimos el registro en la excel
            print str(i)
            excel.write_row(i)
         #Guardamos la excel
            excel.save()


if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=WebViewCreator()
    myapp.show()
    sys.exit(app.exec_())
