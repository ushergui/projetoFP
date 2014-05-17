from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime
from pessoas.models import Pessoa
from caixas.models import Conta


def listarFluxos(request):
    pessoas = Pessoa.objects.all().order_by('nome')

    return render(request, 'fluxos/fluxosListar.html', {'pessoas': pessoas})

def pesquisarFluxos(request):
    if request.method == 'POST':
        pessoaBuscar = request.POST.get('pessoaBuscar')
        dataBuscaInicio = datetime.strptime(request.POST.get('dataBuscaInicio', ''), '%d/%m/%Y')
        dataBuscaFim = datetime.strptime(request.POST.get('dataBuscaFinal', ''), '%d/%m/%Y')
        
        nome = Pessoa.objects.filter(id=pessoaBuscar)
        pessoas = Pessoa.objects.all().order_by('nome')

        totalreceber = 0
        totalpagar = 0
       
        try:
            sql = "select * from caixas_conta where pessoa_id like %s and data >= '%s' and data <= '%s'" % (pessoaBuscar, dataBuscaInicio, dataBuscaFim)
            contas = Conta.objects.raw(sql)

            for item in contas:
                if item.tipo == 'E':
                    totalreceber = totalreceber + item.valor
                else:
                    totalpagar = totalpagar + item.valor
        except:
            contas = [Conta(descricao='erro')]

        return render(request, 'fluxos/fluxoListar.html', {'contas': contas, 'nome':nome, 'pessoas': pessoas, 'totalreceber':totalreceber,'totalpagar':totalpagar})

