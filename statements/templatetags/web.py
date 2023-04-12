import datetime
from gettext import gettext

from django import template
from django.utils import timezone
from django.utils.html import conditional_escape, avoid_wrapping
from django.utils.safestring import mark_safe
from django.utils.timesince import TIME_STRINGS, timesince

register = template.Library()

CHUNKS = (
    (365, "year"),
    (30, "month"),
    (7, "week"),
    (1, "day"),
)


@register.filter
def dt(value, default=""):
    if not value:
        return default
    value = timezone.localtime(value)
    s = format(value, "%Y-%m-%d %H:%M")
    return mark_safe(f"<span title='{timesince(value)}'>{s}</span>")


@register.filter
def u(instance, title_attr="__str__", blank=True):
    esc = conditional_escape

    s = getattr(instance, title_attr)
    if callable(s):
        s = s()

    blank_attr = ' target="_blank" ' if blank else ""

    result = f'<a href="{esc(instance.get_absolute_url())}"{blank_attr}>{esc(s)}</a>'

    return mark_safe(result)


def many_days_since(since, time_strings):
    parts = []
    for i, (days, name) in enumerate(CHUNKS):
        count = since // days
        if count:
            parts.append(avoid_wrapping(f"{time_strings[name] % {'num': count} }"))
        since %= days
    return gettext(", ").join(parts)


def dayssince(d, now=None, reversed=False, time_strings=None, depth=2):
    """
    Take two date objects and return the time between d and now as a nicely
    formatted string, e.g. "3 weeks, 2 days".

    Units used are years, months, weeks, and days.

    `time_strings` is an optional dict of strings to replace the default
    TIME_STRINGS dict.

    Adapted from django.utils.timesince
    """
    if time_strings is None:
        time_strings = TIME_STRINGS

    # Convert datetime.datetime to datetime.date
    if isinstance(d, datetime.datetime):
        d = d.date()
    # if now and not isinstance(now, datetime.datetime):
    #     now = datetime.datetime(now.year, now.month, now.day)

    now = now or datetime.date.today()

    if reversed:
        d, now = now, d
    since = (now - d).days

    if since < -1:
        return avoid_wrapping(f"in {many_days_since(-since, time_strings)} days.")

    if since == -1:
        return "tomorrow"

    if since == 0:
        return "today"

    return many_days_since(since, time_strings) + "\xa0ago"


@register.filter("dayssince", is_safe=False)
def dayssince_filter(value, arg=None):
    """Format a date as the days since that date (i.e. "4 days, 6 hours")."""
    if not value:
        return ""
    try:
        if arg:
            return dayssince(value, arg)
        return dayssince(value)
    except (ValueError, TypeError):
        return ""
