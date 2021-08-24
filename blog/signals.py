from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_in, sender=User)
def user_login(sender,request,user,**kwargs):
    # user ko ip addr dikhane ke liye
    # print("---------")
    ip = request.META.get("REMOTE_ADDR")
    # print("ip:", ip)
    request.session['ip'] = ip
    ct = cache.get('count', 0, version=user.pk)
    ccount = ct+1
    cache.set('count', ccount, 60*60*24, version = user.pk)