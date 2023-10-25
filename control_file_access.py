import os
import tkinter as tk
from tkinter import filedialog

# フォルダのパスを保持する変数
folder_path = ""

def apply_permissions_to_folder(directory, file_permissions):
    try:
        os.chmod(directory, file_permissions)  # フォルダのパーミッションを設定する
    except Exception as e:
        status_label.config(text=f'フォルダのアクセスに失敗しました: {e}')
        return

    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.chmod(dir_path, file_permissions)  # サブフォルダのパーミッションを設定
            except Exception as e:
                status_label.config(text=f'フォルダのアクセスに失敗しました: {e}')
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.chmod(file_path, file_permissions)  # ファイルのパーミッションを設定
            except Exception as e:
                status_label.config(text=f'ファイルのアクセス権限の設定に失敗しました: {e}')

# フォルダを読み取り専用にする関数。つまり、書き込みができなくなる。
def make_read_only():
    global folder_path
    apply_permissions_to_folder(folder_path, 0o555)  # 読み取り専用のパーミッション
    status_label.config(text="書き込み不可")


# フォルダを書き込み可能にする関数
def make_writable():
    global folder_path
    apply_permissions_to_folder(folder_path, 0o755)  # 読み書き可能のパーミッション
    status_label.config(text="書き込み可能")

# フォルダを選択する関数
def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_label.config(text=folder_path)

# GUIウィンドウの作成
root = tk.Tk()
root.title("書き込み禁止")
get_width, get_height  = [root.winfo_screenwidth(), root.winfo_screenheight()] #ユーザーのディスプレイのwidth, heightを求める
half_width, half_height = [get_width // 2, get_height // 2] #真ん中に位置するように適当に1/2をした。多分、この計算だと、偏るかも
root.geometry(f"200x100+{half_width}+{half_height}")

# フォルダを選択するボタン。
select_button = tk.Button(root, text="フォルダを選択", command=select_folder)
select_button.pack()

# 選択したフォルダのパスを表示するラベル
folder_label = tk.Label(root, text="")
folder_label.pack()

# フォルダを読み取り専用にするボタン。つまり、書き込み不可能にするボタン
readonly_button = tk.Button(root, text="書き込み不可能にする", command=make_read_only)
readonly_button.pack()

# フォルダを書き込み可能にするボタン。
writable_button = tk.Button(root, text="書き込み可能にする", command=make_writable)
writable_button.pack()

# ステータスを表示するラベル。
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()