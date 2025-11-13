const redis = require('redis');
const client = redis.createClient();

// Connect to Redis
client.on('connect', () => {
    console.log('Connected to Redis');
});

client.on('error', (err) => {
    console.error('Redis connection error:', err);
});

// Function to get cached URL
const getCachedUrl = (shortenedUrl) => {
    return new Promise((resolve, reject) => {
        client.get(shortenedUrl, (err, data) => {
            if (err) return reject(err);
            resolve(data);
        });
    });
};

// Function to set cached URL
const setCachedUrl = (shortenedUrl, originalUrl) => {
    client.set(shortenedUrl, originalUrl, 'EX', 3600); // Cache for 1 hour
};

module.exports = { getCachedUrl, setCachedUrl };
