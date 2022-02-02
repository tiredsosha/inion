import yaml
import os
import asyncio
import socket

from aiohttp import web

from raspberry.udp_client import send_udp


class Handler:
    def __init__(self):
        pass

    async def send_udp(self, ip: str, command: str):
        byte_message = bytes(command, "utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (ip, 8009))
        opened_socket.close()

    async def index(self, request):
        with open('home/pi/kek/configs/index.html', encoding="utf8") as html:
            html = html.read()
        return web.Response(text=html, content_type='text/html')

    async def pc(self, request):
        with open('home/pi/kek/configs/pc.html', encoding="utf8") as html:
            html = html.read()
        return web.Response(text=html, content_type='text/html')

    async def wake(self, request):
        await [
            send_udp(ip, 'wake')
            for ip in ('172.16.107.210', '172.16.107.211', '172.16.107.212')
        ]
        return web.Response(text="отрабатываю сцеририй выключения")

    async def sleep(self, request):
        await [
            send_udp(ip, 'sleep')
            for ip in ('172.16.107.210', '172.16.107.211', '172.16.107.212')
        ]
        return web.Response(text="отрабатываю сцеририй включения")

    async def comps(self, request):
        command = str(await request.text()).split('=')
        timeline_ip = command[1].split('&')[0]
        tree_ip = command[2].split('&')[0]
        world_ip = command[3]

        async def change_ip():
            with open('home/pi/kek/configs/pc.yaml', 'w') as pc:
                ips = {
                    'timeline': timeline_ip,
                    'tree': tree_ip,
                    'world': world_ip
                }
                print(ips)
                yaml.dump(ips, pc, default_flow_style=False)

        await change_ip()
        os.system("sudo shutdown -r +2")

        return web.Response(text='Изменения ip у компов внесены')

    async def data(self, request):
        command = str(await request.text()).split('=')
        wake_h = int(command[1].split('&')[0]) - 3
        wake_m = command[2].split('&')[0]
        sleep_h = int(command[3].split('&')[0]) - 3
        sleep_m = command[4]

        async def rewrite():
            with open('home/pi/kek/configs/wake.yaml', 'w') as wake:
                wake_t = {'hours': wake_h, 'mins': wake_m}
                yaml.dump(wake_t, wake, default_flow_style=False)
            with open('home/pi/kek/configs/sleep.yaml', 'w') as sleep:
                sleep_t = {'hours': sleep_h, 'mins': sleep_m}
                yaml.dump(sleep_t, sleep, default_flow_style=False)

        await rewrite()

        os.system("sudo shutdown -r +2")

        return web.Response(
            text='Хорошо, в течении 10 минут изменения применятся!')


def main():
    handle = Handler()

    app = web.Application()
    app.add_routes([
        web.get('/config', handle.index),
        web.get('/pc', handle.pc),
        web.get('/wake', handle.wake),
        web.get('/sleep', handle.sleep),
        web.post('/config', handle.data),
        web.post('/pc', handle.comps)
    ])
    web.run_app(app)


if __name__ == '__main__':
    main()