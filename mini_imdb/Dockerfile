# Use a modern Python image
FROM docker.arvancloud.ir/python

# Print everything straight to terminal
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /backend

# Copy dependencies file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django app
COPY . .

# Open port 8000
EXPOSE 8000

# Run Django's dev server for beginners
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
