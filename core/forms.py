from django import forms
from .models import Produtos
from django.core.mail import EmailMessage


class ProdutosModelForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = ('nome', 'preco', 'estoque', 'imagem')


class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=50)
    email = forms.EmailField(label='Email')
    assunto = forms.CharField(label='Assunto', max_length=50)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-Mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject='E-Mail enviado pelo sistema django',
            body=conteudo,
            from_email='remetente@email.com',
            to=('enviadopara@email.com',),
            headers=f'Reply-To: {email}'
        )
        mail.send
