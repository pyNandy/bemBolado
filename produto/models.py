from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from utils import utils
from django.utils.text import slugify
import os
from PIL import Image
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Produtos")
    descricao_curta = models.TextField(max_length=255, verbose_name='Descr.Produto')
    descricao_longa = models.TextField(verbose_name='Detalhes do Produto')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Preço Promo.')
    tipo = models.CharField(default='V', max_length=2, choices=(('V', 'Variável'), ('S', 'Simples'),))
    bordas = GenericRelation('Borda')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Pizzas'

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        if original_width <= new_width:
            img_pil.close()
            return
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(img_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
        super().save(*args, **kwargs)
        if self.imagem:
            self.resize_image(self.imagem, 800)

    def __str__(self):
        return self.nome


# Definindo a Variações 

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto')
    nome = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tamanho')
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1, verbose_name= 'Estoque')

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Pizzas - Variações'

# Formatando os valores preço

    def get_preco_variacao_formatado(self):
        return utils.formata_preco(self.preco)
    get_preco_variacao_formatado.short_description = 'Preço'

# Formatando os valores preço_promocional

    def get_preco_promocional_variacao_formatado(self):
        return utils.formata_preco(self.preco_promocional)
    get_preco_promocional_variacao_formatado.short_description = 'Preço Promocional'    



class Bebida(models.Model):
    nome_b = models.CharField(max_length=255, verbose_name="Tipo de Bebida")
    informacao_curta = models.TextField(max_length=255, verbose_name='Descr.Bebida', blank=True, null=True)
    informacao_longa = models.TextField(verbose_name='Detalhes da Bebida', blank=True, null=True)
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing_b = models.FloatField(verbose_name='Preço')
    preco_promocional_b = models.FloatField(
        default=0, verbose_name='Preço Promo.')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome_b)
        super().save(*args, **kwargs)

    def get_preco_bebida_formatado(self):
        return utils.formata_preco(self.preco_marketing_b)
    get_preco_bebida_formatado.short_description = 'Preço'

    def get_preco_promocional_bebida_formatado(self):
        return utils.formata_preco(self.preco_promocional_b)
    get_preco_promocional_bebida_formatado.short_description = 'Preço Promo.'

class VariacaoBebida(models.Model):
    produto_b = models.ForeignKey(Bebida, on_delete=models.CASCADE, verbose_name='Bebidas')
    nome_b = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tamanho')
    preco_marketing_b = models.FloatField()
    preco_promocional_b = models.FloatField(default=0)
    estoque_b = models.PositiveIntegerField(default=1, verbose_name= 'Estoque')

    def __str__(self):
        return self.nome_b or self.produto_b.nome_b

    class Meta:
        verbose_name = 'Variação de Bebida'
        verbose_name_plural = 'Variações de Bebidas'

    def get_preco_variacao_formatado(self):
        return utils.formata_preco(self.preco_marketing_b)
    get_preco_variacao_formatado.short_description = 'Preço'

    def get_preco_promocional_bebida_formatado(self):
        return utils.formata_preco(self.preco_promocional_b)
    get_preco_promocional_bebida_formatado.short_description = 'Preço Promo.'


####################### PIZZAS DOCES ###########################

class Produto_3(models.Model):
    nome_produto_3 = models.CharField(max_length=255, verbose_name="Produtos")
    descricao_venda_curta = models.TextField(max_length=255, verbose_name='Descr.Produto')
    descricao_venda_longa = models.TextField(verbose_name='Detalhes do Produto')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_de_venda = models.FloatField(verbose_name='Preço')
    preco_de_venda_promocional = models.FloatField(default=0, verbose_name='Preço Promo.')
    tipo = models.CharField(default='V', max_length=2, choices=(('V', 'Variável'), ('S', 'Simples'),))
    bordas = GenericRelation('Borda')

    class Meta:
        verbose_name = 'Produtos'
        verbose_name_plural = 'Pizzas Doces'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome_produto_3)
        super().save(*args, **kwargs)

    def get_preco_venda_formatado(self):
        return utils.formata_preco(self.preco_de_venda)
    get_preco_venda_formatado.short_description = 'Preço'

    def get_preco_venda_promocional_formatado(self):
        return utils.formata_preco(self.preco_de_venda_promocional)
    get_preco_venda_promocional_formatado.short_description = 'Preço Promo.'

    def __str__(self):
        return self.nome_produto_3

class Borda(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')
    nome = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tipo de Borda')
    preco = models.FloatField()

    def __str__(self):
        return self.nome or self.content_object.nome

    class Meta:
        verbose_name = 'Borda'
        verbose_name_plural = 'Pizzas - Tipo de Borda'

    def get_preco_borda_formatado(self):
        return utils.formata_preco(self.preco)
    get_preco_borda_formatado.short_description = 'Preço'

### Variacao_2 ------> Alteracao

class Alteracao(models.Model):
    produto = models.ForeignKey(Produto_3, on_delete=models.CASCADE, verbose_name='Pizzas Doces')
    nome_variacao = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tamanho')
    preco_venda = models.FloatField()
    preco_venda_promocional = models.FloatField(default=0)
    estoque_3 = models.PositiveIntegerField(default=1, verbose_name= 'Estoque')

    def __str__(self):
        return self.nome_variacao or self.produto_3.nome_produto_3

    class Meta:
        verbose_name = 'Variação 2'
        verbose_name_plural = 'Pizzas Doces - Variações'

# Formatando os valores de preço de venda

    def get_preco_variacao_venda_formatado(self):
        return utils.formata_preco(self.preco_venda)
    get_preco_variacao_venda_formatado.short_description = 'Preço'

# Formatando os valores de preço de venda promocional

    def get_preco_promocional_variacao_venda_formatado(self):
        return utils.formata_preco(self.preco_venda_promocional)
    get_preco_promocional_variacao_venda_formatado.short_description = 'Preço Promocional' 



#####FORMA DE PAGAMENTO

class Forma_Pagamento(models.Model):
    pagamento = models.CharField(max_length=50)
    valor_dinheiro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Campo adicional

    def __str__(self):
        return self.pagamento
