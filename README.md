# Multiple Disease Prediction System

A Streamlit web application that uses pre-trained machine-learning models to
provide predictions for:

- Diabetes
- Heart disease
- Parkinson's disease

The application runs as a single Streamlit service and loads the model and
scaler files from the repository's `saved models` directory.

> **Important:** This project is for educational and demonstration purposes.
> Its predictions are not medical diagnoses and must not replace advice from a
> qualified healthcare professional.

## Architecture Overview

```text
User
  |
  v
Internet / HTTPS
  |
  v
Nginx (optional reverse proxy on AWS EC2)
  |
  v
Streamlit application
  |
  +--> Diabetes model and scaler
  +--> Heart disease model and scaler
  `--> Parkinson's model and scaler
```

### Components

- **User interface:** Streamlit
- **Application:** Python
- **Machine learning:** scikit-learn
- **Model storage:** Serialized `.sav` files included in `saved models/`
- **Cloud hosting:** AWS EC2
- **Reverse proxy:** Nginx (recommended for production)
- **Process management:** systemd (recommended) or Docker
- **Object storage:** Not required by the current application

## Repository Structure

```text
.
├── Multiple Disease Prediction.py
├── requirements.txt
├── saved models/
│   ├── diabetes_model.sav
│   ├── diabetes_scaler.sav
│   ├── heartdisease_model.sav
│   ├── heartdisease_scaler.sav
│   ├── parkinsons_model.sav
│   └── parkinsons_scaler.sav
├── DiabetesPrediction_Folder/
├── HeartDiseasePrediction_Folder/
├── ParkinsonsDiseaseDetection_Folder/
└── .devcontainer/
```

The application requires both the model and scaler files. Preserve the
`saved models/` directory when copying or deploying the project.

## Requirements

- Python 3.11 recommended
- Git
- At least 1 GB of available memory for the application and dependencies

Python 3.11 is recommended because the dependency versions in
`requirements.txt` are tested against commonly supported Python versions.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd multiple-disease-prediction-main
```

### 2. Create and activate a virtual environment

On Linux or macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start Streamlit

```bash
streamlit run "Multiple Disease Prediction.py"
```

Open <http://localhost:8501> in a browser.

## Deploy to AWS EC2

The simplest AWS deployment is an Ubuntu EC2 instance running Streamlit.
This section describes a production-oriented setup using systemd and Nginx.

### 1. Launch the EC2 instance

In the AWS EC2 console:

1. Choose **Launch instance**.
2. Select **Ubuntu Server 22.04 LTS** or a later supported Ubuntu LTS release.
3. Select an instance with at least 1 GB RAM. A small instance is suitable for
   testing; choose a larger instance if multiple users will access the system.
4. Create or select an SSH key pair.
5. Configure the security group:
   - Allow SSH (`TCP 22`) only from your own IP address.
   - Allow HTTP (`TCP 80`) from the internet if using Nginx.
   - Allow HTTPS (`TCP 443`) from the internet after TLS is configured.
   - Do not expose Streamlit port `8501` publicly in the final deployment.

Record the instance's public IPv4 address or attach an Elastic IP address.

### 2. Connect through SSH

From a local terminal:

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 3. Install system packages

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3.11 python3.11-venv python3-pip nginx
```

Verify the installation:

```bash
python3.11 --version
nginx -v
```

### 4. Clone and install the application

```bash
cd /opt
sudo git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git multiple-disease-prediction
sudo chown -R ubuntu:ubuntu /opt/multiple-disease-prediction
cd /opt/multiple-disease-prediction

python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Test the application directly on the server:

```bash
streamlit run "Multiple Disease Prediction.py" \
  --server.address 127.0.0.1 \
  --server.port 8501
```

Press `Ctrl+C` after confirming that it starts successfully.

### 5. Create a systemd service

Create the service file:

```bash
sudo nano /etc/systemd/system/multiple-disease-prediction.service
```

Add:

```ini
[Unit]
Description=Multiple Disease Prediction Streamlit application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/multiple-disease-prediction
ExecStart=/opt/multiple-disease-prediction/.venv/bin/streamlit run "/opt/multiple-disease-prediction/Multiple Disease Prediction.py" --server.address 127.0.0.1 --server.port 8501
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable multiple-disease-prediction
sudo systemctl start multiple-disease-prediction
sudo systemctl status multiple-disease-prediction
```

View application logs:

```bash
sudo journalctl -u multiple-disease-prediction -f
```

### 6. Configure Nginx

Create an Nginx site configuration:

```bash
sudo nano /etc/nginx/sites-available/multiple-disease-prediction
```

Add:

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_EC2_IP;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Enable the site and validate the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/multiple-disease-prediction \
  /etc/nginx/sites-enabled/multiple-disease-prediction
sudo nginx -t
sudo systemctl reload nginx
```

The application should now be available at:

```text
http://YOUR_DOMAIN_OR_EC2_IP
```

If you do not have a domain yet, use the EC2 public IP for testing. For a
stable address, use an Elastic IP.

### 7. Add HTTPS with Let's Encrypt

For a domain pointing to the EC2 instance:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d YOUR_DOMAIN
```

Follow the prompts to enable HTTPS and automatic certificate renewal. Verify
renewal with:

```bash
sudo certbot renew --dry-run
```

## Updating the AWS Deployment

After pushing changes to GitHub:

```bash
cd /opt/multiple-disease-prediction
git pull origin main
source .venv/bin/activate
python -m pip install -r requirements.txt
sudo systemctl restart multiple-disease-prediction
sudo systemctl status multiple-disease-prediction
```

## Alternative: Docker Deployment

For a container-based deployment on AWS App Runner or ECS/Fargate, create a
`Dockerfile` with Python 3.11, install `requirements.txt`, and expose port
`8501`. The container command should be:

```bash
streamlit run "Multiple Disease Prediction.py" \
  --server.address 0.0.0.0 \
  --server.port 8501
```

The AWS service must route traffic to container port `8501`. Use a managed
container service when automatic scaling, rolling deployments, and reduced
server maintenance are required.

## Security and Operations

- Keep the EC2 security group restrictive, especially SSH port `22`.
- Use HTTPS before accepting public traffic.
- Never commit passwords, private keys, API keys, or `.streamlit/secrets.toml`.
- Keep model files and application code versioned together so their versions
  remain compatible.
- Create regular backups or use a versioned GitHub repository.
- Monitor systemd and Nginx logs.
- Restrict access to the application if it is only intended for demonstration
  or internal use.
- Treat user-entered health information as sensitive data. Do not add storage
  or logging of submitted health information without appropriate privacy and
  compliance controls.

## Troubleshooting

### The application cannot find a model file

Confirm that all six files exist in `saved models/`:

```bash
ls -la "saved models"
```

### The site is not reachable

Check each layer:

```bash
sudo systemctl status multiple-disease-prediction
sudo systemctl status nginx
sudo ss -ltnp | grep -E ':(80|8501)'
```

Also verify that the EC2 security group allows HTTP traffic on port `80`.

### Check Streamlit logs

```bash
sudo journalctl -u multiple-disease-prediction --no-pager -n 100
```

### Check Nginx logs

```bash
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

## License

No license is currently specified for this repository. Add a license file
before distributing the project or allowing others to reuse the source code.
