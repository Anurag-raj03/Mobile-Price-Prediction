const crypto = require('crypto');

// Function to generate API key
const generateApiKey = () => {
    return crypto.randomBytes(32).toString('hex');
};

// Generate the API key
const apiKey = generateApiKey();
console.log('Generated API Key:', apiKey);
