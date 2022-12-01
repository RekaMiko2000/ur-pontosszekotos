from math import sqrt
import socket
import time
import argparse

class TCP_Client:
    def __init__(self,ip_address:str,port:int):
        self.ip=ip_address
        self.port=port
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.radius=None
        self.y=None
        self.x=None
        self.center_y=None
        self.center_x=None
        self.new_y=None
        self.new_x=None
        self.shift=None
        self.dist=None
        self.time=None
    def draw(self,filename):
        print("Running main funciton")
        socket=self.socket
        socket.connect((self.ip,self.port))
        #socket.send(bytes("movel(p[0.15738, -0.25685, -0.1, 3.14, 0.0, 0.00], a=1.0, v=0.04)"+"\n","utf-8"))
        socket.send(bytes("movel(p[0.160, -0.235, -0.1, 2.24, -2.24, 0.00], a=0.8, v=0.03)"+"\n","utf-8"))
        time.sleep(6)
        print("Can I start the drawing?(y/yes/n/no)")
        answer=input()
        if answer in ["y","yes"]:
            try:
                with open(filename,"r",encoding="utf-8") as f:
                    file=f.readlines()
                    for line in file:
                        line=line.replace("\n","")
                        if line!="\n" or (line[0]!="#" and line[0]!=""):
                            data=line.split(" ")
                            if data[0]=="time":
                                self.time=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="radius":
                                self.radius=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="y":
                                self.y=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="x":
                                self.x=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="center_y":
                                self.center_y=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="center_x":
                                self.center_x=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="new_y":
                                self.new_y=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="new_x":
                                self.new_x=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="shift":
                                self.shift=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="dist":
                                self.dist=self.return_numeric_value(data[1])
                                time.sleep(2)
                            elif data[0]=="line":
                                if self.time is None:
                                    self.time=4
                                self.draw_line(socket,[self.return_numeric_value(data[1]),self.return_numeric_value(data[2])],self.return_numeric_value(data[3]))
                            elif data[0]=="circ":
                                if self.time is None:
                                    self.time=4
                                self.draw_circle_arc(socket,[self.return_numeric_value(data[1]),self.return_numeric_value(data[2])],[self.return_numeric_value(data[3]),self.return_numeric_value(data[4])],[self.return_numeric_value(data[5]),self.return_numeric_value(data[6])],self.return_numeric_value(data[-1]))
            except FileNotFoundError as error:
                print(error)
            self.call_when_closing_connection()
        else:
            self.call_when_closing_connection()
    def draw_line(self,socket,to:list,z):
        print(f"movel(p[{str(to[0])},{str(to[1])}, {str(z)}, 2.24, -2.24, 0.00], a=1.0, v=0.04)")
        socket.send(bytes(f"movel(p[{str(to[0])},{str(to[1])}, {str(z)}, 2.24, -2.24, 0.00], a=1.0, v=0.04)"+"\n","utf-8"))
        time.sleep(self.time)
        self.listen(socket)
    def draw_circle_arc(self,socket,move_from:list,through:list,to:list,z):
        radius=self.distance_for_radius(move_from,to)
        print(f"movep(p[{str(to[0])}, {str(to[1])}, {str(z)}, 3.14, 0.0, 0.00], a=1.0, v=0.02,r={str(radius+0.005)})")
        print(f"movec(p[{str(through[0])}, {str(through[1])}, {str(z)}, 3.14, 0.0, 0.00],p[{str(to[0])}, {str(to[1])}, {str(z)}, 3.14, 0.0, 0.00], a=1.0, v=0.02,r=0,mode=0)")
        radius=self.distance_for_radius(move_from,to)
        socket.send(bytes(f"movep(p[{str(to[0])}, {str(to[1])}, {str(z)}, 3.14, 0.0, 0.00], a=1.0, v=0.02,r={str(radius+0.005)})"+"\n","utf-8"))
        time.sleep(self.time)
        socket.send(bytes(f"movec(p[{str(through[0])}, {str(through[1])}, {str(z)}, 3.14, 0.0, 0.00],p[{str(to[0])}, {str(to[1])}, {str(z)}, 3.14, 0.0, 0.00], a=1.0, v=0.02,r=0,mode=0)"+"\n","utf-8"))
        time.sleep(self.time)
        self.listen(socket)
    def distance_for_radius(self,x:list,y:list):
        dist_x=x[1]-x[0]
        dist_y=y[1]-y[0]
        dist=sqrt(pow(dist_x,2)+pow(dist_y,2))
        return dist
    def return_numeric_value(self,data:str):
        if "-" in data:
            splitted_d=data.split("-")
            if splitted_d[0]=="":
                return (-1)*float(splitted_d[1])
            else:
                return_val=None
                for s in splitted_d:
                    s=s.replace("(","")
                    s=s.replace(")","")
                    if "*" in s:
                        splitted_s=s.split("*")
                        v_1=splitted_s[0]
                        v_2=splitted_s[1]
                        s=((self.get_value(v_1))*(self.get_value(v_2)))
                    else:
                        s=self.get_value(s)
                    if return_val is None:
                        return_val=s
                    else:
                        return_val=return_val-s
                return return_val
        elif "+" in data:
            splitted_d=data.split("+")
            return_val=None
            for s in splitted_d:
                s=s.replace("(","")
                s=s.replace(")","")
                if "*" in s:
                    splitted_s=s.split("*")
                    v_1=splitted_s[0]
                    v_2=splitted_s[1]
                    s=((self.get_value(v_1))*(self.get_value(v_2)))
                else:
                    s=self.get_value(s)
                if return_val is None:
                    return_val=s
                else:
                    return_val=return_val+s
            return return_val
        elif "*" in data:
            data=data.replace("(","")
            data=data.replace(")","")
            splitted_d=data.split("*")
            v_1=splitted_d[0]
            v_2=splitted_d[1]
            data=((self.get_value(v_1))*(self.get_value(v_2)))
            return data
        else:
            return self.get_value(data)
    def get_value(self,value_for:str):
        if value_for=="time":
            return self.time
        if value_for=="radius":
            return self.radius
        elif value_for=="y":
            return self.y
        elif value_for=="x":
            return self.x
        elif value_for=="center_y":
            return self.center_y
        elif value_for=="center_x":
            return self.center_x
        elif value_for=="new_y":
            return self.new_y
        elif value_for=="new_x":
            return self.new_x
        elif value_for=="shift":
            return self.shift
        elif value_for=="dist":
            return self.dist
        else:
            if "/" in value_for:
                splitted=value_for.split("/")
                if splitted[0].isnumeric():
                    return_1=float(splitted[0])
                elif "sqrt" in splitted[0]:
                    splitted[0]=splitted[0].replace("sqrt","")
                    return_1=sqrt(float(splitted[0]))
                else:
                    return_1=self.get_value(splitted[0])
                if splitted[1].isnumeric():
                    return_2=float(splitted[1])
                else:
                    return_2=self.get_value(splitted[1])
                return (return_1/return_2)
            elif value_for!='':
                return float(value_for)
    def listen(self,socket):
        data=socket.recv(1024)
        #print("Received:\n",repr(data))
    def call_when_closing_connection(self):
        print("Closing connection...")
        self.socket.close()
def create_args():
    parser=argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '-file',
        '--file',
        type=str,
        required=True,
        help="The name of the file that contains coordinates for movements"
    )
    return parser

if __name__=="__main__":
    tcp_client=TCP_Client("10.150.1.1",30002)
    parser=create_args()
    args=parser.parse_args()
    print ("Starting Program...")
    try:
        tcp_client.draw(args.file)
    except socket.error as socketerror:
        print("An error has occured: "+str(socketerror))
    print ("Status data received from robot")