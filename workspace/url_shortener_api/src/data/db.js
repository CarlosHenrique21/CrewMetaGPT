const mongoose = require('mongoose');

// Define the URL schema
const urlSchema = new mongoose.Schema({
    originalUrl: { type: String, required: true },
    shortenedUrl: { type: String, required: true, unique: true },
    clicks: { type: Number, default: 0 },
    createdAt: { type: Date, default: Date.now }
});

// Create the URL model
const URL = mongoose.model('URL', urlSchema);

// Connect to MongoDB
const connectDB = async () => {
    try {
        await mongoose.connect('mongodb://localhost:27017/url_shortener', { useNewUrlParser: true, useUnifiedTopology: true });
        console.log('MongoDB connected');
    } catch (error) {
        console.error('MongoDB connection error:', error);
        process.exit(1);
    }};

module.exports = { connectDB, URL };