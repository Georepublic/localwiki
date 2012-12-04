import datetime
from itertools import groupby

from django.views.generic import ListView

from versionutils.versioning.constants import *

from pages.models import Page

from django.db.models import Max

import time

MAX_DAYS_BACK = 7

# select c.id, c.slug, h.history_date, h.history_id from pages_page c left outer join pages_page_hist h on c.id = h.id and h.history_id = (select max(h2.history_id) from pages_page_hist h2 where h2.id = h.id group by h2.id) order by h.history_date desc;

class ChangeListsView(ListView):
    template_name = "changelists/changelists.html"
    context_object_name = 'page_histories'
    
    def get_queryset(self):
        l = []
        lastmonth = datetime.datetime.now() - datetime.timedelta(days=30)
        histories = Page.versions.values('id').filter(history_date__gte = lastmonth).annotate(max_history_id = Max('history_id')).order_by('-id')
        histories = ValuesQuerySetToDict(histories)
        histories.sort(lambda x, y: y['max_history_id'] - x['max_history_id'])
        m = []
        for h in histories:
            n = Page.versions.get(history_id = h['max_history_id'])
            if not n.history_type == TYPE_DELETED:
                h['history_date'] = n.history_date
                m.append(h)
        for h in m:
            p = Page.objects.get(id = h['id'])
            l.append({'history_date': h['history_date'], 'page': p})
        def _the_day(o):
            date = o['history_date']
            return (date.year, date.month, date.day)
        ret = []
        for day, objs in groupby(l, _the_day):
            ret.append({'day': day, 'objs': ValuesQuerySetToDict(objs)})
        return ret

# http://djangosnippets.org/snippets/2454/
def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]
