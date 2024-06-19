from instabot import Bot
import time
import logging
from datetime import datetime, timedelta
import schedule

# Setting up logging
logging.basicConfig(filename='instabot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InstagramBot:
    def __init__(self, username, password):
        self.bot = Bot()
        self.username = username
        self.password = password

    def login(self):
        try:
            self.bot.login(username=self.username, password=self.password)
            logging.info("Logged in successfully.")
        except Exception as e:
            logging.error(f"Login failed: {e}")

    def logout(self):
        try:
            self.bot.logout()
            logging.info("Logged out successfully.")
        except Exception as e:
            logging.error(f"Logout failed: {e}")

    def follow_user(self, user):
        try:
            self.bot.follow(user)
            logging.info(f"Followed {user}.")
        except Exception as e:
            logging.error(f"Failed to follow {user}: {e}")

    def unfollow_user(self, user):
        try:
            self.bot.unfollow(user)
            logging.info(f"Unfollowed {user}.")
        except Exception as e:
            logging.error(f"Failed to unfollow {user}: {e}")

    def upload_photo(self, photo_path, caption):
        try:
            self.bot.upload_photo(photo_path, caption=caption)
            logging.info(f"Uploaded photo {photo_path} with caption: {caption}")
        except Exception as e:
            logging.error(f"Failed to upload photo {photo_path}: {e}")

    def send_message(self, message, users):
        try:
            self.bot.send_message(message, users)
            logging.info(f"Sent message '{message}' to users: {users}")
        except Exception as e:
            logging.error(f"Failed to send message '{message}': {e}")

    def get_followers(self):
        try:
            followers = self.bot.get_user_followers(self.username)
            logging.info(f"Retrieved followers for {self.username}.")
            return followers
        except Exception as e:
            logging.error(f"Failed to get followers for {self.username}: {e}")
            return []

    def like_user_posts(self, user, amount=5):
        try:
            user_id = self.bot.get_user_id_from_username(user)
            media_ids = self.bot.get_last_user_medias(user_id, amount)
            for media_id in media_ids:
                self.bot.like(media_id)
            logging.info(f"Liked {amount} posts of {user}.")
        except Exception as e:
            logging.error(f"Failed to like posts of {user}: {e}")

    def comment_user_post(self, user, comment):
        try:
            user_id = self.bot.get_user_id_from_username(user)
            media_id = self.bot.get_last_user_medias(user_id, 1)[0]
            self.bot.comment(media_id, comment)
            logging.info(f"Commented on {user}'s post: {comment}")
        except Exception as e:
            logging.error(f"Failed to comment on {user}'s post: {e}")

    def schedule_post(self, photo_path, caption, post_time):
        schedule_time = datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S")
        delay = (schedule_time - datetime.now()).total_seconds()

        if delay < 0:
            logging.error(f"Scheduled time {post_time} is in the past.")
            return

        schedule.enter(delay, 1, self.upload_photo, (photo_path, caption))
        logging.info(f"Scheduled post for {post_time}.")

    def start_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    bot = InstagramBot(username="krishh_17_03", password="Krishh_17_03@09876")
    bot.login()

    bot.follow_user('pawankalyan')
    bot.upload_photo("C:/Users/HP/Pictures/its.jpg", caption="Its me")
    bot.unfollow_user('pawankalyan')
    bot.send_message("Hello", ['tanu_patil295', 'priya_kz_1511'])

    followers = bot.get_followers()
    for follower in followers:
        user_info = bot.get_user_info(follower)
        print(user_info)

    bot.like_user_posts('pawankalyan', amount=3)
    bot.comment_user_post('pawankalyan', 'Great post!')

    # Schedule a post for tomorrow at 9:00 AM
    post_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 09:00:00")
    bot.schedule_post("C:/Users/HP/Pictures/its.jpg", "Scheduled post", post_time)

    # Start the scheduler
    bot.start_scheduler()

    bot.logout()
