const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture');
const cameraImageInput = document.getElementById('camera_image');
const cameraForm = document.getElementById('cameraForm');

// Start camera only when user chooses "Capture"
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    });

captureBtn.addEventListener('click', () => {
    // Draw current frame to canvas
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas image to base64
    const dataUrl = canvas.toDataURL('image/png');

    // Put data into hidden input
    cameraImageInput.value = dataUrl;

    // Hide canvas preview to avoid image being shown
    canvas.style.display = 'none';

    // Submit the form
    cameraForm.submit();
});
