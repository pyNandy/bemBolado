document.addEventListener('DOMContentLoaded', (event) => {
    const telefoneInput = document.getElementById('telefone');

    telefoneInput.addEventListener('input', (event) => {
        let telefone = event.target.value.replace(/\D/g, '');
        telefone = telefone.replace(/^(\d{2})(\d)/g, '($1)$2');
        telefone = telefone.replace(/(\d)(\d{4})$/, '$1-$2');
        event.target.value = telefone;
    });
});
