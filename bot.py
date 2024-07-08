import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import random
import json
from urllib.parse import parse_qs

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")
config_file = os.path.join(script_dir, "config.json")


class MatchQuest:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}MatchQuest Auto Claimer
        t.me/smartairdrop2120
        
        """

        self.parse_data = lambda data: {
            key: value[0] for key, value in parse_qs(data).items()
        }

        self.autogame = (
            json.load(open(config_file, "r")).get("autogame", "false").lower() == "true"
        )

    def headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://tgapp.matchain.io",
            "Priority": "u=1, i",
            "Referer": "https://tgapp.matchain.io/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def login(self, data):
        parser = self.parse_data(data)
        user = json.loads(parser["user"])
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/login"
        headers = self.headers()
        payload = json.dumps(
            {
                "uid": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "username": user["username"],
                "tg_login_params": data,
            }
        )
        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def get_profile(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/profile"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def get_balance(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/balance"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def get_reward(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def farming(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        headers["Content-Length"] = str(len(payload))

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def claim(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        headers["Content-Length"] = str(len(payload))

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def invite_claim(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def play_game(self, token):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"
        headers = self.headers()
        headers["authorization"] = token

        while True:
            response = requests.get(url=url, headers=headers)
            game_id = response.json()["data"]["game_id"]
            game_count = response.json()["data"]["game_count"]
            if response.status_code != 200:
                self.log(f"{red}Something went wrong. Please try to re-run!")
                return False
            if game_id != "":
                try:
                    self.log(f"{yellow}Playing game...")
                    time.sleep(30)
                    point = random.randint(50, 100)
                    payload = json.dumps({"game_id": game_id, "point": point})
                    url_claim = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
                    res_game = requests.post(
                        url=url_claim, headers=headers, data=payload
                    )
                    if res_game.status_code != 200:
                        self.log(f"{red}Play game failure!")
                        continue

                    self.log(f"{green}Play game successful, earned {white}{point}")
                    self.log(f"{green}Game left: {white}{game_count}")
                    if game_count <= 0:
                        self.log(f"{yellow}Run out of ticket!")
                        return False
                except:
                    self.log(f"{red}Play game error!")
                    return False
            else:
                self.log(f"{yellow}No game ticket to play!")
                return False

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            end_at_list = []
            data = open(data_file, "r", encoding="utf8").read().strip().split("\n")
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Login
                try:
                    self.log(f"{yellow}Getting user information...")
                    login = self.login(data=data).json()
                    token = login["data"]["token"]
                    user_id = login["data"]["user"]["uid"]
                    self.log(f"{green}User ID: {white}{user_id}")

                    # Balance
                    try:
                        get_balance = self.get_balance(
                            token=token, user_id=user_id
                        ).json()
                        balance = get_balance["data"]
                        self.log(f"{green}Balance: {white}{balance / 1000}")
                    except Exception as e:
                        self.log(f"{red}Get balance error!!!")

                    # Claim from ref
                    try:
                        self.log(f"{yellow}Trying to claim from ref...")
                        invite_claim = self.invite_claim(
                            token=token, user_id=user_id
                        ).json()
                        claim_from_ref = int(invite_claim["data"])
                        if claim_from_ref != 0:
                            self.log(
                                f"{green}Claim from ref: {white}{claim_from_ref / 1000}"
                            )
                        else:
                            self.log(f"{yellow}No point from ref!")
                    except Exception as e:
                        self.log(f"{red}Claim from ref error!!!")

                    # Play game
                    if self.autogame:
                        self.play_game(token=token)
                        # Balance
                        try:
                            get_balance = self.get_balance(
                                token=token, user_id=user_id
                            ).json()
                            balance = get_balance["data"]
                            self.log(f"{green}Current balance: {white}{balance / 1000}")
                        except Exception as e:
                            self.log(f"{red}Get balance error!!!")

                    # Reward and Farming/Claim
                    try:
                        while True:
                            get_reward = self.get_reward(
                                token=token, user_id=user_id
                            ).json()
                            next_claim = get_reward["data"]["next_claim_timestamp"]
                            if next_claim == 0:
                                self.log(f"{yellow}Trying to farm...")
                                farming = self.farming(token=token, user_id=user_id)
                                if farming.status_code != 200:
                                    self.log(f"{red}Cannot process farming!")
                                    continue
                                else:
                                    self.log(f"{green}Farm successful!")
                                    break
                            if next_claim > round(time.time() * 1000):
                                self.log(f"{yellow}Not time to claim yet!")
                                end_at = (
                                    float(get_reward["data"]["next_claim_timestamp"])
                                    / 1000
                                )
                                readable_time = datetime.fromtimestamp(end_at).strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                )
                                self.log(f"{green}Farm end at: {white}{readable_time}")
                                end_at_list.append(end_at)
                                break
                            get_profile = self.get_profile(token=token, user_id=user_id)
                            get_balance = self.get_balance(token=token, user_id=user_id)
                            get_reward = self.get_reward(token=token, user_id=user_id)
                            self.log(f"{yellow}Trying to claim...")
                            claim = self.claim(token=token, user_id=user_id)
                            if claim.status_code != 200:
                                self.log(f"{red}Cannot claim right now!")
                                print(claim.content)
                                break
                            else:
                                self.log(f"{green}Claim successful!")
                                self.log(f"{yellow}Trying to farm...")
                                time.sleep(60)
                                farming = self.farming(token=token, user_id=user_id)
                                if farming.status_code != 200:
                                    self.log(f"{red}Cannot process farming!")
                                    continue
                                else:
                                    self.log(f"{green}Farm successful!")

                            # Balance
                            try:
                                get_balance = self.get_balance(
                                    token=token, user_id=user_id
                                ).json()
                                balance = get_balance["data"]
                                self.log(
                                    f"{green}Current balance: {white}{balance / 1000}"
                                )
                            except Exception as e:
                                self.log(f"{red}Get balance error!!!")
                    except Exception as e:
                        self.log(f"{red}Get reward error!!!")
                except Exception as e:
                    self.log(f"{red}Login error!!!")
                    print(2)

            print()
            # Wait time
            if end_at_list:
                now = datetime.now().timestamp()
                wait_times = [end_at - now for end_at in end_at_list if end_at > now]
                if wait_times:
                    wait_time = min(wait_times)
                else:
                    wait_time = 15 * 60
            else:
                wait_time = 15 * 60

            wait_hours = int(wait_time // 3600)
            wait_minutes = int((wait_time % 3600) // 60)
            wait_seconds = int(wait_time % 60)

            wait_message_parts = []
            if wait_hours > 0:
                wait_message_parts.append(f"{wait_hours} hours")
            if wait_minutes > 0:
                wait_message_parts.append(f"{wait_minutes} minutes")
            if wait_seconds > 0:
                wait_message_parts.append(f"{wait_seconds} seconds")

            wait_message = ", ".join(wait_message_parts)
            self.log(f"{yellow}Wait for {wait_message}!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        match_quest = MatchQuest()
        match_quest.main()
    except KeyboardInterrupt:
        sys.exit()
