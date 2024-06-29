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
            "host": "tgapp-api.matchain.io",
            "connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://tgapp.matchain.io",
            "x-requested-with": "tw.nekomimi.nekogram",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://tgapp.matchain.io/",
            "accept-language": "en,en-US;q=0.9",
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

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def claim(self, token, user_id):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
        headers = self.headers()
        headers["authorization"] = token
        payload = json.dumps({"uid": user_id})

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def play_game(self, token):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"
        headers = self.headers()
        headers["authorization"] = token
        first_call = True

        while True:
            response = requests.get(url=url, headers=headers)
            game_id = response.json()["data"]["game_id"]
            game_count = response.json()["data"]["game_count"]
            if response.status_code != 200:
                self.log(f"{red}Something went wrong. Please try to re-run!")
                return False
            if game_count <= 0:
                if first_call:
                    self.log(f"{yellow}You don't have a game ticket!")
                    return False
            try:
                self.log(f"{yellow}Playing game...")
                self.countdown(30)
                point = random.randint(50, 100)
                payload = json.dumps({"game_id": game_id, "point": point})
                url_claim = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
                res_game = requests.post(url=url_claim, headers=headers, data=payload)
                if res_game.status_code != 200:
                    self.log(f"{red}Play game failure!")
                    continue

                self.log(f"{green}Play game successful, earned {white}{point}")
                self.log(f"{green}Game left: {white}{game_count}")
                first_call = False
                if game_count <= 0:
                    self.log(f"{yellow}Run out of ticket!")
                    return False
            except:
                self.log(f"{red}Play game error!")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        self.clear_terminal()
        print(self.banner)
        data = open(data_file, "r").read().splitlines()
        num_acc = len(data)
        self.log(self.line)
        self.log(f"{green}Numer of account: {white}{num_acc}")
        while True:
            end_at_list = []
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Login
                try:
                    self.log(f"{yellow}Getting user information...")
                    login = self.login(data=data).json()
                    token = login["data"]["token"]
                    user_id = login["data"]["user"]["uid"]
                    first_name = login["data"]["user"]["first_name"]
                    user_name = login["data"]["user"]["username"]
                    invite_limit = login["data"]["user"]["invite_limit"]
                    self.log(
                        f"{green}User info: {white}{first_name} ({user_name} - {user_id})"
                    )
                    self.log(f"{green}Invite limit: {white}{invite_limit}")

                    # Balance
                    try:
                        get_balance = self.get_balance(
                            token=token, user_id=user_id
                        ).json()
                        balance = get_balance["data"]
                        self.log(f"{green}Balance: {white}{balance / 1000}")
                    except Exception as e:
                        self.log(f"{red}Get balance error!!!")

                    # Reward
                    try:
                        get_reward = self.get_reward(
                            token=token, user_id=user_id
                        ).json()
                        end_at = (
                            float(get_reward["data"]["next_claim_timestamp"]) / 1000
                        )
                        readable_time = datetime.fromtimestamp(end_at).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        self.log(f"{green}Farm end at: {white}{readable_time}")
                        end_at_list.append(end_at)
                    except Exception as e:
                        self.log(f"{red}Get reward error!!!")

                    # Claim
                    try:
                        self.log(f"{yellow}Trying to claim...")
                        claim = self.claim(token=token, user_id=user_id).json()
                        if claim["code"] == 400:
                            self.log(f"{yellow}Not time to claim yet!")
                        else:
                            self.log(f"{green}Claim successful!")
                            # Balance
                            try:
                                get_balance = self.get_balance(
                                    token=token, user_id=user_id
                                ).json()
                                balance = get_balance["data"]
                                self.log(
                                    f"{green}Balance after Claim: {white}{balance / 1000}"
                                )
                            except Exception as e:
                                self.log(f"{red}Get balance error!!!")

                            # Farming
                            try:
                                self.log(f"{yellow}Trying to farm...")
                                farming = self.farming(
                                    token=token, user_id=user_id
                                ).json()
                                if farming["code"] == 400:
                                    self.log(f"{yellow}Not time to farm yet!")
                                else:
                                    self.log(f"{green}Farm successful!")
                            except Exception as e:
                                self.log(f"{red}Farming error!!!")

                    except Exception as e:
                        self.log(f"{red}Claim error!!!")

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

                except Exception as e:
                    self.log(f"{red}Login error!!!")

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