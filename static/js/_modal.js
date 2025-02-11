function openModal(actionForm, modalTitle, modalBody, closeButtonText, submitButtonText, submitButtonColor) {
    const modalForm = document.getElementById('modalForm');
    const modalMessage = document.getElementById('modalMessage');

    if (actionForm) {
        const modalTitleForm = document.getElementsByClassName('modal-title-form')[0];
        const modalBodyForm = document.getElementById('modalBodyForm');
        const btnCloseForm = document.getElementById('btnCloseForm');
        const btnSubmitForm = document.getElementById('btnSubmitForm');

        modalForm.action = actionForm;
        modalForm.style.display = 'block';
        modalMessage.style.display = 'none';
        modalTitleForm.innerHTML = modalTitle;
        modalBodyForm.innerHTML = modalBody;
        btnCloseForm.innerHTML = closeButtonText;
        btnSubmitForm.innerHTML = submitButtonText;
        btnSubmitForm.className = `btn btn-${submitButtonColor}`;
    } else {
        document.getElementById('staticBackdrop').removeAttribute('data-bs-backdrop');
        
        const modalTitleMessage = document.getElementsByClassName('modal-title-message')[0];
        const modalBodyMessage = document.getElementById('modalBodyMessage');
        const btnCloseMessage = document.getElementById('btnCloseMessage');
        
        modalForm.style.display = 'none';
        modalMessage.style.display = 'block';

        modalTitleMessage.innerHTML = modalTitle;
        modalBodyMessage.innerHTML = modalBody;
        btnCloseMessage.innerHTML = closeButtonText;

    }

    const modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));

    modal.show();
}