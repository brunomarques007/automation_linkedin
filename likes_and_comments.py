import csv
import logging
import os
import time

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from linkedin_utils.driver_login import login, password, setup_driver, username
from linkedin_utils.openai_integration import generate_linkedin_comment

load_dotenv()

language = os.getenv("LINKEDIN_LANGUAGE")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def like_post(driver, url, max_retries=3, already_loaded=False) -> None:
    """Likes a LinkedIn post."""
    if not already_loaded:
        driver.get(url)
        time.sleep(4)
    for attempt in range(1, max_retries + 1):
        try:
            like_button = driver.find_element(
                By.XPATH, "//button[contains(@aria-label, 'React Like')]"
            )
            if "Liked" in like_button.get_attribute("aria-label"):
                logging.info(f"Post already liked: {url}")
                return
            like_button.click()
            logging.info(f"Post liked: {url}")
            time.sleep(1)
            return
        except Exception as e:
            logging.warning(f"Attempt {attempt} - Error liking post: {e}")
            if attempt == max_retries:
                logging.error(
                    f"Failed to like post after {max_retries} attempts: {url}"
                )
            else:
                time.sleep(2)


def comment_post(
    driver, url, comment, max_retries=3, already_loaded=False
) -> None:
    """Comments on a LinkedIn post."""
    if not already_loaded:
        driver.get(url)
        time.sleep(3)
    for attempt in range(1, max_retries + 1):
        try:
            # Try to open the comment box if necessary
            try:
                comment_box = driver.find_element(
                    By.XPATH, "//div[@role='textbox']"
                )
            except Exception:
                comment_btn = driver.find_element(
                    By.XPATH,
                    "//button[contains(@aria-label, 'Comment') and not(contains(@aria-label, 'Add a comment'))]",
                )
                comment_btn.click()
                time.sleep(1)
                comment_box = driver.find_element(
                    By.XPATH, "//div[@role='textbox']"
                )
            comment_box.click()
            comment_box.clear()
            comment_box.send_keys(comment)
            time.sleep(2)
            comment_button = driver.find_element(
                By.XPATH,
                "//button[contains(@id, 'ember') and contains(@class, 'artdeco-button--primary')]",
            )
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                comment_button,
            )
            time.sleep(2)
            try:
                comment_button.click()
                time.sleep(2)
            except Exception:
                driver.execute_script("arguments[0].click();", comment_button)
            logging.info(f"Comment posted on: {url}")
            time.sleep(1)
            return
        except Exception as e:
            logging.warning(
                f"Attempt {attempt} - Error commenting on post: {e}"
            )
            if attempt == max_retries:
                logging.error(
                    f"Failed to comment on post after {max_retries} attempts: {url}"
                )
            else:
                time.sleep(1)


def get_post_text(driver, url, already_loaded=False) -> str:
    """Extracts the text from a LinkedIn post."""
    if not already_loaded:
        driver.get(url)
        time.sleep(2)
    try:
        # Example XPath for the main post text
        post_element = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'feed-shared-update-v2__description')]//span",
        )
        return post_element.text.strip()
    except Exception:
        logging.warning(f"Could not extract post text: {url}")
        return ""


def like_and_comment(
    driver, post_urls, agent_history=None, max_retries=3
) -> None:
    """Likes and comments on a list of LinkedIn posts."""
    for url in post_urls:
        driver.get(url)
        time.sleep(2)
        like_post(driver, url, max_retries, already_loaded=True)
        post_text = get_post_text(driver, url, already_loaded=True)
        comment = generate_linkedin_comment(post_text, agent_history)
        comment_post(driver, url, comment, max_retries, already_loaded=True)

    logging.info("Process completed.")


def main() -> None:
    """Main function for the LinkedIn like and comment script."""
    post_urls = []

    with open("post_urls.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        post_urls = [row[0] for row in reader if row]

    agent_history = [
        "You are a LinkedIn professional who replies to posts in an engaging, cordial, and relevant way.",
        "Be brief, positive, and encourage discussion.",
        "No use of emojis",
        "Write only one paragraph comments.",
    ]

    driver = setup_driver()
    if driver.current_url != "https://www.linkedin.com/feed/":
        logging.info("Starting LinkedIn login...")
        login(driver, username, password)
    like_and_comment(driver, post_urls, agent_history)

    driver.quit()


if __name__ == "__main__":
    main()
