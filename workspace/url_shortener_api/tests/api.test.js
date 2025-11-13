const request = require('supertest');
const app = require('../src/app');
const { URL } = require('../src/data/db');

jest.mock('../src/data/db');

describe('API Endpoints', () => {
    test('POST /api/v1/shorten should create a new shortened URL', async () => {
        URL.prototype.save = jest.fn();
        const response = await request(app)
            .post('/api/v1/shorten')
            .send({ longUrl: 'http://example.com' });
        expect(response.statusCode).toBe(201);
        expect(response.body.shortenedUrl).toBeDefined();
    });

    test('GET /api/v1/urls should retrieve all shortened URLs', async () => {
        URL.find.mockResolvedValue([{ originalUrl: 'http://example.com', shortenedUrl: 'abc123' }]);
        const response = await request(app).get('/api/v1/urls');
        expect(response.statusCode).toBe(200);
        expect(response.body).toHaveLength(1);
    });

    test('GET /:shortenedUrl should redirect to the original URL', async () => {
        URL.findOne.mockResolvedValue({ originalUrl: 'http://example.com' });
        const response = await request(app).get('/abc123');
        expect(response.statusCode).toBe(302);
    });

    test('DELETE /api/v1/urls/:shortenedUrl should delete a shortened URL', async () => {
        URL.deleteOne.mockResolvedValue({ deletedCount: 1 });
        const response = await request(app).delete('/api/v1/urls/abc123');
        expect(response.statusCode).toBe(204);
    });
});
