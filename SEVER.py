import socket
import os

def receive_file(server_ip, server_port):
    # 创建服务器套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定服务器地址和端口
    server_socket.bind((server_ip, server_port))

    print('服务器已启动，等待文件传输...')

    try:
        # 接收目录名
        directory_name, client_address = server_socket.recvfrom(1024)
        directory_name = directory_name.decode()
        os.makedirs(directory_name, exist_ok=True)

        while True:
            # 接收文件名
            file_name, client_address = server_socket.recvfrom(1024)
            file_name = file_name.decode()

            if file_name == 'END':
                print('所有文件接收完毕')
                break

            # 接收文件大小
            file_size, client_address = server_socket.recvfrom(1024)
            file_size = int(file_size.decode())
            server_socket.sendto('文件大小已接收'.encode(), client_address)

            # 接收文件内容
            file_data = b''  # 初始化接收文件的数据

            chunk_size = 1024  # 每次接收的数据块大小
            total_chunks = (file_size // chunk_size) + 1  # 计算总共需要接收的数据块数量

            # 分块接收文件内容
            for i in range(total_chunks):
                chunk, client_address = server_socket.recvfrom(chunk_size)
                file_data += chunk

            server_socket.sendto('文件内容已接收'.encode(), client_address)

            # 保存文件到目录中
            file_path = os.path.join(directory_name, file_name)
            with open(file_path, 'wb') as file:
                file.write(file_data)

            print(f'{file_name} 接收完毕')

    except Exception as e:
        print('文件接收失败:', e)

    finally:
        # 关闭服务器套接字
        server_socket.close()


# 输入服务器 IP 和端口
server_ip = '127.0.0.1'
server_port = 51000

# 调用函数接收文件
receive_file(server_ip, server_port)