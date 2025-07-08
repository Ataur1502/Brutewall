# core/views.py
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import IPAttempt
from django.utils.timezone import now
import csv
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate,ExtractHour
from django.db.models import Count
import json
from django.utils import timezone
from time import sleep

DELAY_THRESHOLDS = {3: 1, 5: 3, 8: 5}



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    ip = get_client_ip(request)
    ip_obj, _ = IPAttempt.objects.get_or_create(ip_address=ip)

    # ✅ Auto-unblock if time passed
    if ip_obj.blocked and ip_obj.blocked_until:
        if timezone.now() >= ip_obj.blocked_until:
            ip_obj.blocked = False
            ip_obj.attempts = 0
            ip_obj.blocked_until = None
            ip_obj.save()

    # ❌ Still blocked
    if ip_obj.blocked:
        messages.error(request, f"🚫 Your IP is temporarily blocked until {ip_obj.blocked_until.strftime('%H:%M:%S')}")
        return render(request, 'login.html')

    # ✅ Handle login POST
    if request.method == "POST":
        ip_obj.attempts += 1
        ip_obj.last_attempt = timezone.now()

        # 💤 Delay if threshold crossed
        delay = DELAY_THRESHOLDS.get(ip_obj.attempts)
        if delay:
            sleep(delay)

        # ⛔ Block if too many failures
        if ip_obj.attempts >= settings.BRUTE_BLOCK_THRESHOLD:
            ip_obj.blocked = True
            ip_obj.blocked_until = timezone.now() + timedelta(minutes=settings.BRUTE_BLOCK_DURATION_MINUTES)
            messages.error(request, "🚫 Too many failed attempts. You are now blocked temporarily.")
        else:
            messages.warning(request, f"❌ Login Failed (Simulated). Attempt #{ip_obj.attempts}")

        ip_obj.save()
        return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def dashboard(request):
    data = IPAttempt.objects.all()
    blocked_count = data.filter(blocked=True).count()
    active_count = data.filter(blocked=False).count()

    # Heatmap data: group by date + hour
    heatmap_raw = (
        IPAttempt.objects
        .annotate(date=TruncDate('last_attempt'), hour=ExtractHour('last_attempt'))
        .values('date', 'hour')
        .annotate(count=Count('id'))
        .order_by('date', 'hour')
    )

    # Format for chart.js matrix
    heatmap_data = []
    dates_set = sorted({entry['date'] for entry in heatmap_raw})
    date_index = {date: i for i, date in enumerate(dates_set)}

    for entry in heatmap_raw:
        heatmap_data.append({
            "x": entry["hour"],
            "y": date_index[entry["date"]],
            "v": entry["count"]
        })
   

    return render(request, 'dashboard.html', {
        'data': data,
        'blocked_count': blocked_count,
        'active_count': active_count,
        'attempt_labels': json.dumps([str(e['date']) for e in heatmap_raw]),
        'attempt_counts': json.dumps([e['count'] for e in heatmap_raw])
    })

def export_logs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ip_attempt_logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['IP Address', 'Attempts', 'Last Attempt', 'Blocked', 'Blocked Until'])

    for ip in IPAttempt.objects.all():
        writer.writerow([
            ip.ip_address,
            ip.attempts,
            ip.last_attempt.strftime('%Y-%m-%d %H:%M:%S'),
            'Yes' if ip.blocked else 'No',
            ip.blocked_until.strftime('%Y-%m-%d %H:%M:%S') if ip.blocked_until else '-'
        ])

    return response

def reset_ip(request, ip_address):
    ip = get_object_or_404(IPAttempt, ip_address=ip_address)
    ip.attempts = 0
    ip.blocked = False
    ip.blocked_until = None
    ip.save()
    messages.success(request, f"{ip_address} has been reset.")
    return redirect('dashboard')