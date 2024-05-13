import tkinter as tk
from tkinter import messagebox, filedialog
import requests


def check_for_updates():
    """检查 GitHub 上的新版本并获取.exe文件的下载链接"""
    repo_owner = "xuqiu-git"
    repo_name = "photoClean"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200 and 'assets' in data:
        for asset in data['assets']:
            if asset['name'].endswith('.exe'):
                return data['tag_name'], asset['browser_download_url']
        return data['tag_name'], None  # 如果没有找到.exe文件
    else:
        return None, None


def download_update(download_url):
    """让用户选择下载路径并下载新版本的文件"""
    save_path = filedialog.asksaveasfilename(
        title="保存新版本为",
        filetypes=[("Executable files", "*.exe")],
        defaultextension=".exe"
    )
    if save_path:
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            messagebox.showinfo("下载成功", "新版本已下载完成！")
        else:
            messagebox.showerror("下载失败", "无法下载新版本。")
    else:
        messagebox.showinfo("取消下载", "更新下载已取消。")


def update_software():
    latest_version, download_url = check_for_updates()
    if download_url:
        response = messagebox.askyesno("发现新版本", f"最新版本 {latest_version} 可用。是否下载？")
        if response:
            download_update(download_url)
    elif latest_version:
        messagebox.showinfo("无新版本", f"当前已是最新版本 {latest_version}。")
    else:
        messagebox.showerror("检查失败", "无法检查更新。")


# root = tk.Tk()
# update_button = tk.Button(root, text="检查更新", command=update_software)
# update_button.pack(pady=20)
# root.mainloop()