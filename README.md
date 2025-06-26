# LinkedIn Auto Like & Comment Bot

This project automates the process of liking and commenting on LinkedIn posts using Selenium and OpenAI. The bot logs into LinkedIn, reads post URLs from a CSV file, generates context-aware comments using OpenAI, and interacts with each post.

## Features
- Automatic login to LinkedIn
- Likes and comments on a list of LinkedIn post URLs
- Generates professional, engaging comments using OpenAI
- Robust error handling and logging

## Requirements
- Python 3.13.x
- Google Chrome browser
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd linkedin
   ```

2. **Install dependencies with Poetry:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with the following content:
   ```env
   LINKEDIN_USERNAME=your_email_or_username
   LINKEDIN_PASSWORD=your_password
   OPENAI_API_KEY=your_openai_api_key
   LINKEDIN_LANGUAGE=en
   ```

5. **Prepare your post URLs:**
   - Create a file named `post_urls.csv` in the project root.
   - Add one LinkedIn post URL per line, e.g.:
     ```
     https://www.linkedin.com/posts/xyz...
     https://www.linkedin.com/posts/abc...
     ```

## Usage

Run the main script:
```bash
poetry run python likes_and_comments.py
```

The script will:
- Log in to LinkedIn (or reuse an active session)
- For each post URL, like the post and generate a comment using OpenAI
- Post the generated comment
- Log all actions and errors to the console

## Customization
- Edit the `agent_history` list in `likes_and_comments.py` to change the style and tone of the generated comments.
- Adjust the XPaths in the code if LinkedIn changes its layout.

## Troubleshooting
- Make sure your Chrome browser is up to date.
- If you get errors about elements not found, LinkedIn may have updated its UI. Update the XPaths accordingly.
- For OpenAI errors, check your API key and usage limits.

## Disclaimer
This project is for educational purposes only. Use responsibly and in accordance with LinkedIn's terms of service.
