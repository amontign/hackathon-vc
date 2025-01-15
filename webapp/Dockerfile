# Stage 1: Build the Next.js application
FROM node:18 AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application code
COPY . .

# Build the Next.js application
RUN npm run build

# Stage 2: Serve the application
FROM node:18

# Set working directory
WORKDIR /app

# Copy built application from the builder stage
COPY --from=builder /app ./

# Expose the port Next.js will run on
EXPOSE 3000

# Run the Next.js application
CMD ["npm", "run", "start"]
FROM node:18-alpine

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]