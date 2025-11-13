const { shortenUrl, getAllUrls, redirectUrl, deleteUrl } = require('../src/businessLogic/urlService');
const { URL } = require('../src/data/db');

// Mock MongoDB
jest.mock('../src/data/db');

describe('URL Service', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should shorten a URL', async () => {
        URL.prototype.save = jest.fn();
        const longUrl = 'http://example.com';
        const result = await shortenUrl(longUrl);
        expect(result).toBeDefined();
    });

    test('should retrieve all URLs', async () => {
        URL.find.mockResolvedValue([{ originalUrl: 'http://example.com', shortenedUrl: 'abc123' }]);
        const urls = await getAllUrls();
        expect(urls).toHaveLength(1);
    });

    test('should redirect to original URL', async () => {
        URL.findOne.mockResolvedValue({ originalUrl: 'http://example.com' });
        const originalUrl = await redirectUrl('abc123');
        expect(originalUrl).toBe('http://example.com');
    });

    test('should delete a shortened URL', async () => {
        URL.deleteOne.mockResolvedValue({ deletedCount: 1 });
        await deleteUrl('abc123');
        expect(URL.deleteOne).toHaveBeenCalledWith({ shortenedUrl: 'abc123' });
    });
});
