# Use the Node.js 18 Alpine image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first
# This ensures caching if dependencies haven't changed
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY frontend/ ./

# Build the application
RUN npm run build

# Command to run the development server
CMD ["npm", "run", "dev"]
