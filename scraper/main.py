from src.pipeline import Pipeline
import time


if __name__ == "__main__":
    start_time = time.localtime()
    start = time.strftime("%H:%M:%S", start_time)
    print(start)
    pipeline = Pipeline()
    pipeline.run_again()
    finish_time = time.localtime()
    finish = time.strftime("%H:%M:%S", finish_time)
    print(finish)