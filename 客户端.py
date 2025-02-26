# 导入必要的库
import socket
import tkinter as tk
import subprocess
import logging
import os
# 创建 socket 对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取本地主机名
host = socket.gethostname()

pwd = os.getcwd()  # 绝对路径
#版本为1.0
# 创建日志记录器
log_file_path = pwd
print(log_file_path)
logging.basicConfig(filename='客户端日志.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 连接到服务器
port = 12345
client_socket.connect((host, port))
# 记录连接信息
logging.info(f'链接服务端主机名、端口:{host}:{port}')
# 创建主窗口
root = tk.Tk()
root.title("客户端控制台")
# 创建标签来显示连接状态
status_label = tk.Label(root, text="已连接到服务器", font=("Helvetica", 14))
status_label.pack(pady=20)
label = tk.Label(root, text="客户端")
label.pack()
logging.info(f'已连接到服务器')
# 创建文本框来显示消息
message_text = tk.Text(root, width=50, height=10)
message_text.pack(pady=10)
logging.info(f'已创建文本框')
# 创建输入框来输入消息
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)
logging.info(f'已创建输入框')
def send_message():
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

def receive_message():
    while True:
        try:
            # 接收服务器消息
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            update_message(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
        
   

def update_message(data):
    message_text.insert(tk.END, f"收到消息: {data}\n")
    logging.info(f'收到消息: {data}')
# 创建发送按钮
send_button = tk.Button(root, text="发送", command=send_message)
send_button.pack(pady=10)
def close_python_button():
    # 关闭 python 窗口的命令
    command = "taskkill /f /im py.exe"
    subprocess.run(command, shell=True)
    
kill_python = tk.Button(root, text="关闭客户端", command=lambda:close_python_button())
kill_python.pack(pady=10)
# 启动接收消息线程
import threading
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()
logging.info(f'已启动接收消息线程')
# 启动主循环
root.mainloop()
