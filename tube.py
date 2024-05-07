import googleapiclient.discovery #pip install google-api-python-client
from datetime import datetime
from time import sleep


def get_channel_id(api_key, channel_identifier):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="id",
        type="channel",
        q=channel_identifier
    )
    try:
        response = request.execute()
    except:
        print('Лимит!')
        return 0
    if "items" in response and response["items"]:
        return response["items"][0]["id"]["channelId"]
    else:
        print(f"Не удалось найти канал с быстрым названием: {channel_identifier}")
        return None


def get_new_videos(api_key, channel_id, last_update_time, max_results=2):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    #if '@' in channel_id:
        #channel_id = get_channel_id(api_key, channel_id[1:])
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    video_ids = [item["id"]["videoId"] for item in response["items"]]

    videos_request = youtube.videos().list(
        part="snippet",
        id=",".join(video_ids)
    )

    videos_response = videos_request.execute()
    mas = []
    mas_time = [last_update_time]
    for video in videos_response["items"]:
        mas_rep = []
        title = video["snippet"]["title"] #Название видео
        video_url = f"https://www.youtube.com/watch?v={video['id']}" # Ссылка на видео
        description = video["snippet"]["description"] # Описание ролика
        published_at_str = video["snippet"]["publishedAt"]
        channel_title = video["snippet"]["channelTitle"]  # Название канала
        published_at = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
        if last_update_time < published_at.timestamp():
            mas_rep.append(f"На канале {channel_title}")
            mas_rep.append(f"Новое видео: {title}")
            mas_rep.append(f"Ссылка: {video_url}")
            mas_rep.append(f"Дата публикации: {published_at}")
            mas_rep.append(f"Описание: {description}")
            mas_time.append(published_at.timestamp())
            #print(mas_rep)
        #print(f"Новое видео: {title}\nСсылка: {video_url}\nДата публикации: {published_at}\n")
            mas.append(mas_rep)
    return mas, max(mas_time)


def crutch(video_list, lenght):
    for i in range(5 - lenght):
        video_list.append(0)
    return video_list


def push_file():
    to_write_file = open('result.txt', 'w')
    return to_write_file


def push_file_help():
    to_write_file = open('task_help.txt', 'w')
    return to_write_file


def logs(last_update_time_dict,param_t):
    if param_t == 0: #Делаем считывание логов
        f = open('logs.txt')
        last_update_time_dict_2 = {}
        for i in f:
            s_mas = i.split()
            key_for_dict = ' '.join(s_mas[0:len(s_mas)-1])
            last_update_time_dict_2[key_for_dict] = float((s_mas[-1]))
        return last_update_time_dict_2
    if param_t == 1: #Делаем запись логов
        f = open('logs.txt','w')
        mas = last_update_time_dict.keys()
        for i in mas:
            f.write(f"{i} ")
            f.write(str(last_update_time_dict[i]))
            f.write('\n')


def get_url(channel_url):
    #api_key = '' #Апи ключ от гугла
    channel_url = get_channel_id(api_key, channel_url[1:])
    return channel_url


def read_file():
    Channel = {}
    last_update_time_dict = {}
    try:
        f = open('task_help.txt')
        for i in f:
            s_mas = i.split()
            channel_url = s_mas[-1]
            name_channel = ' '.join(s_mas[0:len(s_mas) - 2])
            Channel[name_channel] = channel_url
            print(f"{name_channel}")
            last_update_time_dict[name_channel] = 0
            #print(1)
        f.close()
    except:
        f = open('task.txt')
        task_help = open('task_help.txt','w')
        for i in f:
            s_mas = i.split()
            channel_url = i.split('/')[-1]
            if '@' in channel_url:
                channel_url = get_channel_id(api_key, channel_url[1:])
            channel_url = channel_url.rstrip()
            print(channel_url)
            name_channel = ' '.join(s_mas[0:len(s_mas) -1])
            Channel[name_channel] = channel_url
            last_update_time_dict[name_channel] = 0
            task_help.write(f"{name_channel} ")
            task_help.write(s_mas[-1])
            task_help.write(f" {channel_url}\n")
        task_help.close()
        #sleep(60)
    return Channel, last_update_time_dict


def add(string_for_write): #NameChannel URL
    f = open('task_help.txt') #Открываю файл
    mas = list(map(str, f.readlines()))
    mas.append(string_for_write)
    f.close()
    f = open('task_help.txt','w')
    for i in mas:
        f.write(i.rstrip())
        f.write('\n')
    f.close()
    f = open('logs.txt')  # Открываю файл
    mas = list(map(str, f.readlines()))
    mas.append(string_for_write)
    f.close()
    mas_for_write = string_for_write.split(" ")
    print(mas_for_write)
    name_channel = ' '.join(mas_for_write[0:len(mas_for_write) - 2]) + ' 0'
    print(name_channel)
    f = open('logs.txt')
    mas2 = list(map(str,f.readlines()))
    mas2.append(name_channel)
    f = open('logs.txt', 'w')
    for i in mas2:
        f.write(i.rstrip())
        f.write('\n')
    f.close()


def delete_elem(string_for_delete):
    f = open('task_help.txt') #Открываю файл
    mas = list(map(str, f.readlines()))
    mas.append(string_for_delete)
    f.close()
    f = open('task_help.txt','w')
    for i in mas:
        if string_for_delete not in i:
            f.write(i.rstrip())
            f.write('\n')
    f.close()
    f = open('logs.txt')  # Открываю файл
    mas = list(map(str, f.readlines()))
    f.close()
    f = open('logs.txt','w')  # Открываю файл
    for i in mas:
        if string_for_delete not in i:
            f.write(i.rstrip())
            f.write('\n')
    f.close()


def display_list():
    f = open('task_help.txt') #Открываю файл
    mas_task_help = list(map(str, f.readlines()))
    f.close()
    return mas_task_help


def main():
    # API ключ v3 https://developers.google.com/youtube/v3/getting-started?hl=ru
    #YouTube Data API v3
    global api_key
    api_key = '' #апи ключ в гугле


    # Список каналов
    Channel, last_update_time_dict = read_file()
    count = 0
    to_write_file = open("result.txt",'w',encoding = 'utf-16')
    last_update_time_dict = logs(last_update_time_dict, 0)
    for i in Channel.keys():
        last_update_time = last_update_time_dict[i]
        channel_id = Channel[i]
        lightshockchannel,last_update_time = get_new_videos(api_key, channel_id, last_update_time)
        last_update_time_dict[i] = last_update_time
        print('-------------------')
        if len(lightshockchannel) > 0:
            #[print(*dis,'\n','------------------------','\n') for dis in lightshockchannel]
            #[to_write_file.write(j) for i in lightshockchannel for j in i]
            #print(lightshockchannel)
            for dis in lightshockchannel:
                for j in dis:
                    to_write_file.write(f"{j}\n")
                    #print('Записываю в файл')
                    #print(j)
                for count in range(5):
                    to_write_file.write('\n')
        else:
            print('Новых видео нету')
            print(last_update_time)
        #to_write_file.close()
        count+=1
        sleep(1) #Задержка между проверками, чтобы не влететь в минутный лимит
    last_update_time_dict = logs(last_update_time_dict, 1)
    to_write_file.close()
    #sleep(50) #Раз в сколько секунд проверять каналы

#main()