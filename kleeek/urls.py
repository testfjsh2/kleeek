from django.conf.urls import patterns, include, url
from django.contrib import admin
# from kleeek.views import set_vote
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kleeek.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', include('social_auth.urls')),
    url(r'^set_vote/', 'kleeek.kleeek.views.set_vote'),
    url(r'^spent_kleeek/', 'kleeek.kleeek.views.spent_kleeek'),
    url(r'^conver_kleeek/', 'kleeek.kleeek.views.conver_kleeek'),
    url(r'^get_user_total/', 'kleeek.kleeek.views.get_user_total'),
    url(r'^get_users_total/', 'kleeek.kleeek.views.get_users_total'),
    url(r'^get_room_list/', 'kleeek.kleeek.views.get_room_list'),
    url(r'^get_room/', 'kleeek.kleeek.views.get_room'),
    url(r'^sell_kleeek/', 'kleeek.kleeek.views.sell_kleeek'),
    url(r'^set_bonus/', 'kleeek.kleeek.views.set_bonus'),
    url(r'^set_day_bonus/', 'kleeek.kleeek.views.set_day_bonus'),
    url(r'^set_wall_post_bonus/', 'kleeek.kleeek.views.set_wall_post_bonus'),
    url(r'^set_friend_bonus/', 'kleeek.kleeek.views.set_friend_bonus'),
    # url(r'^close_rooms/', 'kleeek.kleeek.views.close_rooms'),
    # url(r'^kill_rooms/', 'kleeek.kleeek.views.kill_rooms'),
)
