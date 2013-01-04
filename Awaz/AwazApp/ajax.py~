from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

@dajaxice_register
def say_hello(req):
    dajax = Dajax()
    dajax.alert("Hello World!")
    return dajax.json()
