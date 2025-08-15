from django.shortcuts import render, get_object_or_404
from .models import Activity, Session, Announcement
from .models import Session
from datetime import datetime, time, timedelta

def home(request):
    # portada: descripción + imagen + tablón de anuncios
    anuncios = Announcement.objects.all()[:10]
    return render(request, "core/home.html", {"anuncios": anuncios})

def actividades(request):
    crafts = Activity.objects.filter(category="crafts").prefetch_related("sessions")
    sports = Activity.objects.filter(category="sports").prefetch_related("sessions")
    return render(request, "core/actividades.html", {"crafts": crafts, "sports": sports})

def actividad_detalle(request, slug):
    actividad = get_object_or_404(Activity.objects.prefetch_related("sessions"), slug=slug)
    return render(request, "core/actividad_detalle.html", {"a": actividad})

def _floor_time_to_slot(t: time, minutes=30) -> time:
    # Redondea hacia abajo al múltiplo de "minutes"
    m = (t.minute // minutes) * minutes
    return time(t.hour, m)

def _ceil_time_to_slot(t: time, minutes=30) -> time:
    # Redondea hacia arriba al múltiplo de "minutes"
    total = t.hour * 60 + t.minute
    rem = total % minutes
    if rem == 0:
        return t
    total += (minutes - rem)
    return time(total // 60, total % 60)

def _time_slots(start: time, end: time, minutes=30):
    # Genera los bordes de slot [start, end) cada "minutes"
    cur = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    delta = timedelta(minutes=minutes)
    slots = []
    while cur < end_dt:
        slots.append(cur.time())  # inicio del slot
        cur += delta
    return slots  # p.ej. [09:00, 09:30, 10:00, ...]

def horarios(request):
    qs = (Session.objects
          .select_related("activity")
          .filter(is_active=True, day_of_week__lte=4)
          .order_by("day_of_week", "start_time"))

    day_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    if not qs.exists():
        slots = _time_slots(time(9, 0), time(14, 0), minutes=30)
        grid_rows = [{"label": f"{slots[i].strftime('%H:%M')}–{(datetime.combine(datetime.today(), slots[i]) + timedelta(minutes=30)).time().strftime('%H:%M')}",
                      "cells": [[] for _ in range(5)]}
                     for i in range(len(slots))]
        return render(request, "core/horarios.html", {"day_names": day_names, "grid_rows": grid_rows})

    min_start = min(s.start_time for s in qs)
    max_end = max(s.end_time for s in qs)
    start = _floor_time_to_slot(min_start, 30)
    end = _ceil_time_to_slot(max_end, 30)
    slots = _time_slots(start, end, 30)
    slot_index = {s: i for i, s in enumerate(slots)}

    # grid_rows: lista de filas [{label:str, cells:[ [sesiones...]*5 ]}]
    grid_rows = []
    for i, s in enumerate(slots):
        next_dt = (datetime.combine(datetime.today(), s) + timedelta(minutes=30)).time()
        label = f"{s.strftime('%H:%M')}–{next_dt.strftime('%H:%M')}"
        grid_rows.append({"label": label, "cells": [[] for _ in range(5)]})

    for ses in qs:
        s_start = _floor_time_to_slot(ses.start_time, 30)
        s_end = _ceil_time_to_slot(ses.end_time, 30)
        cur = datetime.combine(datetime.today(), s_start)
        end_dt = datetime.combine(datetime.today(), s_end)
        while cur < end_dt:
            idx = slot_index.get(cur.time())
            if idx is not None:
                grid_rows[idx]["cells"][ses.day_of_week].append(ses)
            cur += timedelta(minutes=30)

    return render(request, "core/horarios.html", {
        "day_names": day_names,
        "grid_rows": grid_rows,
    })

def contacto(request):
    # solo renderizar la página con el mapa + email
    return render(request, "core/contacto.html")
