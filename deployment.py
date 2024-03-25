import time
import paramiko


# SSH服务器的设置
def run_order(hostname, port, username, password):
    hostname = hostname
    port = port
    username = username
    password = password

    # 创建SSH客户端实例
    client = paramiko.SSHClient()
    print("+"*20 + " begin " + hostname + " +"*20)
    # 自动添加服务器的主机名和新的主机密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接到服务器
    client.connect(hostname, port, username, password)
    # 运行命令 更新代码从清华网盘
    # https://cloud.tsinghua.edu.cn/f/bded3fe038ac44a4b4fa/?dl=1
    command_list = ["wget -O /root/capture_traffic/capture.py https://cloud.tsinghua.edu.cn/f/4619e69340f5459fa0b2/?dl=1",
                    "wget -O /root/capture_traffic/script.py https://cloud.tsinghua.edu.cn/f/fb3d73b3fa82415bb962/?dl=1",
                    ]
    #client.exec_command("mkdir /root/capture_traffic")
    #client.exec_command("pip3 install psutil")
    #time.sleep(5)
    for command in command_list:
        stdin, stdout, stderr = client.exec_command(command)
        time.sleep(3)
        err = stderr.read().decode()
        if err:
            print(f"Error: {err}")

        # 读取命令结果
        for line in stdout:
            print(line.strip('\n'))

    # 这里的目的 是找到进程号，然后kill
    command_list = ["ps aux | grep capture.py", "ps aux |grep python3", "ps aux | grep script.py"]
    for index, command in enumerate(command_list):
        print(command)
        stdin, stdout, stderr = client.exec_command(command)

        # 读取命令结果
        for line in stdout:
            line = line.strip('\n')
            if index == 0 and "capture.py -b" in line:
                print(line)
                line = line.split(' ')
                for item in line:
                    if item.isdigit():
                        print("need kill pid is:", item)
                        stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                        break
            elif index == 1 and "tshark -i" in line:
                print(line)
                line = line.split(' ')
                for item in line:
                    if item.isdigit():
                        print("need kill pid is:", item)
                        stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                        break
            elif index == 2 and "script.py" in line:
                print(line)
                line = line.split(' ')
                for item in line:
                    if item.isdigit():
                        print("need kill pid is:", item)
                        stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                        break

    # 这里是重新部署
    # nohup capture.py -b enp4s1 -s ip &
    stdin, stdout, stderr = client.exec_command("cd /root/capture_traffic; nohup python3 capture.py -b ens18 -s {} &".format(hostname))
    print("cd /root/capture_traffic; nohup python3 capture.py -b ens18 -s {} &".format(hostname))
    time.sleep(2)

    # 这里检查是否部署成功，查看运行状态
    stdin, stdout, stderr = client.exec_command("ps aux|grep -E 'capture.py|tshark|script.py'")
    print('\n')
    # 读取命令结果
    for line in stdout:
        line = line.strip('\n')
        print(line)
    print("+" * 20 + " end " + hostname + "+ " * 20)
    print('\n')

    # 关闭连接
    client.close()


#hostname = ['10.7.253.123', '10.7.253.124', '10.7.253.125', '10.7.253.126', '10.7.253.127','10.7.253.128', '10.7.253.129', '10.7.253.130', '10.7.253.131', '10.7.253.132']
hostname = ['10.2.0.186','10.2.0.187','10.2.0.188','10.2.0.189','10.2.0.190']
port = 22
username = 'root'
password = 'thusw0rd'

for host in hostname:
    run_order(host, port, username, password)
