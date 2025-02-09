import time
import threading

class GroqRateLimiter:
    def __init__(self, max_tpm=5000, interval=60):
        self.max_tpm = max_tpm  # 🔹 Max tokens per minute
        self.interval = interval  # 🔹 Time window in seconds
        self.tokens_used = 0
        self.lock = threading.Lock()

    def wait_for_tokens(self, tokens_requested):
        """
        Waits if the next request would exceed the token-per-minute (TPM) limit.
        """
        with self.lock:
            while self.tokens_used + tokens_requested > self.max_tpm:
                time_to_wait = self.interval / 2  # 🔹 Adjust wait time dynamically
                print(f"⏳ Rate limit close to max. Waiting {time_to_wait:.1f}s...")
                time.sleep(time_to_wait)
                self.tokens_used = max(0, self.tokens_used - self.max_tpm)  # Reset after wait

            self.tokens_used += tokens_requested  # Track token usage

rate_limiter = GroqRateLimiter()
