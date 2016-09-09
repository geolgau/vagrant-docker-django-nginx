from datetime import datetime

from django.shortcuts import render, redirect
from .models import Item
from redis import Redis
from django.template import Context, RequestContext

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

redis = Redis(host='redis', port=6379)

#@login_required
def home(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    counter = redis.incr('counter')
    return render(request,
                  'index.html',
                  context_instance = RequestContext(request,
                  {
                      'items': items,
                      'counter': counter,
                      'title':'Home Page',
                      'year':datetime.now().year,
                  })
            )

