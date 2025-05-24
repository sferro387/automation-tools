# automation-tools

This project contains two automation tools:
- **Email Sender:** Sends a weekly email every Friday with specific content.
- **Website Clocker:** Automates clocking hours on a website.

## Project Structure

```
src/
├── email_sender/
│   └── send_email.py
├── website_clocker/
│   └── clock_hours.py
├── common/
│   └── date_operations.py
├── main.py
```

## Prerequisites

- Python 3.8+
- `pip` for installing dependencies
- Docker (optional, for containerized runs)

## Setup

1. **Install dependencies:**
   ```sh
   pip3 install -r requirements.txt
   ```

2. **Prepare credentials:**
   - For the email sender, create a `credentials-test.json` file in the `src/` directory with your email and recipient info:
     ```json
     {
       "username": "your_email@example.com",
       "password": "your_password",
       "to": "recipient@example.com",
       "cc": [],
       "bcc": []
     }
     ```
   - For the website clocker, create a `credentials.json` file in `src/website_clocker/`:
     ```json
     {
       "url": "https://your-website.com/login",
       "username": "your_login_username",
       "password": "your_login_password"
     }
     ```

3. **Prepare email template:**
   - Place your HTML template at `src/email_templates/tripple_crown_weekly_stat.html`.

## Running the Tools

### Run with Python

From the `src/` directory, run:

```sh
python3 main.py
```

### How to Clock Hours

To run the website clocker directly:

1. Make sure your `credentials.json` is in `src/website_clocker/`.
2. From the `src/website_clocker/` directory, run:
   ```sh
   python3 clock_hours.py
   ```
   This will open a headless browser, log in, and fill in your hours as configured in the script.

### Run with Docker

Each tool has its own `Dockerfile` in its directory. To build and run, for example, the email sender:

```sh
cd src/email_sender
docker build -t email_sender .
docker run --rm -v "$(pwd)/../..:/app" email_sender
```

Do the same for `website_clocker` in its directory:

```sh
cd src/website_clocker
docker build -t website_clocker .
docker run --rm -v "$(pwd):/app" website_clocker
```

## Customization

- **Scheduling:** Use `cron` or a workflow orchestrator to schedule the script every Friday.
- **Browser Automation:** The website clocker may require Chrome/Firefox and Selenium or Playwright. See `website_clocker/clock_hours.py` for details.

## Troubleshooting

- Ensure all required files (`credentials-test.json`, `credentials.json`, email templates) are present.
- Check Python and Docker logs for errors.

---
