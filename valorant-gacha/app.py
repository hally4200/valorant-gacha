from flask import Flask, render_template
import random
import os

app = Flask(__name__)

def load_crosshairs():
    data_list = []
    if not os.path.exists('crosshairs.txt'):
        return []

    with open('crosshairs.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split(',')
        # 名前, コード, 画像ファイル名, YouTubeID の4つがあるか確認
        # (>=4 にしているのは、将来的にデータを増やしてもエラーにならないための保険)
        if len(parts) >= 4:
            data_list.append({
                "name": parts[0],
                "code": parts[1],
                # 以前 rarity として使っていた場所を image_file に統一します
                "image_file": parts[2], 
                # 新しく追加！
                "youtube_id": parts[3].strip() 
            })
    return data_list

@app.route('/')
def gacha():
    data = load_crosshairs()
    
    if not data:
        # データがまだ古い形式のままの場合などのエラー対策
        return "ERROR: crosshairs.txt の形式が古いです。「名前,コード,画像,YouTubeID」の4つが必要です。"

    # ランダムに1つ選ぶ
    result = random.choice(data)
    
    # 選ばれたデータを画面に送る
    return render_template('index.html', 
                           name=result["name"], 
                           code=result["code"], 
                           # テンプレート側で使いやすい変数名で渡す
                           image_file=result["image_file"],
                           youtube_id=result["youtube_id"])

if __name__ == '__main__':
    app.run(debug=True)