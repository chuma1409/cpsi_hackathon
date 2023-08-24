// script.js

const medicalRecordForm = document.getElementById('medical-record-form');
const previousButton = document.getElementById('previous-button');
const nextButton = document.getElementById('next-button');
const patientRecord = document.getElementById('patient-record');
let currentPatientIndex = 0;

// Sample patient data with records
const patients = [
    {
        name: 'John Doe',
        id: '12345',
        dateOfBirth: '1990-01-01',
        gender: 'Male',
        records: [
            { date: '2023-09-01', content: 'Initial checkup.' }
        ]
    },
    {
        name: 'Jane Smith',
        id: '67890',
        dateOfBirth: '1985-05-15',
        gender: 'Female',
        records: [
            { date: '2023-08-15', content: 'Prescribed medication for flu.' },
            { date: '2023-07-20', content: 'Annual checkup.' }
        ]
    }
    // Add more patients as needed
];

function displayPatientRecord(index) {
    const patient = patients[index];
    let recordsHtml = '';
    patient.records.forEach(record => {
        recordsHtml += `
            <p><strong>Date:</strong> ${record.date}</p>
            <p><strong>Record:</strong> ${record.content}</p>
        `;
    });
    
    patientRecord.innerHTML = `
        <h3>Patient Record</h3>
        <p><strong>Patient ID:</strong> ${patient.id}</p>
        <p><strong>Date of Birth:</strong> ${patient.dateOfBirth}</p>
        <p><strong>Gender:</strong> ${patient.gender}</p>
        <h4>Records:</h4>
        ${recordsHtml}
    `;
}

function navigateToPatient(index) {
    if (index >= 0 && index < patients.length) {
        currentPatientIndex = index;
        displayPatientRecord(currentPatientIndex);
    }
}

medicalRecordForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const newRecord = document.getElementById('new-record').value;
    patients[currentPatientIndex].records.push({
        date: new Date().toISOString().split('T')[0],
        content: newRecord
    });
    
    displayPatientRecord(currentPatientIndex);
    medicalRecordForm.reset();
});

previousButton.addEventListener('click', () => {
    navigateToPatient(currentPatientIndex - 1);
});

nextButton.addEventListener('click', () => {
    navigateToPatient(currentPatientIndex + 1);
});

// Display the initial patient record
displayPatientRecord(currentPatientIndex);
