#!/usr/bin/python3
import sys


class game:
    def __init__(self, senkou):  # 初期化。マス（リスト）の作成、マスに表示するマーク、先手を設定。
        self.table = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.mark = {1:['1P', '●'], 2:['2P', '✕']}
        self.user = senkou
        self.exit = False
        self.collision = False

    def main(self):  # このゲームのメイン処理を担うメソッド。重複チェック、勝ち判定メソッドを呼び出す。
        if not self.collision:  # 重複して再度入力の状態の時は、邪魔なので省く。
            print('{0}の番です'.format(self.mark[self.user][0]))
            self.collision = False
        point = list(map(int, input('どこ?: ').split()))

        if self.table[point[0]][point[1]] != 0:  # 重複チェック（単体）
            print('不正はダメ！')
            self.collision = True
            return

        self.table[point[0]][point[1]] = self.user
        self.draw()  # マスを出力

        if self.clear_check():  # 勝ち判定メソッド
            print('{0}の勝ちです！'.format(self.mark[self.user][0]))
            self.exit = True

        if self.user == 1:  # 交代
            self.user = 2
        else:
            self.user = 1

    def clear_check(self):
        # 横列チェック
        col = self.table[0][0] == self.table[0][1] == self.table[0][2] == self.user or \
                                        self.table[1][0] == self.table[1][1] == self.table[1][2] == self.user or \
                                        self.table[2][0] == self.table[2][1] == self.table[2][2] == self.user
        # 縦列チェック
        row = self.table[0][0] == self.table[1][0] == self.table[2][0] == self.user or \
                                        self.table[0][1] == self.table[1][1] == self.table[2][1] == self.user or \
                                        self.table[0][2] == self.table[1][2] == self.table[2][2] == self.user
        # 斜列チェック
        naname = self.table[0][0] == self.table[1][1] == self.table[2][2] == self.user or \
                                        self.table[0][2] == self.table[1][1] == self.table[2][0] == self.user
        return col or row or naname

    def draw(self):
        for i in self.table:
            print("|".join(list(map(self.mapping, i))))

    def mapping(self, num):
        if num == 0:
            return '-'
        if num == 1:
            return self.mark[1][1]
        if num == 2:
            return self.mark[2][1]
        return 0


# init
g = game(1)

# main
while True:
    g.main()
    if g.collision:
        continue
    if g.exit:
        sys.exit()
