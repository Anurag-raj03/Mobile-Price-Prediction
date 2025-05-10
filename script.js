async function predictPrice() {
    const form = document.getElementById('predictionForm');
    const data = new FormData(form);

    const mobileData = {
        brand: data.get('brand'),
        model: data.get('model'),
        rating: parseFloat(data.get('rating')),
        ram: parseFloat(data.get('ram')),
        rom: parseFloat(data.get('rom')),
        numBackCameras: parseInt(data.get('numBackCameras')),
        backCameraMP1: parseFloat(data.get('backCameraMP1')),
        backCameraMP2: parseFloat(data.get('backCameraMP2')) || 0,
        backCameraMP3: parseFloat(data.get('backCameraMP3')) || 0,
        backCameraMP4: parseFloat(data.get('backCameraMP4')) || 0,
        frontCameraMP: parseFloat(data.get('frontCameraMP')),
        frontSCameraMP: parseFloat(data.get('frontSCameraMP')) || 0,
        battery: parseInt(data.get('battery')),
        processorBrand: data.get('processorBrand'),
        processorName: data.get('processorName')
    };

    try {
        const response = await fetch('http://your-backend-url/predict', {  // Replace 'http://your-backend-url/predict' with your actual backend URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer your_api_key_here'  // Replace 'your_api_key_here' with your actual API key
            },
            body: JSON.stringify(mobileData)
        });
        
        const result = await response.json();
        document.getElementById('result').textContent = `Predicted Price: ₹${result.price.toFixed(2)}`;
    } catch (error) {
        document.getElementById('result').textContent = `Error: ${error.message}`;
    }
}
