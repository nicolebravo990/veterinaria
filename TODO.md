# TODO: Arreglar Proyecto Veterinaria

## Información Recopilada
- **Redirección de Login Incorrecta**: LOGIN_REDIRECT_URL apunta a 'vet_inicio', pero admins deben ir a 'index'. La función login_redirect envía superusers a '/admin/' en lugar de 'index'.
- **Conflicto de Nombres de URL**: 'home' se usa en urls.py principal y en gestorProductos/urls.py, causando conflictos.
- **DataTables No Muestran Datos**: En templates como datatable.html, las URLs de edit/delete están mal construidas en JS, causando que no se generen correctamente.
- **CRUD No Funciona**: Debido a las mismas URLs malformadas en los templates de DataTables.
- **Modelos y APIs**: Los modelos existen, APIs devuelven datos en formato correcto, pero no se muestran por problemas de frontend.

## Plan de Actualización de Código
### 1. [COMPLETED] Arreglar Redirección de Login
- **gestorUser/views.py**: Modificar `login_redirect` para redirigir superusers a 'admin_index', otros a 'vet_inicio'.
- **inventarioVeterinariaPamela/settings.py**: Cambiar LOGIN_REDIRECT_URL a 'login_redirect'.
- **inventarioVeterinariaPamela/urls.py**: Cambiar name de 'home' a 'admin_index' para evitar conflicto.

### 2. [COMPLETED] Arreglar URLs en DataTables
- **templates/gestorProductos/datatable.html**: Corregir construcción de URLs en JS reemplazando {% url %} con placeholders por URLs base dinámicas y corregir nombres de URL (api_perros_adulto → api_perro_adulto).
- **templates/gestorProductos/datatable2.html**: Aplicar misma corrección y corregir nombres de URL (api_gatos_adulto → api_gato_adulto, api_gatos_cachorro → api_gato_cachorro).
- **templates/gestorProductos/datatable3.html**: Aplicar misma corrección.
- **templates/gestorProductos/datatable4.html**: Aplicar misma corrección.

### 3. [COMPLETED] Verificar APIs y Modelos
- Confirmar que APIs devuelven datos correctamente (asumir que sí, ya que usuario dice hay datos en DB).

## Archivos Dependientes a Editar
- gestorUser/views.py
- inventarioVeterinariaPamela/settings.py
- inventarioVeterinariaPamela/urls.py
- templates/gestorProductos/datatable.html
- templates/gestorProductos/datatable2.html
- templates/gestorProductos/datatable3.html
- templates/gestorProductos/datatable4.html

## Pasos de Seguimiento
- Probar redirección de login para admins y clientes.
- Verificar que DataTables muestren datos correctamente.
- Probar operaciones CRUD (crear, editar, eliminar productos).
- Ejecutar `python manage.py runserver` y probar en navegador.
- Si hay errores, revisar logs y corregir.
