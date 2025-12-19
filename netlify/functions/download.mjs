// TikGrab Video Download - Netlify Function
// Redirects to direct download URL (avoids 6MB limit)

export async function handler(event, context) {
    // Handle CORS preflight
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            body: '',
        };
    }

    // Only allow GET requests
    if (event.httpMethod !== 'GET') {
        return {
            statusCode: 405,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Method not allowed' }),
        };
    }

    // Get parameters
    const params = event.queryStringParameters || {};
    const videoUrl = params.url;
    const filename = params.filename || 'video.mp4';

    if (!videoUrl) {
        return {
            statusCode: 400,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({ error: 'Missing url parameter' }),
        };
    }

    try {
        // For large files, redirect directly to the video URL
        // This avoids the 6MB Netlify response limit
        return {
            statusCode: 302,
            headers: {
                'Location': videoUrl,
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache',
            },
            body: '',
        };
    } catch (error) {
        console.error('Download error:', error);
        return {
            statusCode: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({ error: error.message }),
        };
    }
}
