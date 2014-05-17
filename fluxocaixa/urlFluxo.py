from django.conf.urls import patterns, include, url

urlpatterns = patterns('FluxoCaixa.views',
    url(r'^$', 'listarFluxos'),
    url(r'^pesquisar/$', 'pesquisarFluxos'),
)