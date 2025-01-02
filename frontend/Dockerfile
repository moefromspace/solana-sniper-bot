# Build Stage: Use Node.js to build the production-ready React application
FROM node:18-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files (package.json and yarn.lock) into the container
# This ensures only necessary files are copied for dependency installation
COPY package.json yarn.lock ./

# Install dependencies using Yarn with frozen-lockfile to ensure consistency
# RUN yarn install --frozen-lockfile
# During development we will use this
RUN yarn install

# Copy the application source code into the container
COPY ./src /app/src
COPY ./public /app/public

# Build the production-ready React application
RUN yarn build

# Production Stage: Use Nginx to serve the built static files
FROM nginx:1.23-alpine

# Add a non-root user for security purposes
# This user will run the application to minimize security risks
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory to the default Nginx HTML directory
WORKDIR /usr/share/nginx/html

# Copy the built files from the build stage into the Nginx HTML directory
COPY --from=build /app/build ./

# Change ownership of the Nginx HTML directory to the non-root user
RUN chown -R appuser:appgroup /usr/share/nginx/html

# Ensure necessary directories exist and are owned by Nginx
RUN mkdir -p /var/run/nginx /etc/nginx /usr/share/nginx && \
    chown -R nginx:nginx /var/run/nginx /etc/nginx /usr/share/nginx

# Expose port 80 to allow external access to the application
EXPOSE 80

# Start Nginx in the foreground to serve the application
CMD ["nginx", "-g", "daemon off;"]
