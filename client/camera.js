// script.js

const cameraStream = document.getElementById('camera-stream');
const captureButton = document.getElementById('capture-button');
const retakeButton = document.getElementById('retake-button');
const submitButton = document.getElementById('submit-button');
const capturedImageCanvas = document.getElementById('captured-image');
const capturedImageContext = capturedImageCanvas.getContext('2d');

let isImageCaptured = false;

// Function to show a notification message
function showNotification(message, onOkay) {
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.textContent = message;

    const okayButton = document.createElement('button');
    okayButton.textContent = 'Okay';
    okayButton.addEventListener('click', () => {
        onOkay();
        document.body.removeChild(notification);
    });

    notification.appendChild(okayButton);
    document.body.appendChild(notification);
}

// Function to show retake and submit buttons
function showRetakeAndSubmitButtons() {
    retakeButton.style.display = 'block';
    submitButton.style.display = 'block';
}

// Get access to the camera stream
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraStream.srcObject = stream;
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
}

// Capture a picture from the camera stream
function capturePicture() {
    const { videoWidth, videoHeight } = cameraStream;
    capturedImageCanvas.width = videoWidth;
    capturedImageCanvas.height = videoHeight;
    capturedImageContext.drawImage(cameraStream, 0, 0, videoWidth, videoHeight);
    
    isImageCaptured = true;
    showRetakeAndSubmitButtons();

    // Hide the camera stream and display the captured image
    cameraStream.style.display = 'none';
    capturedImageCanvas.style.display = 'block';
}

// Function to retake the picture
function retakePicture() {
    isImageCaptured = false;
    capturedImageCanvas.style.display = 'none';
    cameraStream.style.display = 'block';
    hideRetakeAndSubmitButtons();
}

// Function to submit the picture
function submitPicture() {
    if (isImageCaptured) {
        // Here, you can use the captured image data or send it to the backend
        console.log('Image submitted');
    } else {
        console.log('No image to submit');
    }
}

function hideRetakeAndSubmitButtons() {
    captureButton.style.display = 'block';
    retakeButton.style.display = 'none';
    submitButton.style.display = 'none';
}

// Start the camera when the page loads
window.addEventListener('load', () => {
    showNotification('You will be taking a picture for verification.', startCamera);

    captureButton.addEventListener('click', capturePicture);
    retakeButton.addEventListener('click', retakePicture);
    submitButton.addEventListener('click', submitPicture);

    hideRetakeAndSubmitButtons();
});
