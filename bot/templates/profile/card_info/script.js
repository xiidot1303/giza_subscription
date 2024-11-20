let transactionId = ''; // Store the card token after the first API call

function toggleEditForm() {
    const editForm = document.getElementById('editForm');
    const editButton = document.getElementById('editButton');
    editForm.style.display = editForm.style.display === 'block' ? 'none' : 'block';
    editButton.style.display = editForm.style.display === 'block' ? 'none' : 'block';
}

function validateCardNumber() {
    const cardNumberInput = document.getElementById('newCardNumber');
    const continueButton = document.getElementById('continueButton');
    const cardNumberLength = cardNumberInput.value.replace(/\s/g, '').length;

    if (cardNumberLength === 16) {
        continueButton.classList.add('enabled');
        continueButton.disabled = false;
    } else {
        continueButton.classList.remove('enabled');
        continueButton.disabled = true;
    }
}

function formatExpiry() {
    const expiryInput = document.getElementById('newExpire');
    let value = expiryInput.value.replace(/\D/g, '');

    if (value.length > 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    expiryInput.value = value;
}

async function continueEditing() {
    const newCardNumber = document.getElementById('newCardNumber').value;
    const newExpire = document.getElementById('newExpire').value.replace("/", "");
    const apiHost = "{{ api_host }}";
    const response = await fetch(`${apiHost}cards/init`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            number: newCardNumber,
            expire: newExpire,
        }),
    });

    const data = await response.json();

    if (data.result.code == "OK") {
        transactionId = data.transaction_id;
        const phone = data.phone;
        document.getElementById('editForm').style.display = 'none';
        document.getElementById('verificationForm').style.display = 'block';
    } else {
        alert(data.result?.description);
    }
}

function validateSmsCode() {
    const smsCodeInput = document.getElementById('smsCode');
    const submitButton = document.getElementById('submitButton');
    const codeLength = smsCodeInput.value.length;

    if (codeLength === 6) {
        submitButton.classList.add('enabled');
        submitButton.disabled = false;
    } else {
        submitButton.classList.remove('enabled');
        submitButton.disabled = true;
    }
}

async function submitVerification() {
    const smsCode = document.getElementById('smsCode').value;
    const apiHost = "{{ api_host }}";

    const response = await fetch(`${apiHost}cards/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            transaction_id: transactionId,
            code: smsCode,
        }),
    });

    const data = await response.json();

    if (data.result.code == "OK") {
        const cardData = data.data
        const userId = "{{ user_id }}";

        await fetch(`${apiHost}/profile/update-card`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                card_data: cardData,
                user_id: userId
            }),
        });

        location.reload();
    } else {
        alert(data.result?.description);
    }
}
