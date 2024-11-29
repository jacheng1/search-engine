/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
        {
            source: '/api/:path*',
            destination: 'http://localhost:5000/:path*', // Adjust port to match your Python server.
        },
        ];
    },
};
  
export default nextConfig;