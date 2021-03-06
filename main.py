#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#-----------------------------------------------------------------------------
# Incluimos los módulos necesarios.
#-----------------------------------------------------------------------------
from urllib2 import urlopen
import urllib2
from BeautifulSoup import BeautifulSoup
from PyQt4.uic.uiparser import QtGui
import sys
from Menu import *
import xlsxwriter



class WebViewCreator(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui =Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"),self.getAllData)
    def WriteExcel(self,lista):
        cont2 =0
        tot =0
        lim = 2000
        pag = len(lista)/2000
        if len(lista) <= 2000:
            workbook = xlsxwriter.Workbook('listado.xlsx')
            worksheet = workbook.add_worksheet()
            for i in lista:
                worksheet.write('A'+str(cont2),i[0])
                worksheet.write('B'+str(cont2),i[1])
                worksheet.write('C'+str(cont2),i[2])
                cont2+=1
            workbook.close()
        else:
            while tot <= pag:
                cont2 =0
                workbook = xlsxwriter.Workbook('listado'+str(tot)+'.xlsx')
                worksheet = workbook.add_worksheet()
                listatemp = lista[0:2000]
                for i in listatemp:
                    worksheet.write('A'+str(cont2),i[0])
                    worksheet.write('B'+str(cont2),i[1])
                    worksheet.write('C'+str(cont2),i[2])
                    cont2+=1
                del lista[0:2000]
                workbook.close()
                tot +=1
    def getAllData(self):
        cont2 = 1
        cont =1
        limite = 0

        limite = int(self.ui.lineEdit.text())
        lista=[]
    #Bucle para repetir por cada Página
        while cont < limite:
            #Montamos la url
            uri ="http://www.paginasamarillas.es/search/alojamientos/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/hotel/all-ct/"+str(cont)+"?what=Hotel"
            uri = str(uri)
            #Comprobamos
            if uri != "":
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
                    if datos in lista:
                        print "Duplicado"
                        #Reinicializamos los datos
                        nombre = ""
                        tlf=""
                        fin=""
                        email=""
                    else:
                        lista.append(datos)
                         #Reinicializamos los datos
                        nombre = ""
                        tlf=""
                        fin=""
                        email=""

            cont+=1
        self.WriteExcel(lista)


if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=WebViewCreator()
    myapp.show()
    sys.exit(app.exec_())
