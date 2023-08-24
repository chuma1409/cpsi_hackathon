
function validateIdNumber(idNumber) {
    const idNumberPattern = /^\d{13}$/;
    return idNumberPattern.test(idNumber);
}

function showErrorModal(message) {
    const modal = document.getElementById('errorModal');
    const modalContent = modal.querySelector('.modal-content');
    modalContent.textContent = message;
    modal.style.display = 'flex';
}

function hideErrorModal() {
    const modal = document.getElementById('errorModal');
    modal.style.display = 'none';
}

function sendDataToBackend(data) {
    fetch('backend_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        console.log('Backend response:', responseData);
        // Perform actions based on the backend response
    })
    .catch(error => {
        console.error('Error sending data to backend:', error);
        // Handle the error
    });
}

function validateAndSave() {
    const selectedValue = document.querySelector('.dropdown').value;
    const idNumberInput = document.querySelector('.textbox');
    const idNumber = idNumberInput.value;

    if (!validateIdNumber(idNumber)) {
        showErrorModal('Please enter a valid 13-digit ID number.');
        idNumberInput.focus(); // Set focus to the input for correction
        return;
    }

    const dataToSend = {
        selectedValue: selectedValue,
        idNumber: idNumber
    };
    sendDataToBackend(dataToSend);
    // At this point, both the selected value and the ID number are valid
    // You can save the selected value and perform any other actions you need
    // For demonstration purposes, let's log them to the console
    console.log('Selected Value:', selectedValue);
    console.log('ID Number:', idNumber);
}

const nextButton = document.getElementById('nextButton');
nextButton.addEventListener('click', validateAndSave);
