from tenacity import retry, stop_after_attempt, wait_fixed

# 🔥 retry برای queryهای مهم
def db_retry():
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1)
    )