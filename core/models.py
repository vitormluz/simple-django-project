from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from stdimage import StdImageField


class Produtos(models.Model):
    nome = models.CharField('Produto', max_length=50)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=15)
    estoque = models.BooleanField('Estoque', default=True)
    imagem = StdImageField('Imagem', upload_to='produtos_images', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)
    descricao = models.CharField('Descrição', max_length=350)

    def __str__(self):
        return self.nome


def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

signals.pre_save.connect(produto_pre_save, sender=Produtos)