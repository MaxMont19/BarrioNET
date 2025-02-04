from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models import Lote, Dias, Tarea, Quimico, Historial, Fundo, Usuario
from app.forms import LoteForm

main_bp = Blueprint('main', __name__)

# ================================
# 🔹 DASHBOARD: LISTA DE LOTES aa
# ================================

@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    lotes = Lote.query.order_by(Lote.fecha_poda.asc()).all()
    hoy = datetime.now().date()

    for lote in lotes:
        actualizar_estado_lote(lote.id)

    for lote in lotes:
        # 1️⃣ Verificar si hay tareas pendientes en una fecha programada atrasada
        tarea_atrasada = (
            Tarea.query
            .filter(Tarea.id_lote == lote.id, Tarea.estado != "Completado", Tarea.fecha_programada < hoy)
            .order_by(Tarea.fecha_programada.asc())
            .first()
        )

        if tarea_atrasada:
            # 🔴 Si hay tareas atrasadas, el lote sigue mostrando esa fecha programada hasta completarlas
            lote.estado = "Atrasado"
            lote.fecha_proxima_tarea = tarea_atrasada.fecha_programada
            lote.dias_restantes = "N/A"
            lote.quimicos_pendientes = Tarea.query.filter(Tarea.id_lote == lote.id, Tarea.fecha_programada == tarea_atrasada.fecha_programada, Tarea.estado != "Completado").count()
            continue

        # 2️⃣ Buscar la fecha programada más cercana que aún no ha pasado
        tarea_proxima = (
            Tarea.query
            .filter(Tarea.id_lote == lote.id, Tarea.fecha_programada >= hoy)
            .order_by(Tarea.fecha_programada.asc())
            .first()
        )

        if tarea_proxima:
            fecha_programada = tarea_proxima.fecha_programada
            tareas_de_esa_fecha = (
                Tarea.query
                .filter(Tarea.id_lote == lote.id, Tarea.fecha_programada == fecha_programada)
                .all()
            )
            tareas_completadas = all(t.estado == "Completado" for t in tareas_de_esa_fecha)

            # 🟢 Si todas las tareas están completas, esperar hasta que termine la fecha programada
            if tareas_completadas:
                if hoy >= fecha_programada:
                    estado_lote = "Completado"
                else:
                    estado_lote = "Completado"

            # 🟡 Si hay tareas pendientes → "Pendiente"
            else:
                estado_lote = "Pendiente"

            dias_restantes = max(0, (fecha_programada - hoy).days)
            quimicos_pendientes = len(tareas_de_esa_fecha)
        else:
            estado_lote = "Completado"
            dias_restantes = "N/A"
            quimicos_pendientes = 0

        lote.dias_restantes = dias_restantes
        lote.quimicos_pendientes = quimicos_pendientes
        lote.estado = estado_lote
        lote.fecha_proxima_tarea = fecha_programada if tarea_proxima else "N/A"

    return render_template('dashboard.html', lotes=lotes, hoy=hoy)

# ===================================
# 🔹 AGREGAR NUEVO LOTE
# ===================================
@main_bp.route('/agregar_lote', methods=['GET', 'POST'])
@login_required
def agregar_lote():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))

    form = LoteForm()
    if form.validate_on_submit():
        nuevo_lote = Lote(
            nombre=form.nombre.data,
            fundo_id=form.fundo.data,
            cultivo_id=form.cultivo.data,
            fecha_poda=form.fecha_poda.data
        )

        db.session.add(nuevo_lote)
        db.session.commit()

        calcular_fechas_programadas(nuevo_lote)

        flash('Lote agregado correctamente', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('agregar_lote.html', form=form)


# ================================
# 🔹 CALCULAR FECHAS PROGRAMADAS
# ================================

def calcular_fechas_programadas(lote):
    hoy = datetime.now().date()
    fecha_poda = lote.fecha_poda
    id_cultivo = lote.cultivo_id

    dias_fenologia = Dias.query.filter_by(id_cultivo=id_cultivo).all()

    for dia in dias_fenologia:
        fecha_programada = fecha_poda + timedelta(days=dia.dias)
        quimicos = Quimico.query.filter_by(id_dias=dia.id).all()

        for quimico in quimicos:
            estado_tarea = "Pendiente" if fecha_programada >= hoy else "Completado"

            nueva_tarea = Tarea(
                id_lote=lote.id,
                id_usuario=current_user.id,
                id_quimico=quimico.id,
                fecha_programada=fecha_programada,
                estado=estado_tarea,
                id_dias=dia.id
            )
            db.session.add(nueva_tarea)

    db.session.commit()


# ===================================
# 🔹 ACTUALIZAR ESTADO DEL LOTE
# ===================================

def actualizar_estado_lote(id_lote):
    hoy = datetime.now().date()
    lote = Lote.query.get(id_lote)

    if not lote:
        return

    # 1️⃣ Revisar si hay tareas pendientes en una fecha programada atrasada
    tarea_atrasada = (
        Tarea.query
        .filter(Tarea.id_lote == id_lote, Tarea.estado != "Completado", Tarea.fecha_programada < hoy)
        .order_by(Tarea.fecha_programada.asc())
        .first()
    )

    if tarea_atrasada:
        lote.estado = "Atrasado"
        lote.fecha_proxima_tarea = tarea_atrasada.fecha_programada
        db.session.commit()
        return

    # 2️⃣ Buscar la próxima fecha programada que aún no ha pasado
    tarea_proxima = (
        Tarea.query
        .filter(Tarea.id_lote == id_lote, Tarea.fecha_programada >= hoy)
        .order_by(Tarea.fecha_programada.asc())
        .first()
    )

    if not tarea_proxima:
        lote.estado = "Completado"
    else:
        fecha_actual = tarea_proxima.fecha_programada
        tareas_pendientes = Tarea.query.filter(Tarea.id_lote == id_lote, Tarea.fecha_programada == fecha_actual, Tarea.estado != "Completado").count()

        if tareas_pendientes == 0:
            if hoy >= fecha_actual:
                lote.estado = "Completado"
            else:
                lote.estado = "Pendiente"
        else:
            lote.estado = "Pendiente"

    db.session.commit()

# ===================================
# 🔹 COMPLETAR UNA TAREA
# ===================================


@main_bp.route('/completar_tarea/<int:tarea_id>', methods=['POST'])
@login_required
def completar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)

    if tarea.estado == "Completado":
        flash("Esta tarea ya ha sido completada.", "warning")
        return redirect(url_for('main.detalle_lote', id_lote=tarea.id_lote))

    # Actualizar la tarea con el usuario que la completó
    tarea.estado = "Completado"
    tarea.fecha_realizada = datetime.now().date()
    tarea.id_usuario = current_user.id  # Asigna el usuario actual

    # Guardar la tarea en el historial
    nueva_entrada = Historial(
        id_lote=tarea.id_lote,
        id_tarea=tarea.id,
        id_usuario=current_user.id,  # Guardar el usuario que completó la tarea
        id_quimico=tarea.id_quimico,
        observacion=request.form.get("observacion", "")
    )

    db.session.add(nueva_entrada)
    db.session.commit()

    flash("Tarea marcada como completada y registrada en el historial con el usuario correspondiente.", "success")
    return redirect(url_for('main.detalle_lote', id_lote=tarea.id_lote))


# ===================================
# 🔹 EDITAR LOTE
# ===================================

@main_bp.route('/editar_lote/<int:lote_id>', methods=['GET', 'POST'])
@login_required
def editar_lote(lote_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para editar lotes.', 'danger')
        return redirect(url_for('main.dashboard'))

    lote = Lote.query.get_or_404(lote_id)
    form = LoteForm(obj=lote)

    if form.validate_on_submit():
        lote.nombre = form.nombre.data
        lote.fundo = form.fundo.data
        lote.cultivo = form.cultivo.data
        lote.fecha_poda = form.fecha_poda.data
        db.session.commit()
        flash('Lote actualizado correctamente', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('editar_lote.html', form=form, lote=lote)

# ===================================
# 🔹 ELIMINAR LOTE
# ===================================

@main_bp.route('/eliminar_lote/<int:lote_id>', methods=['POST'])
@login_required
def eliminar_lote(lote_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para eliminar lotes.', 'danger')
        return redirect(url_for('main.dashboard'))

    lote = Lote.query.get_or_404(lote_id)
    db.session.delete(lote)
    db.session.commit()
    flash('Lote eliminado correctamente', 'success')
    return redirect(url_for('main.dashboard'))


# ===================================
# 🔹 DETALLE DEL LOTE
# ===================================

@main_bp.route('/detalle_lote/<int:id_lote>')
@login_required
def detalle_lote(id_lote):
    lote = Lote.query.get_or_404(id_lote)
    hoy = datetime.now().date()

    # 1️⃣ Buscar la fecha programada más antigua con tareas pendientes (si hay atrasadas)
    tarea_atrasada = (
        Tarea.query
        .filter(Tarea.id_lote == id_lote, Tarea.estado != "Completado", Tarea.fecha_programada < hoy)
        .order_by(Tarea.fecha_programada.asc())
        .first()
    )

    if tarea_atrasada:
        fecha_actual = tarea_atrasada.fecha_programada
    else:
        # 2️⃣ Si no hay tareas atrasadas, buscar la fecha programada más cercana que aún no ha pasado
        tarea_proxima = (
            Tarea.query
            .filter(Tarea.id_lote == id_lote, Tarea.fecha_programada >= hoy)
            .order_by(Tarea.fecha_programada.asc())
            .first()
        )
        fecha_actual = tarea_proxima.fecha_programada if tarea_proxima else None

    # Obtener las tareas de la fecha que corresponde (ya sea atrasada o la siguiente programada)
    tareas = (
        Tarea.query
        .filter(Tarea.id_lote == id_lote, Tarea.fecha_programada == fecha_actual)
        .order_by(Tarea.fecha_programada.asc())
        .all()
    ) if fecha_actual else []

    return render_template('vista_detalle_lote.html', lote=lote, tareas=tareas, hoy=hoy, fecha_actual=fecha_actual)


# ===================================
# 🔹 RUTA HOME -> REDIRECCIÓN A DASHBOARD
# ===================================
@main_bp.route('/')
@login_required
def home():
    return redirect(url_for('main.dashboard'))

# ===================================
# 🔹 RUTA HOME -> REDIRECCIÓN A HISTORIAL
# ===================================

@main_bp.route('/historial', methods=['GET'])
@login_required
def historial():
    lotes = Lote.query.order_by(Lote.nombre.asc()).all()
    return render_template('historial.html', lotes=lotes)

# ===================================
#  HISTORIAL DE CADA LOTE
# ===================================

@main_bp.route('/historial_lote/<int:id_lote>', methods=['GET'])
@login_required
def historial_lote(id_lote):
    lote = Lote.query.get_or_404(id_lote)

    historial = (
        db.session.query(
            Lote.nombre.label("nombre_lote"),
            Fundo.nombre.label("fundo"),
            Tarea.fecha_programada,
            Tarea.fecha_realizada,
            Usuario.username.label("usuario"),
            Quimico.fenologia,
            Quimico.nombre_comercial,
            Quimico.denominacion_ing_activo,
            Quimico.objetivo,
            Quimico.dosis_cilindro,
            Quimico.dosis_hectarea,
            Quimico.volumen,
            Historial.observacion
        )
        .join(Fundo, Fundo.id == Lote.fundo_id)
        .join(Tarea, Tarea.id_lote == Lote.id)
        .join(Usuario, Tarea.id_usuario == Usuario.id)
        .join(Quimico, Tarea.id_quimico == Quimico.id)
        .join(Historial, Historial.id_tarea == Tarea.id)
        .filter(Historial.id_lote == id_lote)
        .order_by(Tarea.fecha_programada.asc())  # 🔹 Ordenado por fecha programada
        .all()
    )

    return render_template('historial_lote.html', lote=lote, historial=historial)


# ===================================
#  DESCARGA EN EXCEL
# ===================================

import pandas as pd
from flask import send_file
import io

@main_bp.route('/descargar_historial/<int:id_lote>', methods=['GET'])
@login_required
def descargar_historial(id_lote):
    lote = Lote.query.get_or_404(id_lote)

    historial = (
        db.session.query(
            Lote.nombre.label("Nombre del Lote"),
            Fundo.nombre.label("Fundo"),
            Tarea.fecha_programada.label("Fecha Programada"),
            Tarea.fecha_realizada.label("Fecha Realizada"),
            Usuario.username.label("Usuario"),
            Quimico.fenologia.label("Fenología"),
            Quimico.nombre_comercial.label("Nombre Comercial"),
            Quimico.denominacion_ing_activo.label("Denominación Ing. Activo"),
            Quimico.objetivo.label("Objetivo"),
            Quimico.dosis_cilindro.label("Dosis x Cilindro"),
            Quimico.dosis_hectarea.label("Dosis x Hectárea"),
            Quimico.volumen.label("Volumen"),
            Historial.observacion.label("Observaciones")
        )
        .join(Fundo, Fundo.id == Lote.fundo_id)
        .join(Tarea, Tarea.id_lote == Lote.id)
        .join(Usuario, Tarea.id_usuario == Usuario.id)
        .join(Quimico, Tarea.id_quimico == Quimico.id)
        .join(Historial, Historial.id_tarea == Tarea.id)
        .filter(Historial.id_lote == id_lote)
        .order_by(Tarea.fecha_programada.asc())
        .all()
    )

    # Convertir a DataFrame
    df = pd.DataFrame(historial)

    # Usar BytesIO para evitar almacenar archivos en disco
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Historial")
    
    output.seek(0)

    # Enviar archivo como respuesta sin almacenarlo en el servidor
    return send_file(output, as_attachment=True, download_name=f"historial_lote_{lote.nombre}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ===================================
#  DESCARGA EN EXCEL DE TODOS LOS LOTES
# ===================================

@main_bp.route('/descargar_historial_todos', methods=['GET'])
@login_required
def descargar_historial_todos():
    historial = (
        db.session.query(
            Lote.nombre.label("Nombre del Lote"),
            Fundo.nombre.label("Fundo"),
            Tarea.fecha_programada.label("Fecha Programada"),
            Tarea.fecha_realizada.label("Fecha Realizada"),
            Usuario.username.label("Usuario"),
            Quimico.fenologia.label("Fenología"),
            Quimico.nombre_comercial.label("Nombre Comercial"),
            Quimico.denominacion_ing_activo.label("Denominación Ing. Activo"),
            Quimico.objetivo.label("Objetivo"),
            Quimico.dosis_cilindro.label("Dosis x Cilindro"),
            Quimico.dosis_hectarea.label("Dosis x Hectárea"),
            Quimico.volumen.label("Volumen"),
            Historial.observacion.label("Observaciones")
        )
        .join(Fundo, Fundo.id == Lote.fundo_id)
        .join(Tarea, Tarea.id_lote == Lote.id)
        .join(Usuario, Tarea.id_usuario == Usuario.id)
        .join(Quimico, Tarea.id_quimico == Quimico.id)
        .join(Historial, Historial.id_tarea == Tarea.id)
        .order_by(Tarea.fecha_programada.asc())  # 🔹 Ordenado por fecha programada
        .all()
    )

    df = pd.DataFrame(historial)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Historial")

    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name="historial_completo.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
