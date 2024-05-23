from inmobiliaria_app.models import Usuario, Inmueble, Usuario_Inmueble
from django.db import connections
cursor = connections['default'].cursor()
cursor.execute("select * from usuario where nombres like '%jess%'")
print(cursor.fetchall())

# manually close the cursor if you are done!
cursor.close()
# select = """select * from usuario where nombres like '%jess%'"""

# query = Usuario.objects.raw(select)

# for p in query:
#     print(p.nombres)
#     print(p.apellidos)



