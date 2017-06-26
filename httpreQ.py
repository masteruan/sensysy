import httplib

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()
httpServ = httplib.HTTPConnection("beta.joule40.com", 80)
#httpServ = httplib.HTTPConnection("api.thingspeak.com", 80)
httpServ.connect()
httpServ.request("GET", "/wp-content/themes/wpbootstrap/check_consumption.php?id_smartobject=2&temperatura=19.5&umidita=2.5&aria=20&presenza=1")
#httpServ.request("GET", "/update?api_key=7JUW5OPBI90Q3S2N&field1=33")

response = httpServ.getresponse()
result = response.read()
if response.status == httplib.OK:
    print "Output from HTML request"
    print (result)
    if result == "value=44444444":
        print "44 gatti in fila per 6"
    elif result == "value=14444414":
        print "Sticassi"
httpServ.close()
