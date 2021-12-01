import os

import yaml
from dotenv import load_dotenv
from trello import TrelloClient


TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
TRELLO_SECRET = os.getenv('TRELLO_SECRET')
 
client = TrelloClient(api_key=TRELLO_API_TOKEN, api_secret=TRELLO_SECRET)


class TrelloOperation:
    def __init__(self, client):
        self.client = client
        self.loadcfgyaml()

    def loadcfgyaml(self):
        """設定ファイルを読み込み、クラス全体で使用できるようにselfの変数化する"""
        load_dotenv()
        with open('config.yml', 'r') as yml:
            config = yaml.safe_load(yml)
        self.cfg = config
        self.cfg_teams = config['teams']

    def openboard_getallname(self) -> list:
        """既存のボード名のリストを作成する
        list_boards()は完全削除前のアーカイブのボードも取得するため
        closedしていないボードの名前一覧を取得する
        """
        boards = client.list_boards()
        boards_name = [] 
        for board in boards:
            if not board.closed: 
                boards_name.append(board.name)
        return boards_name

    def createboard_defaultlist(self):
        """コンフィグにある値でボードとリストを作成する"""
        for team_name, members  in self.cfg_teams.items():
            # 作ろうとしているボード名と既存ボード名に被りがない時のみボードを作成
            boards_name = self.openboard_getallname()
            if not team_name in boards_name:
                board = client.add_board(team_name, permission_level='private')
                print(f"[INFO] ボード「 {team_name} 」を作成しました")
                for member_name in members:
                    print(member_name)
                    board.add_list(member_name)
                    print(f"[INFO] ボード{team_name}にリスト「 {member_name} 」を作成しました")
            else:
                print(f"[WARN] ボード「 {team_name} 」は作成済みです")
    
    def boards_getname(self, boards):
        """引数に渡されたboardsオブジェクトから
        削除されていないボードの名前だけを取得する"""
        nonarchive_boards = [ b for b in boards if b.closed is False]
        return nonarchive_boards

    def check_selectboards(self, boards, select_boardname):
        """指定した名前のボードが存在するか確認する"""
        nonarchive_boards = self.boards_getname(boards)
        select_board = [ nb for nb in nonarchive_boards if nb.name == select_boardname]
        return select_board

    def main(self):
        self.createboard_defaultlist()


trello = TrelloOperation(client)
trello.main()