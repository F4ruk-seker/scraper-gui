import time
from map_scraper import MapScraper
from map_scraper import Arrangement as AR


from alive_progress import alive_bar

def main():
    opt = MapScraper(
        target="https://www.google.com/maps/place/K%C3%B6fteci+Yusuf/@40.4229058,28.8603544,11z/data=!4m12!1m2!2m1!1sk%C3%B6fteci+yusuf!3m8!1s0x14ca5ba06ba716cd:0xd2955b80bb80466c!8m2!3d40.4229027!4d29.1652049!9m1!1b1!15sCg5rw7ZmdGVjaSB5dXN1ZiIDiAEBWhAiDmvDtmZ0ZWNpIHl1c3VmkgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11bwnxzbpv")

    opt.set_window_size(1280, 720)
    try:
        opt.go_target()
        bad_try_count = 0
        while not opt.is_available():
            time.sleep(1)
            bad_try_count += 1
            if bad_try_count > 10:
                print("DEBUG : bad_try_count END")
                break
        time.sleep(1)
        opt.change_arrangement(AR.LATEST)
        time.sleep(5)
        opt.active_progress_bar()
        opt.scrape_comments(max_count=500, time_out=20 * 1)
    finally:
        opt.close_bw()

    print(opt.get_comment_list())
    print(len(opt.get_comment_list()))


if __name__ == "__main__":
    main()

