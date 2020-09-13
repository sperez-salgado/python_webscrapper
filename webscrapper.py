import pycurl
from appJar import gui
from io import BytesIO
import certifi

htmlbuffer = BytesIO()

myapp = gui()
myapp.addLabel("title", "Ingresa una dirección web para traela", 0, colspan=3)

myapp.addLabel("addrlabel", "Dirección:", 1, 0)
myapp.addEntry("addr", 1, 1)
myapp.setEntryDefault("addr","http://algunaURL.com")
myapp.addLabel("codelabel", "Contenido:")
myapp.addScrolledTextArea("code", colspan=3)

def clicme(button):
    if button == "Salir":
        myapp.stop()
    elif button == "Guardar":
        thehtml = htmlbuffer.getvalue()
        if thehtml == "":
            myapp.setTextArea("code","No hay nada que guardar") 
        else:
            path = myapp.getEntry("saveat")
            fileobj = open(path,"wb")
            fileobj.write(thehtml)
            fileobj.close()
			
    else:
        myapp.clearTextArea("code",callFunction=False)
        webaddr = myapp.getEntry("addr")
        if webaddr.startswith("http://") or webaddr.startswith("https://"):
            htmlcode = pycurl.Curl()
            htmlcode.setopt(htmlcode.URL, webaddr)
            htmlcode.setopt(htmlcode.WRITEDATA, htmlbuffer)
            if webaddr.startswith("https://"):
                htmlcode.setopt(htmlcode.CAINFO, certifi.where())			
            htmlcode.perform()
            htmlcode.close()
			
            thehtml = htmlbuffer.getvalue()
			
            myapp.setTextArea("code",thehtml.decode('iso-8859-1'))
            myapp.setButtonState("Guardar","active")
            myapp.setEntryState("saveat","normal")
        else:
            myapp.setTextArea("code","Intenta de nuevo, la dirección debe iniciar con http:// o https://")
		

myapp.addSaveEntry("saveat", colspan=3)
myapp.addButtons(["Traer", "Guardar", "Salir"], clicme, colspan=3)
myapp.setButtonState("Guardar","disabled")
myapp.setEntryDefault("saveat", "Guardar en...")
myapp.setEntryState("saveat","disabled")

myapp.go()