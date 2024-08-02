from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import threading

from collections import deque


api_key = ''
api_base = ''

class History:
    def __init__(self, max_save_round):
        self.max_save_round = max_save_round
        self.history = deque(maxlen=self.max_save_round)  # 设置最大长度，自动丢弃旧记录
    
    def get_from_list(self, lst):
        for item in lst[:-1]:
            if item['type'] == 'request':
                self.history.append({'role': 'user', 'content': item['content']})
            else:
                self.history.append({'role': 'assistant', 'content': item['content']})


    def save_history(self, role, content):
        # 存储一条消息到历史记录中
        self.history.append({'role': role, 'content': content})
    
    def clear_history(self):
        # 清除所有历史记录
        self.history.clear()

    def get_histories(self, n=None):
        # 获取最后n条历史记录，如果n没有指定或大于当前历史记录数，则返回所有记录
        n = n if n is not None and n < len(self.history) else len(self.history)
        return list(self.history)[-n:]
    

    def append_to_last_history(self, increment):
        # 检查历史记录是否为空
        if not self.history:
            raise IndexError("No history to append to.")
        
        # 获取最后一条历史记录
        last_record = self.history[-1]
        
        # 将增量追加到最后一条记录的内容中
        last_record['content'] += increment
        
        # 更新历史记录中的最后一条记录（由于deque中的对象是mutable的，所以这步实际上是可选的）
        self.history[-1] = last_record




# 定义调用GPT模型的参数
model = "gpt-4-0125-preview"
temperature = 0.8  # 设置创造性/随机性，范围从0到1
max_tokens = 8000  # 设置最大的token数
# prompt = "Translate the following English text to French: '{}'"  # 设置提示文本

n = 1  # 生成回应的数量
stop = ["\n"]  # 设置停止符
context_length = None  # 上下文长度，一般由模型自动管理

history_rounds = 20


client = OpenAI(api_key=api_key, base_url=api_base)


def get_answer(client, history, system_prompt, user_prompt, printing=True, save=True):
    '''
        user_prompt和system_prompt都是字符串！
    '''
    stream = client.chat.completions.create(
        model = model,
        messages=[{'role': "system", 'content': system_prompt},
         *history.get_histories(history_rounds), 
         {'role': "user", 'content': user_prompt}],
        stream=True,
    )
    answer = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer += chunk.choices[0].delta.content
            if printing==True:
                print(chunk.choices[0].delta.content, end="")
    if save == True:
        history.save_history('user', user_prompt)
        history.save_history('assistant', answer)
    return answer
# history.get_histories()

def get_answer_generator(client, history, system_prompt, user_prompt, printing=True):
    stream = client.chat.completions.create(
        model=model,
        messages=[{'role': "system", 'content': system_prompt},
                  *history.get_histories(history_rounds), 
                  {'role': "user", 'content': user_prompt}],
        stream=True,
    )
    print(*history.get_histories(history_rounds))
    answer = ''
    history.save_history('user', user_prompt)
    # print(history.get_histories(1))
    history.save_history('assistant', answer)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            history.append_to_last_history(chunk.choices[0].delta.content)
            if printing == True:
                print(chunk.choices[0].delta.content, end='')
            yield chunk.choices[0].delta.content


def get_answer_single(client, system_prompt, user_prompt, printing=False):
    '''
        user_prompt和system_prompt都是字符串！
    '''
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': "system", 'content': system_prompt},
                  {'role': "user", 'content': user_prompt}],
        stream=False,
    )
    answer = response.choices[0].message.content
    if printing:
        print(answer)
    return answer

def get_answers_parallel(client, system_prompt, user_prompt, n=1, printing=False):
    answers = []
    print_lock = threading.Lock()

    def get_and_print_answer():
        answer = get_answer_single(client, system_prompt, user_prompt, printing=False)
        if printing:
            with print_lock:
                print(answer)
        return answer

    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(get_and_print_answer) for _ in range(n)]
        for future in futures:
            # 结果将保持原始提交顺序
            answers.append(future.result())

    return answers
