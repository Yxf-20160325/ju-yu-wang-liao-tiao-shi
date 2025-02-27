# 代码由Yxf-20160325Github
# 导入必要的库
import socket
import tkinter as tk
import threading
import subprocess
import os
import logging

# 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()

# 绑定端口
port = 12345
server_socket.bind((host,port))

# 设置最大连接数
server_socket.listen(20)

print("服务器已启动，等待客户端连接...")
pwd = os.getcwd()  # 绝对路径
#版本为1.0
# 创建日志记录器
log_file_path = pwd
logging.basicConfig(filename='服务端日志.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 创建主窗口
root = tk.Tk()
root.title("服务器控制台")
print ("日志路径:" + log_file_path + "\服务器日志.log")
# 创建标签来显示连接状态
status_label = tk.Label(root, text="等待客户端连接...", font=("Helvetica", 14))
status_label.pack(pady=20)
label = tk.Label(root, text="服务端")
label.pack()
# 创建文本框来显示消息
message_text = tk.Text(root, width=50, height=10)
message_text.pack(pady=10)
# 创建发送框
send_entry = tk.Entry(root, width=50)
send_entry.pack(pady=10)
logging.info(f'已创建文本框')
# 创建发送按钮
send_button = tk.Button(root, text="发送", command=lambda: send_message(send_entry.get()))
send_button.pack(pady=10)
# 创建关闭按钮
close_cmd_button = tk.Button(root, text="关闭服务器", command=lambda: close_python())
close_cmd_button.pack(pady=10)

def close_python():
    # 关闭 python.exe 窗口的命令
    command = "taskkill /f /im py.exe"
    subprocess.run(command, shell=True)
    command_1 = "taskkill /f /im python.exe"
    subprocess.run(command_1, shell=True)
def update_status(message):
    def update():
        status_label.config(text=message)
    root.after(0, update)

def update_message(data):
    message_text.insert(tk.END, f"收到消息: {data}\n")
    logging.info(f'收到消息: {data}')
def send_message(message):
    # 这里可以添加发送消息的逻辑
    print(f"发送消息: {message}")
    logging.info(f'发送消息: {message}')
    # 发送消息给客户端
    client_socket.send(message.encode('utf-8'))
    
def handle_client(client_socket, addr):
    update_status(f"连接地址: {addr}")
   
    while True:
        try:
            # 接收客户端消息
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            update_message(data)
        except Exception as e:
            print(f"Error handling client: {e}")
        
        break

    # 关闭连接
    client_socket.close()
    update_status("客户端连接已关闭")

while True:
    # 接受客户端连接
    client_socket, addr = server_socket.accept()
    print(f"连接地址: {addr}")

    # 在新线程中处理客户端连接
    import threading
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()

    # 启动 GUI 主循环
    root.mainloop()
