from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf

class Perfil(models.Model):
    telefone = models.CharField(max_length=15, blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(max_length=9)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        error_messages = {}
        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()
        if perfil:
            cpf_salvo = perfil.cpf
            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já está cadastrado, efetue o login.'
        
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'
        
        # if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
        #     error_messages['cep'] = 'CEP inválido, digite os 8 digitos do CEP.'

        # Modificação na validação do CEP
        if re.match(r'^\d{5}-\d{3}$', self.cep) is None and re.match(r'^\d{8}$', self.cep) is None:
            error_messages['cep'] = 'CEP inválido.'
        
        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
