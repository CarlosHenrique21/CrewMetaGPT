const URL = require('../data/db');
const shortid = require('shortid');

// Function to create a new shortened URL
const shortenUrl = async (longUrl, customAlias) => {
    const existingUrl = await URL.findOne({ originalUrl: longUrl });
    if (existingUrl) return existingUrl.shortenedUrl;

    const shortenedUrl = customAlias || shortid.generate();
    const urlRecord = new URL({ originalUrl: longUrl, shortenedUrl });
    await urlRecord.save();
    return shortenedUrl;
};

// Function to retrieve all shortened URLs
const getAllUrls = async () => {
    return await URL.find();
};

// Function to redirect to the original URL
const redirectUrl = async (shortenedUrl) => {
    const urlRecord = await URL.findOne({ shortenedUrl });
    if (!urlRecord) throw new Error('URL not found');
    return urlRecord.originalUrl;
};

// Function to delete a shortened URL
const deleteUrl = async (shortenedUrl) => {
    const result = await URL.deleteOne({ shortenedUrl });
    if (result.deletedCount === 0) throw new Error('URL not found');
};

module.exports = { shortenUrl, getAllUrls, redirectUrl, deleteUrl };
