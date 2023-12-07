import socket
import os

def send_file(server_ip, server_port, directory_path):
    # 创建客户端套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 获取目录名称
        directory_name = os.path.basename(directory_path)

        # 发送目录名
        client_socket.sendto(directory_name.encode(), (server_ip, server_port))

        # 遍历目录中的文件并逐个发送
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)

            # 读取文件内容
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # 发送文件名
            client_socket.sendto(file_name.encode(), (server_ip, server_port))

            # 发送文件大小
            file_size = len(file_data)
            client_socket.sendto(str(file_size).encode(), (server_ip, server_port))

            # 接收服务器确认
            server_response, server_address = client_socket.recvfrom(1024)
            print(server_response.decode())

            # 发送文件内容
            chunk_size = 1024  # 每次发送的数据块大小
            total_chunks = (file_size // chunk_size) + 1  # 计算总共需要发送的数据块数量

            # 分块发送文件内容
            for i in range(total_chunks):
                start_idx = i * chunk_size
                end_idx = (i + 1) * chunk_size
                chunk_data = file_data[start_idx:end_idx]
                client_socket.sendto(chunk_data, (server_ip, server_port))

            print(f'{file_name} 传输完毕')

    except Exception as e:
        print('文件传输失败:', e)

    finally:
        # 关闭客户端套接字
        client_socket.close()


# 输入服务器 IP 和端口
server_ip = input('请输入服务器 IP 地址: ')
server_port = int(input('请输入服务器端口号: '))

# 输入要传输的目录路径
directory_path = input('请输入要传输的目录路径: ')

# 调用函数传输目录内的文件
send_file(server_ip, server_port, directory_path)