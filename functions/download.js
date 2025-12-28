// TikGrab Video Download - Cloudflare Pages Function
// Redirects to direct download URL

export async function onRequest(context) {
    const { request } = context;
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response('', {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
        });
    }

    // Only allow GET requests
    if (request.method !== 'GET') {
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
            status: 405,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // Get parameters from URL
    const url = new URL(request.url);
    const videoUrl = url.searchParams.get('url');
    const filename = url.searchParams.get('filename') || 'video.mp4';

    if (!videoUrl) {
        return new Response(JSON.stringify({ error: 'Missing url parameter' }), {
            status: 400,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        });
    }

    try {
        // Redirect directly to the video URL
        return new Response(null, {
            status: 302,
            headers: {
                'Location': videoUrl,
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache',
            },
        });
    } catch (error) {
        console.error('Download error:', error);
        return new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        });
    }
}
