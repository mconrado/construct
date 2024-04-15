from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Categoria(models.Model):
    titulo =  models.CharField('titulo', max_length=40)
    created_at = models.DateTimeField('criado em', auto_now=True)
    
    class Meta: 
        verbose_name_plural = 'categorias'
        verbose_name = 'categoria'
        ordering = ('-created_at',)

    def __str__(self):
        return self.titulo   

class Produto(models.Model):
    nome =  models.CharField('produto', max_length=40, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True,verbose_name='categoria',)
    quantidade = models.FloatField('quantidade', )
    preco_compra = models.FloatField('preço de compra', )
    preco_venda = models.FloatField('preço de venda', )
    slug = models.SlugField(unique=True, blank=True, null=True)

    def gerar_desconto(self, desconto):
        #self.preco_venda - ((self.preco_venda * desconto)/100)
        return (self.preco_venda * (desconto-100))

    def lucro(self):
        lucro = self.preco_venda - self.preco_compra
        return (lucro * 100) / self.preco_compra

    class Meta: 
        verbose_name_plural = 'produtos'
        verbose_name = 'produto'
        ordering = ('-quantidade',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        return super().save(*args, **kwargs)


    def __str__(self):
        return self.nome   


class Imagem(models.Model):
    imagem = models.ImageField(upload_to="produtos")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    
    class Meta: 
        verbose_name_plural = 'imagens'
        verbose_name = 'imagem'
        ordering = ('-produto',)

    def __str__(self):
        return self.imagem   