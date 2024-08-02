from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Optional, List

from gpt_method import *
from utils import convert_string

from fastapi.responses import StreamingResponse
from prompts import generate_lesson_plan_prompt, events_dict, generate_outline_prompt, eventPrompts, ask_prompt

history = History(50)
history_rounds = 20

app = FastAPI()

course_router = APIRouter(prefix="/lesson-create")  # 添加前缀/course
edit_router = APIRouter(prefix="/lesson-edit") 
main_router = APIRouter(prefix="/lesson-main") 



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://localhost:8080", "http://139.9.45.156:10245"],  # 允许的源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

class CourseName(BaseModel):
    name: str

class CourseGoal(BaseModel):
    name: str
    goal: str
    theme: str
    prompt: str
    lesson_type: str



# 同步生成器
# @course_router.post("/course-name/")
# async def receive_course_name(course_name: CourseName):
#     print(course_name.name)
#     usr_prompt = f"请你为{course_name.name}创建一个课程简介，大约100-150字。"
#     sys_prompt = "你是chat-gpt，一个基于gpt的课件制作助手，你要为公开课严肃地介绍我们的课程。不需要任何欢迎语，请科学、严谨地用维基百科的风格进行介绍"
#     return {"summary": get_answer(client, history, sys_prompt, usr_prompt, False)}

# 异步实现
@course_router.post("/course-name/")
def receive_course_name(course_name: CourseName):
    usr_prompt = f"请你为{course_name.name}创建一个课程简介，大约100-150字。"
    sys_prompt = "你是chat-gpt，一个基于gpt的课件制作助手，你要为公开课严肃地介绍我们的课程。不需要任何欢迎语，请科学、严谨地用维基百科的风格进行介绍"
    
    def generate_answer(history):
        # 直接调用同步的生成器函数
        for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(history), media_type="text/plain")


@course_router.post("/course-goal/")
async def receive_course_goal(course_goal: CourseGoal):
    # print(course_goal.goal)
    d = {"lesson_name": course_goal.name,
         "lesson_goal": course_goal.goal,
         "lesson_theme": course_goal.theme,
         "lesson_type": course_goal.lesson_type}
    usr_prompt = convert_string(d, course_goal.prompt)
    print(usr_prompt)
    sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture."
    # ans = get_answer(client, history, sys_prompt, usr_prompt, False)
    # print(ans)
    # return ans
    def generate_answer(history):
        # 直接调用同步的生成器函数
        for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(history), media_type="text/plain")


# EDIT页面

class CourseData(BaseModel):
    name: str
    goal: str
    content: str
    theme: str
    lesson_type: str
    # prompt: str

@edit_router.post("/generate-outline/")
async def receive_course_data(course_data: CourseData):
    d = {"lesson_name": course_data.name,
        "lesson_goal": course_data.goal,
        "lesson_theme": course_data.theme,
        "lesson_type": course_data.lesson_type}
    prompt = generate_outline_prompt
    usr_prompt = convert_string(d, prompt)
    print(usr_prompt)
    sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture."
    # ans = get_answer(client, history, sys_prompt, usr_prompt, False)
    # print(ans)
    def generate_answer(history):
        # 直接调用同步的生成器函数
        for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt, False):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(history), media_type="text/plain")
    # return {'outline': ans}


class ButtonRequest(BaseModel):
    buttonName: str
    name: str
    theme: str
    goal: str
    selection: str
    textArea: str
    outline: str
    prompt: str
    isUsePrompt: bool
    lesson_type: str
    histories: Optional[List]
    # prompt: str

@edit_router.post("/get-button-response/")
async def receive_course_data(button_request: ButtonRequest):
    d = {"lesson_name": button_request.name,
        "lesson_goal": button_request.goal,
        "lesson_theme": button_request.theme,
        "selection": button_request.selection,
        "text_area": button_request.textArea,
        "lesson_outline": button_request.outline,
        "prompt":button_request.prompt,
        "lesson_type": button_request.lesson_type
        }
    if button_request.isUsePrompt != True:
        prompt = eventPrompts[button_request.buttonName]
        his = History(10)
    else:
        prompt = button_request.prompt
        his = History(10)
        his.get_from_list(button_request.histories)
    usr_prompt = convert_string(d, prompt)
    print(usr_prompt)
    # print(his)
    # print(usr_prompt)
    sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture."
    # ans = get_answer(client, history, sys_prompt, usr_prompt, False)
    # print(ans)
    def generate_answer(history):
        # 直接调用同步的生成器函数
        for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt, False):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(his), media_type="text/plain")
    # return {'outline': ans}


class AskData(BaseModel):
    name: str
    goal: str
    content: str
    theme: str
    prompt: str
    outline: str
    answer_num: int


# @edit_router.post("/ask/")
# async def receive_course_data(ask_data: AskData):
#     d = {"lesson_name": ask_data.name,
#         "lesson_goal": ask_data.goal,
#         "lesson_theme": ask_data.theme,
#         "lesson_outline": ask_data.outline}
#     usr_prompt = convert_string(d, ask_data.prompt)
#     print(usr_prompt)
#     sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture. Please Response me in Markdown Format in every single response!"
#     ans = get_answers_parallel(client, sys_prompt, usr_prompt, ask_data.answer_num)
#     print(ans)
#     return {'responses': ans}


# Main的定义

class RequestData(BaseModel):
    name: str
    goal: str
    theme: str
    prompt: str
    outline: str
    textArea: str
    lesson_type:str
    # answer_num: Optional[int] = 1  # 使answer_num变为可选，并默认为None
    histories: List  # 等同于list[str]，只是另一种写法
    # question: Optional[str]


class OutlineData(BaseModel):
    name: str
    goal: str
    theme: str
    content: str
    outline: str


@edit_router.post("/ask/")
def receive_question(request: RequestData):
    d = {"lesson_name": request.name,
    "lesson_goal": request.goal,
    "lesson_theme": request.theme,
    "lesson_outline": request.outline,
    "text_area": request.textArea,
    "prompt": request.prompt,
    "lesson_type": request.lesson_type,
    }
    usr_prompt = convert_string(d, ask_prompt)
    sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture."
    his = History(15)
    print(request.histories)
    his.get_from_list(request.histories)
    
    def generate_answer(history):
        # 直接调用同步的生成器函数
        # for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt, False):
        for chunk in get_answer_generator(client, history, sys_prompt, request.prompt, False):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(his), media_type="text/plain")



@edit_router.post("/generate-lesson-plan/")
def generate_lesson_plan(request: OutlineData):
    d = {"lesson_name": request.name,
    "lesson_goal": request.goal,
    "lesson_theme": request.theme,
    "lesson_content": request.content,
    "lesson_outline": request.outline
    }
    prompt = generate_lesson_plan_prompt
    # 直接取第二行，将事件提取出来
    events_list = ['{' + x.strip() + '}\n' for x in request.content.split('\n\n')[1][3:].split(' & ')]
    events = ''.join(events_list)
    # print(events)
    prompt = convert_string(d, prompt)
    prompt = convert_string({"lesson_events": events}, prompt)
    usr_prompt = convert_string(events_dict, prompt)
    print(usr_prompt)
    sys_prompt = "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4-preview architecture."
    his = History(10)
    # print(request.histories)
    # his.get_from_list(request.histories)
    def generate_answer(history):
        # 直接调用同步的生成器函数
        for chunk in get_answer_generator(client, history, sys_prompt, usr_prompt, True):
            yield (chunk).encode("utf-8")  # 编码为字节流
    return StreamingResponse(generate_answer(his), media_type="text/plain")


app.include_router(course_router)
app.include_router(edit_router)
app.include_router(main_router)

# 设置静态文件服务


# app.mount("/css", StaticFiles(directory="css"), name="css")
# app.mount("/img", StaticFiles(directory="img"), name="img")
# app.mount("/js", StaticFiles(directory="js"), name="js")
# app.mount("/", StaticFiles(directory="/"), name="/")

if __name__ == "__main__":
    import uvicorn
    # 设置 host='127.0.0.1' 表示服务运行在本地，port=8000 指定端口为 8000。
    # log_level="info" 设置日志等级为信息级别，reload=True 在开发时启用自动重载。
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, log_level="info", reload=True)