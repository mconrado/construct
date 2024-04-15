from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Produto, Imagem
from django.urls import reverse
#Django Messages - definida lá no settings - MESSAGES_TAG
from django.contrib import messages
from django.contrib.messages import constants
from rolepermissions.decorators import has_permission_decorator

from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from .forms import ProdutoForm

# Create your views here.
@has_permission_decorator('cadastrar_produtos')

def adicionar_produto(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        categoria = request.GET.get('categoria')
        preco_min = request.GET.get('preco_min')
        preco_max = request.GET.get('preco_max')
        produtos = Produto.objects.all()

        if nome or categoria or preco_min or preco_max:
            
            if not preco_min:
                preco_min = 0

            if not preco_max:
                preco_max = 9999999

            if nome:
                produtos = produtos.filter(nome__icontains=nome)

            if categoria:
                produtos = produtos.filter(categoria=categoria)

            produtos = produtos.filter(preco_venda__gte=preco_min).filter(preco_venda__lte=preco_max)

        categorias = Categoria.objects.all()
        return render (request, 'adicionar_produto.html', {'categorias':categorias, 'produtos':produtos} )
    elif request.method == "POST":
        nome_produto = request.POST.get("nome_produto")
        categoria = request.POST.get("categoria")
        quantidade = request.POST.get("quantidade")
        preco_compra = request.POST.get("preco_compra")
        preco_venda = request.POST.get("preco_venda")
        lista_de_imagens = request.FILES.getlist("imagens")
        produto = Produto(nome=nome_produto,categoria_id=categoria, quantidade=quantidade, preco_compra=preco_compra, preco_venda=preco_venda )
        produto.save()

        for img_arquivo in lista_de_imagens:
            # if img.size > 500:
            #     mas pode ser definido via configuração do servidor de hospedagem
            #     return HTTPResponse("Tamanho da imagme deve ser menor que 200px") 
            nome_da_imagem = f'{date.today()}-{produto.id}.jpg'
            img = Image.open(img_arquivo)
            img = img.convert('RGB')
            img = img.resize((300,300))
            draw = ImageDraw.Draw(img)
            draw.text((20,280),f"GregMaster - Construct - {date.today()}", (255,255,255))
            output_imagem_draw = BytesIO()
            img.save(output_imagem_draw, format="JPEG", quality=100 )
            output_imagem_draw.seek(0)
            img_converte_in_memory_file = InMemoryUploadedFile(
                output_imagem_draw,
                "ImageField",
                nome_da_imagem,
                "image/jpeg",
                sys.getsizeof(output_imagem_draw),
                None
            )
            

            #imagem = Imagem(imagem=img_arquivo, produto=produto)
            imagem = Imagem(imagem=img_converte_in_memory_file, produto=produto)
            imagem.save()
        messages.add_message(request, constants.SUCCESS, 'Produto cadastrado com sucesso!')
        return redirect(reverse('adicionar_produto'))

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    messages.add_message(request, constants.ERROR, 'Produto excluído com sucesso!')
    return redirect(reverse('adicionar_produto')) # o reverse espera o name da url


def produto(request, slug):
    if request.method == "GET":
        produto = Produto.objects.get(slug=slug)
        data = produto.__dict__
        data['categoria'] = produto.categoria.id
        form = ProdutoForm(initial=data)
        return render(request, 'produto.html', {'form': form})