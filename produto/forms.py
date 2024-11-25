from django.forms.models import BaseInlineFormSet
from django import forms
from .models import Forma_Pagamento
import re

class VariacaoObrigatoria(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(VariacaoObrigatoria, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
    

class FormaPagamentoForm(forms.Form):
    forma_pagamento = forms.ModelChoiceField(
        queryset=Forma_Pagamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'onchange': 'toggleDinheiroField()'}),
        empty_label="Selecione uma forma de pagamento"
    )
    valor_pagamento = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'valor_pagamento', 'style': 'display:none;'})
    )

    def clean(self):
        cleaned_data = super().clean()
        forma_pagamento = cleaned_data.get("forma_pagamento")
        valor_pagamento = cleaned_data.get("valor_pagamento")

        # Verifica se a forma de pagamento é "Dinheiro" e se o valor em dinheiro foi fornecido
        if forma_pagamento and forma_pagamento.pagamento == 'Dinheiro':
            if not valor_pagamento:
                self.add_error('valor_pagamento', 'Este campo é obrigatório para pagamentos em dinheiro.')
            else:
                # Verifica se o valor está no formato correto (ex: 15,00 ou 25,15)
                pattern = re.compile(r'^\d+,\d{2}$')
                if not pattern.match(valor_pagamento):
                    self.add_error('valor_pagamento', 'Digite um valor válido em formato de moeda (ex: 15,00 ou 25,15).')
                else:
                    # Convertendo o valor para float para evitar erros no backend
                    try:
                        float(valor_pagamento.replace(',', '.'))
                    except ValueError:
                        self.add_error('valor_pagamento', 'Digite um valor válido em formato de moeda (ex: 15,00 ou 25,15).')

        return cleaned_data
