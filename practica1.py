#Laura Sanz Ruano

#!/usr/bin/python
#-*- coding: utf-8 -*-
import webapp
import urllib

class urlApp(webapp.webApp):
    urls1 = {} # clave: url real y valor el numero
    urls2 = {} # clave: el numero y valor la url real
    urlcorta = 0

    def parse(self, request):
        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]
        if metodo == 'POST':
            cuerpo = request.split('\r\n\r\n', 1)[1]
        elif metodo == 'GET':
            cuerpo = ''
        return(metodo, recurso, cuerpo)

    def process(self, resourceName):
        (metodo, recurso, cuerpo) = resourceName

        formulario = '<form action="" method="POST">'
        formulario += 'Acortar url: <input type="text" name="valor">'
        formulario += '<input type="submit" value="Enviar">'
        formulario += '</form>'

        if metodo == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                htmlBody = "<html><body>" + formulario + "<p> Urls almacenadas: "\
                        + str(self.urls1) + "</p></body></html>"
            else:
                try:
                    recurso = int(recurso[1:])
                    if recurso in self.urls2:
                        httpCode = "300 Redirect"
                        htmlBody = "<html><body><meta http-equiv='refresh'content='1 url="\
                                + self.urls2[recurso] + "'>" + "</p>" + "</body></html>"
                    else:
                        httpCode = "404 Not Found"
                        htmlBody = "<html><body> Error: Recurso no encontrado </body></html>"

                except ValueError:
                    httpCode = "404 Not Found"
                    htmlBody = "<html><body> Error: Recurso no encontrado </body></html>"

        elif metodo == "POST":
            if cuerpo == "":
                httpCode = "404 Not Found"
                httpBody = "<html><body> Error: no introdujo una url </body></html>"
                return (httpCode, htmlBody)
            if cuerpo.find("http%3A%2F%2F") >= 0:
                cuerpo = cuerpo.split('http%3A%2F%2F')[1]

            cuerpo = "http://" + cuerpo
            if cuerpo in self.urls1:
                urlcorta = self.urls1[cuerpo]
            else:
                urlcorta = self.urlcorta
                self.urlcorta = self.urlcorta + 1

            self.urls1[cuerpo] = urlcorta
            self.urls2[urlcorta] = cuerpo
            httpCode = "200 OK"
            htmlBody = "<html><body>URL original: <a href=" + cuerpo + ">" + cuerpo + "</href>"\
                    + "<p>URL acortada: <a href=" + str(urlcorta) + ">" + str(urlcorta)\
                    + "</href></body></html>"
            return (httpCode, htmlBody)

        else:
            httpCode = "404 Not Found"
            htmlBody = "<html><body> Metodo desconocido </body></html>"
        return (httpCode, htmlBody)

        if __name__ == "__main__":
            testWebApp = contentApp("localhost", 1234)
