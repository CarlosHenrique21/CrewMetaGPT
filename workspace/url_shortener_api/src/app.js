const express = require('express');
const mongoose = require('mongoose');
const urlRoutes = require('./api/urlRoutes');
const app = express();

// Middleware to parse JSON requests
app.use(express.json());

// MongoDB Connection
mongoose.connect('mongodb://localhost:27017/url_shortener', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// API Routes
app.use('/api/v1', urlRoutes);

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
