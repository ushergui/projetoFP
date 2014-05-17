from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from pessoas.models import Pessoa
from caixas.models import Conta


def listarFluxos(request):
    pessoas = Pessoa.objects.all().order_by('nome')

    return render(request, 'fluxos/fluxoListar.html', {'pessoas': pessoas})

def pesquisarFluxos(request):
    if request.method == 'POST':
        pessoaBuscar = request.POST.get('pessoaBusca')
        dataBuscaInicio = datetime.strptime(request.POST.get('dataBuscaInicio', ''), '%d/%m/%Y')
        dataBuscaFim = datetime.strptime(request.POST.get('dataBuscaFinal', ''), '%d/%m/%Y')
        
        pessoas = Pessoa.objects.all().order_by('nome')

        totalreceber = 0
        totalpagar = 0
       
        try:
            sql = ("select cc.* from caixas_conta cc inner join pessoas_pessoa pp on pp.id = cc.pessoa_id where pp.id = '%s' and cc.data > '%s' and cc.data < '%s' ") % (pessoaBuscar, dataBuscaInicio, dataBuscaFim)
            contas = Conta.objects.raw(sql)

            for item in contas:
                if item.tipo == 'E':
                    totalreceber = totalreceber + item.valor
                else:
                    totalpagar = totalpagar + item.valor
        except:
            contas = [Conta(descricao='erro')]

        return render(request, 'fluxos/fluxoListar.html', {'contas': contas, 'pessoas': pessoas, 'totalreceber':totalreceber,'totalpagar':totalpagar})

