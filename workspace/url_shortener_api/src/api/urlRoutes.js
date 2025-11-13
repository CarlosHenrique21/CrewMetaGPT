const express = require('express');
const urlService = require('../businessLogic/urlService');
const router = express.Router();

// POST: Create a new shortened URL
router.post('/shorten', async (req, res) => {
    try {
        const { longUrl, customAlias } = req.body;
        const result = await urlService.shortenUrl(longUrl, customAlias);
        res.status(201).json({ shortenedUrl: result });
    } catch (error) {
        console.error('Error shortening URL:', error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});

// GET: Retrieve a list of all shortened URLs
router.get('/urls', async (req, res) => {
    try {
        const urls = await urlService.getAllUrls();
        res.status(200).json(urls);
    } catch (error) {
        console.error('Error retrieving URLs:', error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});

// GET: Redirect to the original URL
router.get('/:shortenedUrl', async (req, res) => {
    try {
        const originalUrl = await urlService.redirectUrl(req.params.shortenedUrl);
        res.redirect(originalUrl);
    } catch (error) {
        console.error('Error redirecting to URL:', error);
        res.status(404).json({ message: 'URL not found' });
    }
});

// DELETE: Delete a shortened URL
router.delete('/urls/:shortenedUrl', async (req, res) => {
    try {
        await urlService.deleteUrl(req.params.shortenedUrl);
        res.status(204).send();
    } catch (error) {
        console.error('Error deleting URL:', error);
        res.status(404).json({ message: 'URL not found' });
    }
});

module.exports = router;