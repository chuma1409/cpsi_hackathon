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
    fetch('http://localhost:8000/get_user_by_id/' + data.idNumber)
        .then(response => response.json())
        .then(responseData => {
            if (responseData.id_number && responseData.name && responseData.last_name) {
                // Store the ID number in sessionStorage
                sessionStorage.setItem('idNumber', data.idNumber);

                // Redirect to verify.html
                window.location.href = 'verify.html';
            } else {
                showErrorModal('Patient not found. Please check the ID number.');
                // Perform actions based on the backend response
            }
        })
        .catch(error => {
            console.error('Error fetching data from backend:', error);
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
