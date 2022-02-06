from django.shortcuts import render
import googletrans
from googletrans import Translator


def index(request):
    context = {
        "ndict": googletrans.LANGUAGES,
    }
    if request.method == "POST":
        bf = request.POST.get("bf")
        fr = request.POST.get("fr")
        to = request.POST.get("to")
        translator = Translator()
        trans1 = translator.translate(bf, src=fr, dest=to)
        context.update({
            "bf":bf,
            "fr":fr,
            "to":to,
            "af":trans1.text
        })
   
    return render(request, 'trans/index.html', context)