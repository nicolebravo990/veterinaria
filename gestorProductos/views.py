from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import (
    CategoriaRegistroForm, ProductosRegistroForm, PCProductosForm, PAProductosForm,
    PSProductosForm, AProductosForm, AGAProductosForm, AGCProductosForm,
    SnackGProductosForm, SnackPProductosForm, AntiparasitarioForm,
    MedicamentoForm, ShampooForm, CamaForm, CollarForm, JugueteForm,
    DatatableProductosForm, DatatableProductosPCForm, DatatableProductosPAForm,
    DatatableProductosPSForm, DatatableProductosAForm, DatatableAGAForm,
    DatatableAGCForm, DatatableSnackGForm, DatatableSnackPForm,
    DatatableAntiparasitarioForm, DatatableMedicamentoForm, DatatableShampooForm,
    DatatableCollarForm, DatatableCamaForm, DatatableJugueteForm
)
from .models import (
    Productos, Categoria, Carrito, PCProductos, PAProductos, PSProductos,
    AProductos, AGAProductos, AGCProductos, SnackGProductos, SnackPProductos,
    Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete
)
from gestorUser.forms import CitaMedicaForm
from gestorUser.models import CitaMedica

# Create your views here.

# ===========================
# VISTAS DE SESIÓN
# ===========================

@login_required
def vetInicio(request):
    productos = Productos.objects.all()[:20]

    # Get user's citas and appointment form
    citas_usuario = []
    formulario_cita = CitaMedicaForm()
    if request.user.is_authenticated:
        citas_usuario = CitaMedica.objects.filter(user=request.user).order_by('fecha', 'hora')
        
    return render(request,'gestorProductos/vetInicio.html',{
        'productos': productos,
        'formulario_cita': formulario_cita,
        'citas_usuario': citas_usuario,
    })

def logout_view(request):
    logout(request)  # Cierra la sesión
    messages.success(request, 'Has cerrado sesión correctamente.')

    # Redirige al login
    return redirect('login')  # Redirige a la página de inicio de sesión

# ===========================
# VISTAS DE DATATABLE
# ===========================
def datatable(request):
    productos = Productos.objects.all()
    data = {'productos':productos}
    return render(request,'gestorProductos/datatable.html', data)

def datatable2(request):
    pcproductos = PCProductos.objects.all()
    data = {'pcproductos':pcproductos}
    return render(request,'gestorProductos/datatable2.html', data)

def datatable3(request):
    paproductos = PAProductos.objects.all()
    data = {'paproductos':paproductos}
    return render(request,'gestorProductos/datatable3.html', data)

def datatable4(request):
    psproductos = PSProductos.objects.all()
    data = {'psproductos':psproductos}
    return render(request,'gestorProductos/datatable4.html', data)



# ===========================
# VISTAS DE PRODUCTOS PERROS
# ===========================
def ProductosPAData(request):
    paproductos = PAProductos.objects.all()
    data = {'paproductos':paproductos}
    return render(request,'gestorProductos/PAProductos.html', data)

def ProductosPCData(request):
    pcproductos = PCProductos.objects.all()
    data = {'pcproductos':pcproductos}
    return render(request,'gestorProductos/PCProductos.html', data)

def ProductosPSData(request):
    psproductos = PSProductos.objects.all()
    data = {'psproductos':psproductos}
    return render(request,'gestorProductos/PSProductos.html', data)

def ProductosAData(request):
    aproductos = AProductos.objects.all()
    data = {'aproductos':aproductos}
    return render(request,'gestorProductos/AProductos.html', data)

# ===========================
# VISTAS DE SOBRE NOSOTROS
# ===========================
def sobreData(request):
    """
    Vista para manejar la página 'Sobre Nosotros'.
    """
    contexto = {
        'titulo': 'Sobre Nosotros',
        'descripcion': 'Somos una veterinaria dedicada al cuidado y bienestar de tus mascotas. Con más de 10 años de experiencia, ofrecemos servicios personalizados, productos de calidad y atención médica profesional para asegurar la felicidad y salud de tus compañeros peludos.',
        'equipo': [
            {'nombre': 'Dr. Juan Pérez', 'rol': 'Veterinario Principal', 'descripcion': 'Especialista en pequeñas especies con 15 años de experiencia.'},
            {'nombre': 'Ana López', 'rol': 'Asistente Veterinaria', 'descripcion': 'Apasionada por el cuidado animal y experta en nutrición de mascotas.'},
            {'nombre': 'Carlos Martínez', 'rol': 'Gerente', 'descripcion': 'Encargado de la atención al cliente y gestión del negocio.'},
        ],
        'mision': 'Proporcionar atención de calidad para mejorar la vida de las mascotas y sus dueños.',
        'vision': 'Ser la veterinaria líder en nuestra comunidad, reconocida por el compromiso y excelencia en el cuidado de los animales.',
        'valores': ['Compromiso', 'Excelencia', 'Pasión por los animales', 'Empatía', 'Innovación']
    }
    return render(request, 'gestorProductos/sobreNosotros.html', contexto)

# ===========================
# VISTAS DE ALIMENTO PERRO
# ===========================
def alimentoPerroAData(request):
    paproductos = PAProductos.objects.all()[:20]
    return render(request, 'gestorProductos/alimentoPAdulto.html', {'paproductos': paproductos})

def alimentoPerroCData(request):
    pcproductos = PCProductos.objects.all()[:20]
    return render(request, 'gestorProductos/alimentoPCachorro.html', {'pcproductos': pcproductos})

def alimentoPerroSData(request):
    psproductos = PSProductos.objects.all()[:20]
    return render(request, 'gestorProductos/alimentoPSenior.html', {'psproductos': psproductos})

def antipulgasData(request):
    aproductos = AProductos.objects.all()[:20]
    return render(request, 'gestorProductos/antipulgas.html', {'aproductos': aproductos})

# ======================================
# VISTAS DE ELIMINAR Y EDITAR PRODUCTOS
# ======================================
def eliminarProducto(request, codigo):
    try:
        producto = Productos.objects.get(codigo=codigo)
        # Aquí va el código para eliminar el producto
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige a la lista de productos
    except Productos.DoesNotExist:
        messages.error(request, f"Producto con código {codigo} no encontrado.")
        return redirect('datatable')  # Redirige a una página donde se pueda ver el error


def editarProducto(request, id):
    # Busca el producto según el id
    producto = get_object_or_404(Productos, id=id)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            return redirect('datatable')  # Redirige a la lista de productos
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosForm(instance=producto)

    return render(request, 'gestorProductos/editarProducto.html', {'form': form, 'producto': producto})

# ============================================
# VISTAS DE ELIMINAR Y EDITAR PERRO CACHORRO
# ============================================
def eliminarProductoPC(request, id):
    try:
        pcproducto = PCProductos.objects.get(id=id)
        # Aquí va el código para eliminar el producto
        pcproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')  # Redirige a la lista de productos
    except PCProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable2')  # Redirige a una página donde se pueda ver el error



# ===========================================
# VISTAS DE ELIMINAR Y EDITAR PERRO ADULTO
# ===========================================
def eliminarProductoPA(request, codigo):
    try:
        paproducto = PAProductos.objects.get(codigo=codigo)
        paproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Ajusta con el nombre de tu vista de lista
    except PAProductos.DoesNotExist:
        messages.error(request, f"Producto con codigo {codigo} no encontrado.")
        return redirect('datatable')

# EDITAR PRODUCTO
def editarProductoPA(request, codigo):
    paproducto = get_object_or_404(PAProductos, codigo=codigo)

    if request.method == 'POST':
        form = DatatableProductosPAForm(request.POST, instance=paproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableProductosPAForm(instance=paproducto)

    return render(request, 'gestorProductos/editarProductoPA.html', {'form': form, 'paproducto': paproducto})

def editarProductoPC(request, codigo):
    # Busca el producto según el codigo
    pcproducto = get_object_or_404(PCProductos, codigo=codigo)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosPCForm(request.POST, instance=pcproducto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            return redirect('datatable2')  # Redirige a la lista de productos
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosPCForm(instance=pcproducto)

    return render(request, 'gestorProductos/editarProductoPC.html', {'form': form, 'pcproducto': pcproducto})

def editarProductoPS(request, codigo):
    # Busca el producto según el codigo
    psproducto = get_object_or_404(PSProductos, codigo=codigo)

    if request.method == 'POST':
        # Crea el formulario con datos enviados y la instancia del producto
        form = DatatableProductosPSForm(request.POST, instance=psproducto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el modelo
            return redirect('datatable4')  # Redirige a la lista de productos
    else:
        # Crea el formulario con la instancia del producto existente
        form = DatatableProductosPSForm(instance=psproducto)

    return render(request, 'gestorProductos/editarProductoPS.html', {'form': form, 'psproducto': psproducto})

# ==========================================
# VISTAS DE ELIMINAR Y EDITAR PERRO SENIOR
# ==========================================
def eliminarProductoPS(request, id):
    try:
        psproducto = PSProductos.objects.get(id=id)
        # Aquí va el código para eliminar el producto
        psproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')  # Redirige a la lista de productos
    except PSProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable')  # Redirige a una página donde se pueda ver el error



# ========================================
# VISTAS DE ELIMINAR Y EDITAR ANTIPULGAS
# ========================================
def eliminarProductoA(request, id):
    try:
        aproducto = AProductos.objects.get(id=id)
        aproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')
    except AProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable4')

def editarProductoA(request, codigo):
    aproducto = get_object_or_404(AProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableProductosAForm(request.POST, instance=aproducto)
        if form.is_valid():
            form.save()
            return redirect('datatable4')
    else:
        form = DatatableProductosAForm(instance=aproducto)

    return render(request, 'gestorProductos/editarProductoA.html', {'form': form, 'aproducto': aproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR GATO ADULTO
# ========================================
def eliminarProductoAGA(request, id):
    try:
        agaproducto = AGAProductos.objects.get(id=id)
        agaproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')
    except AGAProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable2')

def editarProductoAGA(request, codigo):
    agaproducto = get_object_or_404(AGAProductos, codigo=codigo)
    if request.method == 'POST':
        form = DatatableAGAForm(request.POST, instance=agaproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAGAForm(instance=agaproducto)
    return render(request, 'gestorProductos/editarProductoAGA.html', {'form': form, 'agaproducto': agaproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR GATO CACHORRO
# ========================================
def eliminarProductoAGC(request, id):
    try:
        agcproducto = AGCProductos.objects.get(id=id)
        agcproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')
    except AGCProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable2')

def editarProductoAGC(request, id):
    agcproducto = get_object_or_404(AGCProductos, id=id)
    if request.method == 'POST':
        form = DatatableAGCForm(request.POST, instance=agcproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAGCForm(instance=agcproducto)
    return render(request, 'gestorProductos/editarProductoAGC.html', {'form': form, 'agcproducto': agcproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SNACK GATO
# ========================================
def eliminarProductoSnackG(request, id):
    try:
        snackgproducto = SnackGProductos.objects.get(id=id)
        snackgproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable2')
    except SnackGProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable2')

def editarProductoSnackG(request, id):
    snackgproducto = get_object_or_404(SnackGProductos, id=id)
    if request.method == 'POST':
        form = DatatableSnackGForm(request.POST, instance=snackgproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable2')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableSnackGForm(instance=snackgproducto)
    return render(request, 'gestorProductos/editarProductoSnackG.html', {'form': form, 'snackgproducto': snackgproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SNACK PERRO
# ========================================
def eliminarProductoSnackP(request, id):
    try:
        snackpproducto = SnackPProductos.objects.get(id=id)
        snackpproducto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable')
    except SnackPProductos.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable')

def editarProductoSnackP(request, id):
    snackpproducto = get_object_or_404(SnackPProductos, id=id)
    if request.method == 'POST':
        form = DatatableSnackPForm(request.POST, instance=snackpproducto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableSnackPForm(instance=snackpproducto)
    return render(request, 'gestorProductos/editarProductoSnackP.html', {'form': form, 'snackpproducto': snackpproducto})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR ANTIPARASITARIO
# ========================================
def eliminarProductoAntiparasitario(request, id):
    try:
        antiparasitario = Antiparasitario.objects.get(id=id)
        antiparasitario.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')
    except Antiparasitario.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable3')

def editarProductoAntiparasitario(request, id):
    antiparasitario = get_object_or_404(Antiparasitario, id=id)
    if request.method == 'POST':
        form = DatatableAntiparasitarioForm(request.POST, instance=antiparasitario)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableAntiparasitarioForm(instance=antiparasitario)
    return render(request, 'gestorProductos/editarProductoAntiparasitario.html', {'form': form, 'antiparasitario': antiparasitario})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR MEDICAMENTO
# ========================================
def eliminarProductoMedicamento(request, id):
    try:
        medicamento = Medicamento.objects.get(id=id)
        medicamento.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')
    except Medicamento.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable3')

def editarProductoMedicamento(request, id):
    medicamento = get_object_or_404(Medicamento, id=id)
    if request.method == 'POST':
        form = DatatableMedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableMedicamentoForm(instance=medicamento)
    return render(request, 'gestorProductos/editarProductoMedicamento.html', {'form': form, 'medicamento': medicamento})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR SHAMPOO
# ========================================
def eliminarProductoShampoo(request, id):
    try:
        shampoo = Shampoo.objects.get(id=id)
        shampoo.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable3')
    except Shampoo.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable3')

def editarProductoShampoo(request, id):
    shampoo = get_object_or_404(Shampoo, id=id)
    if request.method == 'POST':
        form = DatatableShampooForm(request.POST, instance=shampoo)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable3')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableShampooForm(instance=shampoo)
    return render(request, 'gestorProductos/editarProductoShampoo.html', {'form': form, 'shampoo': shampoo})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR COLLAR
# ========================================
def eliminarProductoCollar(request, id):
    try:
        collar = Collar.objects.get(id=id)
        collar.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')
    except Collar.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable4')

def editarProductoCollar(request, id):
    collar = get_object_or_404(Collar, id=id)
    if request.method == 'POST':
        form = DatatableCollarForm(request.POST, instance=collar)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableCollarForm(instance=collar)
    return render(request, 'gestorProductos/editarProductoCollar.html', {'form': form, 'collar': collar})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR CAMA
# ========================================
def eliminarProductoCama(request, id):
    try:
        cama = Cama.objects.get(id=id)
        cama.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')
    except Cama.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable4')

def editarProductoCama(request, id):
    cama = get_object_or_404(Cama, id=id)
    if request.method == 'POST':
        form = DatatableCamaForm(request.POST, instance=cama)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableCamaForm(instance=cama)
    return render(request, 'gestorProductos/editarProductoCama.html', {'form': form, 'cama': cama})

# ========================================
# VISTAS DE ELIMINAR Y EDITAR JUGUETE
# ========================================
def eliminarProductoJuguete(request, id):
    try:
        juguete = Juguete.objects.get(id=id)
        juguete.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('datatable4')
    except Juguete.DoesNotExist:
        messages.error(request, f"Producto con id {id} no encontrado.")
        return redirect('datatable4')

def editarProductoJuguete(request, id):
    juguete = get_object_or_404(Juguete, id=id)
    if request.method == 'POST':
        form = DatatableJugueteForm(request.POST, instance=juguete)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('datatable4')
        else:
            messages.error(request, "Error al actualizar el producto.")
    else:
        form = DatatableJugueteForm(instance=juguete)
    return render(request, 'gestorProductos/editarProductoJuguete.html', {'form': form, 'juguete': juguete})

# ========================================
# REGISTRAR LOS DATOS EN FORMULARIOS
# ========================================
def crear_alimentopa(request):
    form = PAProductosForm()
    if request.method == "POST":
        form = PAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable?created=adulto')
        else:
            messages.error(request, "Error al crear el producto. Verifica los datos.")
    return render(request, 'gestorProductos/crearProductoPA.html', {'form': form})

def crear_alimentopc(request):
    form = PCProductosForm()
    if request.method == "POST":
        form = PCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2?created=cachorro')
    return render(request, 'gestorProductos/crearProductoPC.html', {'form': form})

def crear_alimentops(request):
    form = PSProductosForm()
    if request.method == "POST":
        form = PSProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable?created=senior')
    return render(request, 'gestorProductos/crearProductoPS.html', {'form': form})

def crear_snackp(request):
    form = SnackPProductosForm()
    if request.method == "POST":
        form = SnackPProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable?created=snacks')
    return render(request, 'gestorProductos/crearSnackPerro.html', {'form': form})

def crear_alimentoga(request):
    form = AGAProductosForm()
    if request.method == "POST":
        form = AGAProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2?created=gato_adulto')
    return render(request, 'gestorProductos/crearAlimentoGA.html', {'form': form})

def crear_alimentogc(request):
    form = AGCProductosForm()
    if request.method == "POST":
        form = AGCProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2?created=gato_cachorro')
    return render(request, 'gestorProductos/crearAlimentoGC.html', {'form': form})

def crear_snackg(request):
    form = SnackGProductosForm()
    if request.method == "POST":
        form = SnackGProductosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable2?created=snack_gato')
    return render(request, 'gestorProductos/crearSnackGato.html', {'form': form})

def crear_antiparasitario(request):
    form = AntiparasitarioForm()
    if request.method == "POST":
        form = AntiparasitarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable3?created=antiparasitario')
    return render(request, 'gestorProductos/crearAntiparasitario.html', {'form': form})

def crear_shampoo(request):
    form = ShampooForm()
    if request.method == "POST":
        form = ShampooForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable3?created=shampoo')
    return render(request, 'gestorProductos/crearshampoo.html', {'form': form})

def crear_medicamentos(request):
    form = MedicamentoForm()
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable3?created=medicamentos')
    return render(request, 'gestorProductos/crearMedicamentos.html', {'form': form})

def crear_collares(request):
    form = CollarForm()
    if request.method == "POST":
        form = CollarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('collares?created=collares')
    return render(request, 'gestorProductos/crearCollares.html', {'form': form})

def crear_camas(request):
    form = CamaForm()
    if request.method == "POST":
        form = CamaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('datatable4?created=camas')
    return render(request, 'gestorProductos/crearCamas.html', {'form': form})

def crear_juguetes(request):
    form = JugueteForm()
    if request.method == "POST":
        form = JugueteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('juguetes?created=juguetes')
    return render(request, 'gestorProductos/crearJuguetes.html', {'form': form})

def ProductoPCRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable2')  # Redirect to datatable2 for PCProductos
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearProductoPC.html', {'form': form})

def ProductoPARegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable')  # Keeps redirect to main datatable for PAProductos
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearProductoPA.html', {'form': form})

def ProductoPSRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable4')  # Redirect to datatable4 for PSProductos
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearProductoPS.html', {'form': form})

def AProductoRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable3')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearProductoA.html', {'form': form})

def SnackPerroRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearSnackPerro.html', {'form': form})

def AlimentoGARegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable2')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearAlimentoGA.html', {'form': form})

def AlimentoGCRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable2')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearAlimentoGC.html', {'form': form})

def SnackGatoRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable2')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearSnackGato.html', {'form': form})

def antiparasitarioRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable2')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearAntiparasitario.html', {'form': form})

def shampooRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable3')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearshampoo.html', {'form': form})

def medicamentosRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable3')  # Redirige al inicio de sesión
    else:
        form = ProductosRegistroForm()
    
    return render(request, 'gestorProductos/crearMedicamentos.html', {'form': form})

def camasRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable4')  # Redirige a la tabla de datos
    else:
        form = ProductosRegistroForm()

    return render(request, 'gestorProductos/crearCamas.html', {'form': form})

def collaresRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable4')
    else:
        form = ProductosRegistroForm()

    return render(request, 'gestorProductos/crearCollares.html', {'form': form})

def juguetesRegistro(request):
    form = ProductosRegistroForm()
    if request.method == "POST":
        form = ProductosRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable4')
    else:
        form = ProductosRegistroForm()

    return render(request, 'gestorProductos/crearJuguetes.html', {'form': form})

# ========================================

# ========================================
@login_required
def home(request):
    categorias = Categoria.objects.all()

    # KPIs para superusuarios
    if request.user.is_superuser:
        # Total productos
        total_productos = (
            Productos.objects.count() +
            PCProductos.objects.count() +
            PAProductos.objects.count() +
            PSProductos.objects.count() +
            AProductos.objects.count() +
            AGAProductos.objects.count() +
            AGCProductos.objects.count() +
            SnackGProductos.objects.count() +
            SnackPProductos.objects.count() +
            Antiparasitario.objects.count() +
            Medicamento.objects.count() +
            Shampoo.objects.count() +
            Cama.objects.count() +
            Collar.objects.count() +
            Juguete.objects.count()
        )

        # Total stock
        total_stock = (
            sum(Productos.objects.values_list('stock', flat=True)) +
            sum(PCProductos.objects.values_list('stock', flat=True)) +
            sum(PAProductos.objects.values_list('stock', flat=True)) +
            sum(PSProductos.objects.values_list('stock', flat=True)) +
            sum(AProductos.objects.values_list('stock', flat=True)) +
            sum(AGAProductos.objects.values_list('stock', flat=True)) +
            sum(AGCProductos.objects.values_list('stock', flat=True)) +
            sum(SnackGProductos.objects.values_list('stock', flat=True)) +
            sum(SnackPProductos.objects.values_list('stock', flat=True)) +
            sum(Antiparasitario.objects.values_list('stock', flat=True)) +
            sum(Medicamento.objects.values_list('stock', flat=True)) +
            sum(Shampoo.objects.values_list('stock', flat=True)) +
            sum(Cama.objects.values_list('stock', flat=True)) +
            sum(Collar.objects.values_list('stock', flat=True)) +
            sum(Juguete.objects.values_list('stock', flat=True))
        )

        # Valor inventario (suma precio * stock)
        valor_inventario = (
            sum(p.precio * p.stock for p in Productos.objects.all()) +
            sum(p.precio * p.stock for p in PCProductos.objects.all()) +
            sum(p.precio * p.stock for p in PAProductos.objects.all()) +
            sum(p.precio * p.stock for p in PSProductos.objects.all()) +
            sum(p.precio * p.stock for p in AProductos.objects.all()) +
            sum(p.precio * p.stock for p in AGAProductos.objects.all()) +
            sum(p.precio * p.stock for p in AGCProductos.objects.all()) +
            sum(p.precio * p.stock for p in SnackGProductos.objects.all()) +
            sum(p.precio * p.stock for p in SnackPProductos.objects.all()) +
            sum(p.precio * p.stock for p in Antiparasitario.objects.all()) +
            sum(p.precio * p.stock for p in Medicamento.objects.all()) +
            sum(p.precio * p.stock for p in Shampoo.objects.all()) +
            sum(p.precio * p.stock for p in Cama.objects.all()) +
            sum(p.precio * p.stock for p in Collar.objects.all()) +
            sum(p.precio * p.stock for p in Juguete.objects.all())
        )

        # Datos para gráficos
        categorias_count = {
            'Alimentos_Perro': PAProductos.objects.count() + PCProductos.objects.count() + PSProductos.objects.count(),
            'Alimentos_Gato': AGAProductos.objects.count() + AGCProductos.objects.count(),
            'Snacks': SnackPProductos.objects.count() + SnackGProductos.objects.count(),
            'Medicamentos': Antiparasitario.objects.count() + Medicamento.objects.count(),
            'Accesorios': Shampoo.objects.count() + Cama.objects.count() + Collar.objects.count() + Juguete.objects.count(),
            'Otros': Productos.objects.count() + AProductos.objects.count()
        }

        # Productos recientes (últimos 5 agregados)
        productos_recientes = []
        for model in [Productos, PCProductos, PAProductos, PSProductos, AProductos, AGAProductos, AGCProductos, SnackGProductos, SnackPProductos, Antiparasitario, Medicamento, Shampoo, Cama, Collar, Juguete]:
            productos_recientes.extend(list(model.objects.order_by('-id')[:5]))

        productos_recientes = sorted(productos_recientes, key=lambda x: x.id, reverse=True)[:5]

        context = {
            'categorias': categorias,
            'total_productos': total_productos,
            'total_stock': total_stock,
            'valor_inventario': valor_inventario,
            'categorias_count': categorias_count,
            'productos_recientes': productos_recientes
        }
    else:
        context = {'categorias': categorias}

    return render(request, 'index.html', context)

def guardar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')

        # Guardar en la base de datos
        Productos.objects.create(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria
        )
        return redirect('datatable4')  # Redirige a la página de éxito

# =================================
# VISTAS DE ALIMENTO Y SNACK GATO
# =================================
def alimentoGatoAData(request):
    agaproductos = AGAProductos.objects.all()[:20]
    return render(request, 'gestorProductos/alimentoGAdulto.html', {'agaproductos': agaproductos})

def alimentoGatoCData(request):
    agcproductos = AGCProductos.objects.all()
    return render(request, 'gestorProductos/alimentoGCachorro.html', {'agcproductos': agcproductos})

def Snack_gato(request):
    snackgproductos = SnackGProductos.objects.all()[:20]
    return render(request, 'gestorProductos/snackGato.html', {'snackgproductos': snackgproductos})

# ===========================
# VISTAS DE SNACK PERRO
# ===========================

def Snack_Perro(request):
    snackpproductos = SnackPProductos.objects.all()[:20]
    return render(request, 'gestorProductos/snackPerro.html', {'snackpproductos': snackpproductos})

# ===========================
# VISTAS DE OTROS PRODUCTOS
# ===========================
def medicamentos(request):
    medicamento = Medicamento.objects.all()[:20]
    return render(request, 'gestorProductos/medicamentos.html', {'medicamento': medicamento})

def antiparasitarios(request):
    antiparasitario = Antiparasitario.objects.all()[:20]
    return render(request, 'gestorProductos/antiparasitario.html', {'antiparasitario': antiparasitario})


def shampoos(request):
    shampoo = Shampoo.objects.all()[:20]
    return render(request, 'gestorProductos/shampoo.html', {'shampoo': shampoo})

def camas(request):
    cama = Cama.objects.all()[:20]
    return render(request, 'gestorProductos/camas.html', {'cama': cama})

def collares(request):
    collar = Collar.objects.all()[:20]
    return render(request, 'gestorProductos/collares.html', {'collar': collar})

def juguetes(request):
    juguete = Juguete.objects.all()[:20]
    return render(request, 'gestorProductos/juguetes.html', {'juguete': juguete})

# ===========================
# VISTAS DEL CARRITO
# ===========================

# --- VER CARRITO ---
def ver_carrito(request):
    if request.GET.get("clear") == "1":
        if "carrito" in request.session:
            del request.session["carrito"]
            request.session.modified = True
            messages.success(request, "Carrito vaciado correctamente.")
        return redirect("ver_carrito")

    carrito = request.session.get("carrito", {})
    total = sum(item["subtotal"] for item in carrito.values())

    # Guardar la URL anterior si no viene del propio carrito
    url_anterior = request.META.get("HTTP_REFERER")

    if url_anterior and "carrito" not in url_anterior:
        request.session["ultima_url"] = url_anterior

    return render(request, "gestorProductos/verCarrito.html", {
        "carrito": carrito,
        "total": total,
        "volver": request.session.get("ultima_url", "/")
    })


# --- AGREGAR AL CARRITO ---

def agregar_carrito(request, tipo, producto_id):
    """
    Añade un producto al carrito guardado en session.
    URL: carrito/agregar/<str:tipo>/<int:producto_id>/
    Se espera un POST con campo 'cantidad'. Si no es POST, redirige atrás.
    """
    # Solo aceptar POST para añadir
    if request.method != "POST":
        # si fue GET, simplemente redirigimos a la página anterior
        referer = request.META.get("HTTP_REFERER") or '/'
        return redirect(referer)

    # Mapeo de tipos (ajusta claves si usas otras abreviaciones)
    modelos = {
        "pa": PAProductos,
        "pc": PCProductos,
        "ps": PSProductos,
        "a": AProductos,
        "p": Productos,
        "ap": Antiparasitario,
        # si en tu HTML usas otras strings, añádelas aquí (ej. "perro_adulto": PAProductos)
    }

    modelo = modelos.get(tipo)
    if not modelo:
        messages.error(request, "Tipo de producto inválido.")
        # preferible volver a la página previa
        return redirect(request.META.get("HTTP_REFERER", "/"))

    producto = get_object_or_404(modelo, id=producto_id)

    # obtener cantidad del POST (validar)
    try:
        cantidad = int(request.POST.get("cantidad", 1))
        if cantidad < 1:
            cantidad = 1
    except (ValueError, TypeError):
        cantidad = 1

    # session cart
    carrito = request.session.get("carrito", {})

    # usar una key que incluya tipo para evitar colisiones entre modelos
    key = f"{tipo}_{producto.id}"

    precio_unit = float(producto.precio) if producto.precio is not None else 0.0

    if key not in carrito:
        carrito[key] = {
            "tipo": tipo,
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": precio_unit,
            "cantidad": cantidad,
            "subtotal": round(precio_unit * cantidad, 2),
            # opcional: agregar imagen url si quieres mostrarlo en carrito
            "imagen": getattr(producto, "imagen").url if getattr(producto, "imagen", None) else "",
        }
    else:
        # sumar cantidad
        carrito[key]["cantidad"] += cantidad
        carrito[key]["subtotal"] = round(carrito[key]["cantidad"] * carrito[key]["precio"], 2)

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, f"Se agregó {cantidad} x {producto.nombre} al carrito.")

    # Intentamos volver a la página anterior; si no existe, ir a inicio
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect("vet_inicio")

# --- ACTUALIZAR CANTIDADES ---
def actualizar_carrito(request):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})

        for key in carrito.keys():
            nueva_cantidad = int(request.POST.get(f"cantidad_{key}", 1))
            carrito[key]["cantidad"] = nueva_cantidad
            carrito[key]["subtotal"] = nueva_cantidad * carrito[key]["precio"]

        request.session["carrito"] = carrito

    return redirect("ver_carrito")

# --- ELIMINAR PRODUCTO ---

def eliminar_carrito(request, tipo, producto_id):
    carrito = request.session.get("carrito", {})
    key = f"{tipo}_{producto_id}"

    if key in carrito:
        del carrito[key]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado correctamente del carrito.")
    else:
        messages.error(request, "Producto no encontrado en el carrito.")

    return redirect("ver_carrito")


# ===========================
# APIS
# ===========================
def api_perros_adulto(request):
    productos = PAProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_cachorro(request):
    productos = PCProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_senior(request):
    productos = PSProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_perros_snacks(request):
    productos = SnackPProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_adulto(request):
    productos = AGAProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_cachorro(request):
    productos = AGCProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_gatos_snacks(request):
    productos = SnackGProductos.objects.filter()
    data = list(productos.values())
    return JsonResponse({"data": data})

def api_antiparasitario(request):
    productos = Antiparasitario.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_shampoo(request):
    productos = Shampoo.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_medicamento(request):
    productos = Medicamento.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_collares(request):
    productos = Collar.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_camas(request):
    productos = Cama.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_juguetes(request):
    productos = Juguete.objects.filter()
    return JsonResponse({"data": list(productos.values())})

def api_aproductos(request):
    productos = AProductos.objects.filter()
    return JsonResponse({"data": list(productos.values())})

# Endpoint para agregar producto (POST) — usa csrftoken desde JS (recomendado)
@require_http_methods(["POST"])
def agregar_producto(request):
    # si usas fetch/ajax con csrftoken esto funcionará
    nombre = request.POST.get('nombre')
    descripcion = request.POST.get('descripcion')
    precio = request.POST.get('precio')
    stock = request.POST.get('stock')
    categoria = request.POST.get('categoria')

    if not all([nombre, descripcion, precio, stock, categoria]):
        return HttpResponseBadRequest("Faltan campos")

    p = Productos.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        categoria=categoria
    )
    return JsonResponse({'ok': True, 'id': p.pk})








