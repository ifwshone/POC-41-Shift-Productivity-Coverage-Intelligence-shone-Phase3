/** @type {import('next').NextConfig} */
const nextConfig = {
    eslint: {
      // Allows the production build to complete even with ESLint warnings
      ignoreDuringBuilds: true,
    },
    typescript: {
      // Allows the production build to complete even with TypeScript warnings
      ignoreBuildErrors: true,
    },
  };
  
  export default nextConfig;
  