FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# run app.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "application:app"]

# # Build the image
# docker build -t cloud-clicker-app .

# # Run the image and delete the container when it exits
# docker run --rm -p 4000:80 cloud-clicker-app

# # Test the app
# curl http://localhost:4000