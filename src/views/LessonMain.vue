<template>
    <div id="app">
        <div class="nav">
            <el-breadcrumb separator=">">
                <el-breadcrumb-item :to="{ path: '/' }"><img class="icon" src="~@/assets/home.png" /></el-breadcrumb-item>
                <el-breadcrumb-item>课程创建</el-breadcrumb-item>
                <el-breadcrumb-item>大纲编辑</el-breadcrumb-item>
                <el-breadcrumb-item>教案编辑</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row class="row-container">
            <el-col :span="16" class="column-container">
                <div class="edit-column">
                    <!-- <v-md-editor v-model="lesson_outline_markdown" height="800px"></v-md-editor> -->
                    <el-container>
                        <el-header>
                            <el-button type="primary" @click='generateAllLessonPlans'
                                style="margin-bottom: 20px; margin-top: 30px;">生成全部教案</el-button>
                            <el-button type="primary" @click='loadSectionsFromLocalStorage'
                                style="margin-bottom: 20px; margin-top: 30px;">测试模式：载入教案。</el-button>
                        </el-header>
                        <div v-for="(section, index) in lesson_sections" :key="index">
                            <div v-if="!section.editing" @dblclick="toggleEdit(index)">
                                <v-md-preview :text="section.text"></v-md-preview>
                            </div>
                            <div v-else class="editor-container">
                                <v-md-editor v-model="section.text"></v-md-editor>
                                <div style="text-align: right;">
                                    <el-button @click="saveEdit(index)" type="primary"
                                        style="margin-bottom: 20px; margin-top: 30px;">确定修改</el-button>
                                </div>
                            </div>
                        </div>
                    </el-container>
                    <!-- 双击后进行编辑！ -->

                </div>
            </el-col>
            <el-col :span="8" class="column-container">
                <div class="gpt-column">
                    <el-container>
                        <el-header>
                            <el-row type="flex" justify="center">
                                <el-col :span="24">
                                    <h2>
                                        <el-icon><i class="fa fa-optin-monster fa-lg" aria-hidden="true"></i></el-icon>
                                        ChatGPT-website
                                    </h2>
                                </el-col>
                            </el-row>
                        </el-header>

                        <el-main>
                            <el-row type="flex" justify="center">
                                <el-col :span="24">
                                    <h4 class="text-center">欢迎！更多功能请点击下方设置按钮</h4>
                                    <!-- <img src="../static/images/reward.png" alt="reward"> -->
                                </el-col>
                            </el-row>
                            <!-- <div id="chatWindow" class="chat-window"></div> -->
                            <div class="chat-window" ref="chatWindow">
                                <div v-for="message in messages" :key="message.id" class="message-bubble"
                                    :class="{ 'sender': message.type === 'request', 'receiver': message.type === 'response' }">
                                    <!-- 对于接收的消息，头像显示在左边 -->
                                    <el-icon v-if="message.type === 'response'" class="avatar">
                                        <user />
                                    </el-icon>
                                    <div class="message-content">
                                        <v-md-preview :text="message.content"></v-md-preview>
                                    </div>
                                    <!-- 对于发送的消息，头像显示在右边 -->
                                    <el-icon v-if="message.type === 'request'" class="avatar">
                                        <user />
                                    </el-icon>
                                </div>
                            </div>

                            <el-row class="chat-input-row">
                                <el-col :span="20">
                                    <el-input type="textarea" v-model="chatInput" placeholder="Message"
                                        class="chat-input"></el-input>
                                </el-col>
                                <el-col :span="4">
                                    <el-button type="primary" @click="sendMessage">发送</el-button>
                                </el-col>
                            </el-row>
                        </el-main>

                        <el-footer class="text-center">
                            <!-- “抢走工作的不会是AI,而是率先掌握AI能力的人”
                            <el-link :underline="false" href="https://blog.csdn.net/qq_57421630"
                                target="_blank">联系我</el-link>
                            <el-link :underline="false" href="https://gitee.com/aniu-666/chat-gpt-website"
                                target="_blank">项目地址</el-link> -->
                        </el-footer>
                    </el-container>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
// import axios from 'axios';
import VMdEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import createCopyCodePreview from '@kangc/v-md-editor/lib/plugins/copy-code/preview';
import createTipPlugin from '@kangc/v-md-editor/lib/plugins/tip/index';
import '@kangc/v-md-editor/lib/plugins/tip/tip.css';
// import '@kangc/v-md-editor/lib/style/preview.css';

import hljs from 'highlight.js';

// import axios from 'axios';
// import markdownit from 'markdown-it';

import { ElIcon } from 'element-plus';
import { User } from '@element-plus/icons-vue';

import fetchStream from '@/utils/fetchStream';


export default {
    components: {
        // 注册编辑器组件
        'v-md-editor': VMdEditor,
        'v-md-preview': VMdPreview,
        ElIcon,
        User,
    },
    data() {
        return {
            // ...其他数据...
            lesson_name: '',
            lesson_goal: '',
            lesson_content: '',
            lesson_theme: '',
            prompt_comm: ` `,
            lesson_outline_markdown: '', // 用于存储Markdown原始数据
            responses: '',
            response_time: '',

            // 分段相关
            lesson_sections: [],

            // Chat相关
            chatInput: '', // 用户输入的消息
            messages: [], // 聊天消息数组
            currentStreamingMessageIndex: null,
        };
    },
    beforeMount() {
        VMdEditor.use(githubTheme, {
            Hljs: hljs,
        });
        VMdPreview.use(githubTheme, {
            Hljs: hljs,
        });
        VMdPreview.use(createCopyCodePreview());
        VMdEditor.use(createTipPlugin());
        VMdPreview.use(createTipPlugin());


    },
    created() {
        this.lesson_name = localStorage.getItem('lesson_name');
        this.lesson_goal = localStorage.getItem('lesson_goal');
        this.lesson_content = localStorage.getItem('lesson_content');
        this.lesson_theme = localStorage.getItem('lesson_theme');
        this.lesson_description = localStorage.getItem('lesson_description');
        this.lesson_outline_markdown = localStorage.getItem('lesson_outline');
    },
    mounted() {
        this.splitMarkdownIntoSections();
        // this.loadSectionsFromLocalStorage();
    },
    methods: {
        async generateAllLessonPlans() {
            let promises = this.lesson_sections.map((section, index) => {
                // 检查索引，如果为0，则返回一个立即解决的Promise
                if (index === 0) {
                    return Promise.resolve();
                } else {
                    // 对于其他索引，正常调用generateLessonPlan函数
                    return this.generateLessonPlan(index);
                }
            });

            try {
                await Promise.all(promises);

                // 处理所有生成的结果
                // results 是一个数组，包含了每个 promise 的返回值
                this.lesson_sections.forEach((section, index) => {
                    // 假设有一个函数 saveSectionContent 负责实际的保存逻辑
                    this.saveEdit(index);
                })
            } catch (error) {
                console.error('生成过程中出现错误:', error);
            }
        },

        generateLessonPlan(index) {
            return new Promise((resolve, reject) => {
                const to_deliver = this.lesson_sections[index].text;
                const lines = this.lesson_sections[index].text.split('\n');
                // 然后，取前三行并加上一个额外的换行符
                // 如果不足三行，就取实际的行数
                const firstThreeLines = lines.slice(0, 3).join('\n') + '\n';
                // 将处理过的字符串赋值回去
                this.lesson_sections[index].text = firstThreeLines;
                fetchStream(
                    'http://localhost:8000/lesson-main/generate-lesson-plan/',
                    {
                        name: this.lesson_name,
                        theme: this.lesson_theme,
                        goal: this.lesson_goal,
                        content: to_deliver,
                        outline: this.lesson_outline_markdown
                    },
                    (chunk) => {
                        // 成功接收到数据块时的处理逻辑
                        // 根据你的需求处理 chunk
                        this.lesson_sections[index].text += chunk;
                    },
                    (error) => {
                        // 请求失败时的处理逻辑
                        console.error('请求失败:', error);
                        reject(error); // 用 reject 表示出现错误
                    },
                    () => {
                        // 请求结束时的处理逻辑
                        // 可能不需要特别处理
                        resolve();
                    }
                );
            });
        },
        async sendMessage() {
            if (!this.chatInput.trim()) return; // 如果输入为空则不执行任何操作

            const messageContent = this.chatInput.trim();

            // 将请求消息添加到 messages 数组
            this.messages.push({
                type: 'request',
                content: messageContent,
            });

            // 清空输入框
            this.chatInput = '';

            // 使用 fetchStream 发送请求并处理流式响应
            fetchStream(
                'http://localhost:8000/lesson-main/ask/', // URL
                {
                    name: this.lesson_name,
                    goal: this.lesson_goal,
                    histories: this.messages, // 假设我们只需要发送消息内容
                    theme: this.lesson_theme,
                    prompt: messageContent,
                    outline: this.lesson_outline_markdown
                },
                (chunk) => { // 成功接收到数据块时的处理逻辑
                    if (this.currentStreamingMessageIndex === null) {
                        // 这是当前消息的第一个数据块
                        const newMessage = {
                            type: 'response', // 假定流式响应为接收消息
                            content: chunk
                        };
                        this.messages.push(newMessage);
                        this.currentStreamingMessageIndex = this.messages.length - 1;
                    } else {
                        // 后续的数据块
                        this.messages[this.currentStreamingMessageIndex].content += chunk;
                        // 为了触发Vue的响应式更新，需要重新赋值
                        this.messages = [...this.messages];
                    }
                    this.scrollToBottom();
                },
                (error) => { // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                },
                () => { // onFinally: 流式响应结束
                    console.log('Stream finished');
                    this.currentStreamingMessageIndex = null; // 重置索引，为接收下一个消息做准备
                    // 可选：执行一些清理工作或通知用户
                }
            );
        },
        splitMarkdownIntoSections() {
            // 临时替换掉 "### " 防止被分割
            let tempMarkdown = this.lesson_outline_markdown.replace(/(### )/g, 'TEMP_H3_PLACEHOLDER');

            // 找到第一个 "## " 的位置
            let firstSectionIndex = tempMarkdown.indexOf('## ');

            // 如果存在前言，将其作为第一部分
            if (firstSectionIndex !== -1) {
                this.lesson_sections.push({ text: tempMarkdown.substring(0, firstSectionIndex), editing: false });
            }

            // 使用 "## " 将剩下的 markdown 文档分割为若干部分，并存入 lesson_sections 数组
            let remainingSections = tempMarkdown.substring(firstSectionIndex).split('## ');
            remainingSections.forEach(section => {
                if (section.trim() !== '') {
                    // 替换回 "### " 并添加到 sections 数组
                    let sectionText = '## ' + section.replace(/TEMP_H3_PLACEHOLDER/g, '### ');
                    this.lesson_sections.push({ text: sectionText, editing: false });
                }
            });
        },
        toggleEdit(index) {
            this.lesson_sections[index].editing = !this.lesson_sections[index].editing;
        },
        saveEdit(index) {
            // 根据你的逻辑保存编辑
            this.lesson_sections[index].editing = false;
            // 将lesson_sections存储到localStorage
            localStorage.setItem('lesson_sections', JSON.stringify(this.lesson_sections));
        },
        loadSectionsFromLocalStorage() {
            // 从localStorage加载lesson_sections
            const storedSections = localStorage.getItem('lesson_sections');
            if (storedSections) {
                this.lesson_sections = JSON.parse(storedSections);
            } else {
                // 如果localStorage中没有数据，可能需要初始化或执行其他操作
            }
        },

        scrollToBottom() {
            this.$nextTick(() => {
                const chatWindow = this.$refs.chatWindow;
                if (chatWindow) {
                    chatWindow.scrollTop = chatWindow.scrollHeight;
                }
            });
        }
    }
};






</script>



<style scoped>
@import url('../font-awesome/css/font-awesome.min.css');
@import url('../css/github-dark-dimmed.min.css');
@import url('../css/style.css');

.row-container {
    height: 100vh;
    /* Set the height of the row to fill the viewport */
    overflow: hidden;
    /* Prevent scrolling on the row */
}

.column-container {
    height: 100%;
    /* Set the height of the columns to fill the row */
    overflow-y: auto;
    /* Enable vertical scrolling within columns */
}

.edit-column,
.gpt-column {
    height: 100%;
    /* Set the height of the columns content */
    padding: 20px;
    /* Padding for the content */
    overflow-y: auto;
    /* Enable vertical scrolling within column content */
    margin: 0;
    font-family: sans-serif;
    line-height: 140%;
    background-color: var(--bg);
    color: var(--fg);
    display: flex;
    justify-content: center;
}






.chat-window {
    display: flex;
    flex-direction: column;
    padding: 10px;
    overflow-y: auto;
    max-height: 500px;
}

.message-bubble {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.sender {
    justify-content: flex-end;
}

.receiver {
    justify-content: flex-start;
}

.sender .message-content {
    order: 1;
    /* 发送者的消息内容排在前面 */
    background-color: #ebebeb;
}

.receiver .message-content {
    background-color: #d3d3d3;
}

.avatar {
    margin: 0 10px;
}

.message-content {
    max-width: 60%;
    padding: 10px;
    border-radius: 15px;
    background-color: #f3f3f3;
}

/* Add your other styles here */
</style>