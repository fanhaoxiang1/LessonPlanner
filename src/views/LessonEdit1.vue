<!-- src/views/lesson_edit.vue -->

<template>
    <div id="app">
        <el-container @click="handleContainerClick">
            <el-header height="50px">
                <div>
                    <img class="logo" src="~@/assets/icon.svg" />
                </div>
                <!-- 面包屑导航（Element Plus组件） -->
                <div class="nav">
                    <el-breadcrumb separator=">">
                        <el-breadcrumb-item :to="{ path: '/' }"><img class="icon"
                                src="~@/assets/home.png" /></el-breadcrumb-item>
                        <el-breadcrumb-item>课程创建</el-breadcrumb-item>
                        <el-breadcrumb-item>大纲编辑</el-breadcrumb-item>
                    </el-breadcrumb>
                </div>
            </el-header>
            <el-main style="padding-bottom: 0; padding-top: 0;">
                <el-container @click="handleContainerClick">,
                    <el-main style="height: calc(98vh - 60px); padding-bottom: 0 20px 0 0; margin: 0 20px 0 20px;">
                        <!-- <div class="content">
                        <p class="bdg">inqury based learning</p>
                        <h2>{{lesson_name}}</h2>
                        <P>{{lesson_description}}</P>
                        <hr /> -->
                        <br />
                        <p>课程目标描述</p>
                        <div>
                            <el-input v-model="lesson_goal" type="textarea" :rows="11" placeholder="Please input" />
                        </div>
                        <!-- <p>课程内容描述（TODO 暂无影响）</p>
                    <div>
                        <el-input v-model="lesson_content" type="textarea" :rows="6" placeholder="Please input" />
                    </div> -->
                        <div style="margin: 20px 0;float: left;">
                            <el-popconfirm title="你确定要生成吗？" @confirm="generateOutline">
                                <template #reference>
                                    <el-button type="primary">生成本节课的教案大纲</el-button>
                                </template>
                            </el-popconfirm>
                        </div>
                        <!-- <p>TOEFL to be soon offered as personalised test based on individual backgrounds, requirements:
                            ETS</p> -->
                        <!-- <ul>
                            <li>TOEFL to be soon offered as personalised test based on individual <span class="bdg"
                                    style="font-size: 14px;padding: 6px;">Understand</span> </li>
                            <li>TOEFL to be soon offered as personalised test based on individual <span class="bdg"
                                    style="font-size: 14px;padding: 6px;">Apply</span> </li>
                            <li>TOEFL to be soon offered as personalised test based on individual <span class="bdg"
                                    style="font-size: 14px;padding: 6px;">Applyxxx</span> </li>
                            <li>TOEFL to be soon offered as personalised test based on individual <span class="bdg"
                                    style="font-size: 14px;padding: 6px;">Windows</span> </li>

                        </ul> -->


                        <hr style="margin: 80px 0 0 0;" />


                        <!-- <h2>Prompt调节</h2>
                    <p>Prompt内容，课程名称用{lesson_name}代替，课程关于用{lesson_theme}代替，课程目标用{lesson_goal}代替，课程内容用{lesson_content}代替。
                    </p>

                    <div>
                        <el-input :rows="15" type="textarea" v-model="prompt_comm" />
                    </div> -->
                        <!-- <div style="display: flex; justify-content: flex-end; margin-bottom: 20px; margin-top: 10px;">
                        <el-button plain @click='generateOutline'>生成本节课的教案大纲</el-button>
                    </div> -->


                        <div class="banner">
                            请仔细检查！<br>
                            以下内容由大语言模型基于您提供的素材库生成，请您根据您的需求增删知识点或调整授课流程!
                            <br>
                        </div>
                        <!-- <div>
                        <p>{{ lesson_outline_time }}</p>
                    </div> -->
                        <!-- <div v-html="renderedMarkdown"></div> -->
                        <div>
                            <!-- 当不处于编辑模式时，显示渲染后的Markdown内容，并监听双击事件 -->
                            <!-- <div v-if="!editing" v-html="renderedMarkdown" @dblclick="toggleEdit"></div> -->
                            <!-- 使用v-md-editor库进行预览 -->
                            <!-- <div v-if="!editing" @dblclick="toggleEdit"> -->
                            <div v-for="(section, index_section) in lesson_outline_markdown_split_new"
                                :key="index_section">
                                <el-card shadow='hover'>
                                    <div v-for="(markdown, index) in section" :key="index" class="markdown-split">

                                        <!-- 当被忽略，且不是## ，则折叠。 -->
                                        <!-- 当 visibleIndex 不等于 index 时显示 v-md-preview 组件 -->
                                        <div v-if="visibleIndex[0] !== index_section || visibleIndex[1] !== index">
                                            <div @click="handleMarkdownClick(index_section, index)">
                                                <div v-if="!ignoreContent[index_section] || markdown.startsWith('## ')">
                                                    <v-md-preview :text="markdown" class="v-md-preview-class">
                                                    </v-md-preview>
                                                </div>
                                            </div>
                                            <div v-if="markdown.startsWith('## ')" class="menu-after-h2">
                                                <div>
                                                    <!-- 1. 隐藏/打开模块 -->
                                                    <el-switch v-model="ignoreContent[index_section]"
                                                        active-color="#ff4949" inactive-color="#13ce66"
                                                        :active-value="true" :inactive-value="false">
                                                    </el-switch>
                                                    <span>忽略该块内容</span>
                                                </div>
                                                <!-- <el-divider direction="vertical" v-if="!ignoreContent[index_section]" />
                                                <div v-if="!ignoreContent[index_section]">
                                                    <el-button-group>
                                                        <el-button icon="ArrowLeft">安排更少时间</el-button>
                                                        <el-button>
                                                            安排更多时间<el-icon>
                                                                <ArrowRight />
                                                            </el-icon>
                                                        </el-button>
                                                    </el-button-group>
                                                </div> -->
                                                <el-divider direction="vertical" />
                                                <el-button :type="buttonType[index_section]" icon="Check"
                                                    v-if="!ignoreContent[index_section]"
                                                    :loading="buttonLoading[index_section]"
                                                    @click="generateLessonPlan(index_section)">{{
            buttonText[index_section] }}</el-button>
                                            </div>
                                        </div>
                                        <!-- 当 visibleIndex 等于 index 时显示 v-md-editor 组件 -->
                                        <div v-else>
                                            <el-row>
                                                <el-col :span="21">
                                                    <v-md-editor
                                                        v-model="lesson_outline_markdown_split_new[index_section][index]"
                                                        mode="edit"
                                                        left-toolbar="undo redo | h bold italic | ul ol code | getSelection openAssistant save"
                                                        right-toolbar="preview" :toolbar="toolbar">
                                                    </v-md-editor>
                                                </el-col>
                                                <el-col :span="3">
                                                    <div class="button-column">
                                                        <el-button icon="ChatDotSquare" color='#79bbff'
                                                            v-if='!markdown.startsWith("## ")'
                                                            style="margin: 0 0 3px 5px"
                                                            @click="isAssistantOpen = !isAssistantOpen;">
                                                            <el-text size="small">打开教案助手</el-text>
                                                        </el-button>
                                                        <el-button icon="DocumentAdd" color='#e1f3d8'
                                                            style="margin: 0 0 3px 5px" plain
                                                            @click="insertParagraph(0, index_section, index)"
                                                            v-if='!markdown.startsWith("## ")'>
                                                            <el-text size="small">上方增加</el-text>
                                                        </el-button>

                                                        <el-button icon="Minus" color="#fde2e2"
                                                            v-if='!markdown.startsWith("## ")'
                                                            style="margin: 0 0 3px 5px" plain
                                                            @click="lesson_outline_markdown_split_new[index_section].splice(index, 1); visibleIndex = [-1, -1]">
                                                            <el-text size="small">移除该块</el-text>
                                                        </el-button>
                                                        <el-button icon="DocumentAdd" color="#e1f3d8"
                                                            v-if='!markdown.startsWith("## ")'
                                                            style="margin: 0 0 3px 5px" plain
                                                            @click="insertParagraph(1, index_section, index)">
                                                            <el-text size="small">下方增加</el-text>
                                                        </el-button>
                                                    </div>
                                                </el-col>
                                            </el-row>
                                        </div>
                                    </div>
                                </el-card>
                                <div style="margin-bottom: 10px;"></div>
                            </div>
                            <!-- </div> -->
                            <!-- 使用v-md-editor库 -->
                            <!-- <div v-else class="editor-container ">
                            <v-md-editor v-model="lesson_outline_markdown" height="800px"></v-md-editor>
                            <div style="text-align: right;">
                                <el-button @click="saveEdit" type="primary"
                                    style="margin-bottom: 20px; margin-top: 30px;">确定修改</el-button>
                            </div>
                        </div> -->
                        </div>
                        <div style="margin: 20px 0;float: right;">
                            <el-button type="primary" @click="downloadLessonPlan">下载教案</el-button>
                        </div>
                    </el-main>
                    <el-aside width="40%" style="height: 98vh; padding: 0;" v-if="isAssistantOpen">
                        <div>
                            <el-text size="large" tag="b">Lesson Plan Assistant</el-text>
                            <div style="margin-top: 10px">
                                <el-card shadow="hover" body-style="background-color: #e1f3d8;" style="width: 98%; ">
                                    <el-button v-for="(button, index) in generalButtons" :key="index"
                                        :class="['button-for-edit', button.icon]" @click="buttonClicked(button.name)"
                                        :color=button.color size="small">
                                        {{ button.name }}
                                    </el-button>
                                    <el-divider style="margin: 3px 0 5px 0;"></el-divider>
                                    <p style="padding-bottom: 10px; margin-bottom: 10px;">
                                        在此部分，您可能需要:
                                    </p>
                                    <!-- <el-row style="margin-bottom: 10px;"> -->
                                    <!-- <el-col :span="8"> -->
                                    <el-button v-for="(button, index) in buttons" :key="index"
                                        :class="['button-for-edit', button.icon]" @click="buttonClicked(button.name)"
                                        :color=button.color>
                                        {{ button.name }}
                                    </el-button>
                                    <!-- </el-col> -->

                                    <!-- <el-col :span="16"> -->
                                    <el-row>
                                        <el-col :span="5">
                                            <el-switch v-model="allowInput" style="margin-right: 10px;"></el-switch>
                                            <el-text size="small">我需要</el-text>
                                        </el-col>
                                        <el-col :span="18">
                                            <!-- Input -->
                                            <el-input v-model="askPrompt" :disabled="!allowInput"
                                                type="text"></el-input>
                                        </el-col>
                                        <el-col :span="1">
                                            <!-- Input -->
                                            <el-button type="info" icon="Select" circle @click="customedRequest(0)"
                                                :disabled="!allowInput" style="margin: 2px 2px 0px 3px" />
                                        </el-col>
                                    </el-row>
                                    <span> LLM outputs:</span>
                                    <div style="margin-bottom: 10px;"></div>
                                    <v-md-editor v-model="responseContent" :mode="isAssistantEditable"
                                        left-toolbar="undo redo clear| getSelection" right-toolbar="preview"
                                        :codemirrorConfig="{ lineNumbers: false }" :toolbar="toolbar" height="350px">
                                    </v-md-editor>
                                    <div v-if="responseContent != ''" style="margin: 20px 0 0 0;">
                                        <el-row>
                                            <el-col :span="4">
                                                <el-text size="small">继续提问：</el-text>
                                            </el-col>
                                            <el-col :span="18">
                                                <!-- Input -->
                                                <el-input v-model="moreQuestion" autosize type="textarea"></el-input>
                                            </el-col>
                                            <el-col :span="1">
                                                <!-- Input -->
                                                <el-button icon="Select" circle @click="sendMessage"
                                                    style="margin: 2px 2px 0px 3px" />
                                            </el-col>
                                        </el-row>
                                    </div>

                                    <div class="action-buttons">
                                        <el-button size="small" @click="copyText(responseContent)"
                                            style="margin-bottom: 10px;">复制</el-button>
                                        <!-- <el-button size="small" @click="sendMessage" style="margin-bottom: 10px;">重新生成</el-button> -->
                                        <br />
                                        <el-button size="small" @click="historyVisible = true">历史记录...</el-button>
                                        <el-button size="small" type="primary"
                                            @click="confirmAction">Confirm</el-button>
                                    </div>
                                    <!-- </el-col> -->
                                    <!-- </el-row> -->
                                    <!-- 其他内容 -->
                                </el-card>
                            </div>
                        </div>
                    </el-aside>
                </el-container>
            </el-main>
        </el-container>
        <div>
            <el-drawer v-model="historyVisible" title="历史记录" direction="ltr" size="20%" :modal="true"
                :before-close="popoverVisible = false">
                <main>
                    <el-popover :visible="popoverVisible" placement="right" width="500px" :offset="40">
                        <div>
                            <b>请求：</b><br />
                            {{ selectedHistory.request }}
                            <br />
                            <b>输出：</b><br />
                            {{ selectedHistory.response }}
                        </div><br />
                        <i>复制答案?</i>
                        <div style="text-align: right; margin: 0">
                            <el-button size="small" @click="popoverVisible = false">关闭</el-button>
                            <el-button size="small" type="primary"
                                @click="copyText(selectedHistory.response)">复制</el-button>
                        </div>
                        <template #reference>
                            <ul class="infinite-list" style="overflow: auto">
                                <li v-for="(history, index) in histories" :key="index" class="infinite-list-item"
                                    @mouseover="click_history(history)">
                                    {{ history.request }}
                                    <br />
                                    {{ history.time }}
                                </li>
                            </ul>
                        </template>
                    </el-popover>
                </main>
            </el-drawer>
        </div>
    </div>
</template>

<script>
// lesson_edit.js 的 JavaScript 内容
import axios from 'axios';


// import VMdEditor from '@kangc/v-md-editor';
// import '@kangc/v-md-editor/lib/style/base-editor.css';
// import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
// import '@kangc/v-md-editor/lib/theme/style/github.css';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';

import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn'
import VMdEditor from '@kangc/v-md-editor/lib/codemirror-editor';
import '@kangc/v-md-editor/lib/style/codemirror-editor.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
// import hljs from 'highlight.js';

// codemirror 编辑器的相关资源
import Codemirror from 'codemirror';
// mode
import 'codemirror/mode/markdown/markdown';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/css/css';
import 'codemirror/mode/htmlmixed/htmlmixed';
import 'codemirror/mode/vue/vue';
// edit
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/addon/edit/closetag';
import 'codemirror/addon/edit/matchbrackets';
// placeholder
import 'codemirror/addon/display/placeholder';
// active-line
import 'codemirror/addon/selection/active-line';
// scrollbar
import 'codemirror/addon/scroll/simplescrollbars';
import 'codemirror/addon/scroll/simplescrollbars.css';
// style
import 'codemirror/lib/codemirror.css';






import fetchStream from '@/utils/fetchStream';
import config from '../js/config.js';
import { ElMessage } from 'element-plus';


import hljs from 'highlight.js';

export default {
    components: {
        // 注册编辑器组件
        'v-md-editor': VMdEditor,
        'v-md-preview': VMdPreview,
    },
    data() {
        this.toolbar = {
            getSelection: {
                title: '设定为选中的上下文',
                icon: 'v-md-icon-quote', // 请根据实际情况选择一个合适的图标
                action(editor) {
                    let selectedText = editor.getCurrentSelectedStr();
                    if (selectedText === null) {
                        selectedText = '';
                    }
                    if (selectedText == '') {
                        ElMessage({
                            showClose: true,
                            message: '选择范围为空.',
                            type: 'warning',
                        })
                    }
                    else {
                        ElMessage({
                            showClose: true,
                            message: '成功设置选定范围.',
                            type: 'success',
                        })
                        this.selectedText = selectedText;
                    }
                }
            },
            openAssistant: {
                title: '打开教案助手',
                icon: 'v-md-icon-tip', // 请根据实际情况选择一个合适的图标
                action: () => {
                    this.isAssistantOpen = !this.isAssistantOpen;
                    this.isAssistantEditable = "preview";
                }
            },
            save: {
                title: '保存并退出该块',
                icon: 'v-md-icon-save', // 请根据实际情况选择一个合适的图标
                action: () => {
                    this.visibleIndex = [-1, -1];
                    // this.isAssistantOpen = false;
                    this.isAssistantEditable = "preview";
                    // this.messages = [];
                    // this.updateMarkdown();
                }
            },
            // selectAll: {
            //     title: '全选该块内容为上下文',
            //     icon: 'v-md-icon-open-in-new', // 请根据实际情况选择一个合适的图标
            //     action: (editor) => {
            //         this.selectedText = editor.text;
            //         if (this.selectedText == '') {
            //             ElMessage({
            //                 showClose: true,
            //                 message: '选择范围为空.',
            //                 type: 'warning',
            //             })
            //         }
            //         else {
            //             ElMessage({
            //                 showClose: true,
            //                 message: '成功设置选定范围.',
            //                 type: 'success',
            //             })
            //         }
            //     }
            // },
        };

        return {
            // ...其他数据...
            lesson_name: '',
            lesson_goal: '',
            lesson_content: '',
            lesson_theme: '',
            sliderValue: 3,
            prompt_comm: ``,
            lesson_description: '课程梗概显示在此……',
            lesson_outline_markdown: '', // 用于存储Markdown原始数据
            // lesson_outline_time: '课程大纲显示在此。',
            responses: '',
            response_time: '',
            editing: false,
            popoverContent: null,
            visibleIndex: [-1, -1],
            isAssistantOpen: false,
            radio: 0,
            generalButtons: config.generalMethods,
            selectedText: '',
            toolbar: this.toolbar,
            ignoreContent: null,
            collapseValue: "0",
            allowInput: false,
            askPrompt: '',
            responseContent: '',
            buttons: [],
            messages: [],
            histories: [],
            historyVisible: false,
            popoverVisible: false,
            selectedHistory: { 'request': '', "response": '' },
            moreQuestion: '', // 追问
            currentStreamingMessageIndex: null,
            buttonType: null,
            buttonLoading: null,
            buttonText: null,
            isAssistantEditable: 'preview',
            lesson_outline_original: '',
        };
    },
    computed: {
        lesson_outline_markdown_split: {
            get() {
                // 根据空行切分Markdown字符串，过滤掉只包含空白字符的段落
                return this.lesson_outline_markdown.split("\n\n").filter(paragraph => paragraph.trim() !== "");
            },
            set(value) {
                // 将切分后的Markdown段落数组合并回一个字符串
                this.lesson_outline_markdown = value.join("\n\n");
            }
        },
        lesson_outline_markdown_split_original: {
            get() {
                // 根据 "## " 切分 Markdown 字符串
                const lines = this.lesson_outline_original.split("\n\n");

                // 遍历每一行，检查是否以 "## " 开头
                let result = [];
                let currentSection = [];
                for (const line of lines) {
                    if (line.trim().startsWith("## ")) {
                        // 如果是新的 "## " 标题行，将当前 section 存入结果
                        if (currentSection.length > 0) {
                            result.push(currentSection);
                        }
                        currentSection = [];
                    }
                    currentSection.push(line);
                }

                // 将最后一个 section 存入结果
                if (currentSection.length > 0) {
                    result.push(currentSection);
                }

                // 过滤掉空白段落
                result = result.map(section => {
                    return section.filter(paragraph => paragraph.trim() !== "");
                });
                // console.log(this.lesson_outline_markdown);
                return result;
            },
            set(value) {
                // 将数组结构转换回 Markdown 字符串
                const markdownLines = [];
                for (const section of value) {
                    // 在每个 section 的每一行后面添加两个换行符
                    // 最后一个换行符将在 join 方法中添加
                    const sectionText = section.join("\n\n");
                    markdownLines.push(sectionText);
                }
                // 使用 join("\n\n") 来保证 section 之间有两个换行符
                // 这样在每个 section 之间就有了三个换行符，我们需要移除额外的一个
                this.lesson_outline_original = markdownLines.join("\n\n").replace(/\n{3,}/g, "\n\n").trim();
                // console.log(this.lesson_outline_original);
            }
        },


        lesson_outline_markdown_split_new: {
            get() {
                // 根据 "## " 切分 Markdown 字符串
                const lines = this.lesson_outline_markdown.split("\n\n");

                // 遍历每一行，检查是否以 "## " 开头
                let result = [];
                let currentSection = [];
                for (const line of lines) {
                    if (line.trim().startsWith("## ")) {
                        // 如果是新的 "## " 标题行，将当前 section 存入结果
                        if (currentSection.length > 0) {
                            result.push(currentSection);
                        }
                        currentSection = [];
                    }
                    currentSection.push(line);
                }

                // 将最后一个 section 存入结果
                if (currentSection.length > 0) {
                    result.push(currentSection);
                }

                // 过滤掉空白段落
                result = result.map(section => {
                    return section.filter(paragraph => paragraph.trim() !== "");
                });
                console.log(this.lesson_outline_markdown);
                return result;
            },
            set(value) {
                // 将数组结构转换回 Markdown 字符串
                const markdownLines = [];
                for (const section of value) {
                    // 在每个 section 的每一行后面添加两个换行符
                    // 最后一个换行符将在 join 方法中添加
                    const sectionText = section.join("\n\n");
                    markdownLines.push(sectionText);
                }
                // 使用 join("\n\n") 来保证 section 之间有两个换行符
                // 这样在每个 section 之间就有了三个换行符，我们需要移除额外的一个
                this.lesson_outline_markdown = markdownLines.join("\n\n").replace(/\n{3,}/g, "\n\n").trim();
                // console.log(this.lesson_outline_markdown);
            }
        }
    },
    beforeMount() {
        VMdEditor.Codemirror = Codemirror;
        VMdEditor.use(createKatexPlugin());
        VMdEditor.use(githubTheme, {
            Hljs: hljs,
        });
        VMdPreview.use(githubTheme, {
            Hljs: hljs,
        });
        window.addEventListener('beforeunload', this.handleBeforeUnload);
    },
    beforeUnmount() {
        window.removeEventListener('beforeunload', this.handleBeforeUnload);
    },
    created() {
        this.ignoreContent = Array(this.lesson_outline_markdown_split_new.length).fill(false);
        this.lesson_name = localStorage.getItem('lesson_name');
        this.lesson_goal = localStorage.getItem('lesson_goal');
        this.lesson_content = localStorage.getItem('lesson_content');
        this.lesson_theme = localStorage.getItem('lesson_theme');
        this.lesson_description = localStorage.getItem('lesson_description');
        if (localStorage.getItem('lesson_outline') !== null) {
            this.lesson_outline_original = localStorage.getItem('lesson_outline_original');
        }
        if (localStorage.getItem('lesson_outline') !== null) {
            this.lesson_outline_markdown = localStorage.getItem('lesson_outline');
        }
        if (localStorage.getItem("buttonType") !== null) {
            this.buttonType = JSON.parse(localStorage.getItem("buttonType"));
            this.buttonLoading = JSON.parse(localStorage.getItem("buttonLoading"));
            this.buttonText = JSON.parse(localStorage.getItem("buttonText"));
            this.ignoreContent = JSON.parse(localStorage.getItem("ignoreContent"));
        }
        console.log(this.lesson_outline_markdown_split_new);
        // this.add_history("What is the weather today?", "The weather is sunny");
        // 第二次调用
        // this.add_history("How do I get to the nearest subway station?", "Turn left at the next intersection, and it will be on your right");

        // alert(this.lesson_outline_markdown)
        // alert(this.lesson_name);
        // alert(this.lesson_goal);
    },
    methods: {
        handleBeforeUnload() {
            this.saveLessonPlan();
            localStorage.setItem('buttonType', JSON.stringify(this.buttonType));
            localStorage.setItem('buttonLoading', JSON.stringify(this.buttonLoading));
            localStorage.setItem('buttonText', JSON.stringify(this.buttonText));
            localStorage.setItem('ignoreContent', JSON.stringify(this.ignoreContent));
        },
        saveLessonPlan() {
            this.updateMarkdown();
            localStorage.setItem('lesson_outline', this.lesson_outline_markdown);
        },
        async copyText(text) {
            try {
                this.popoverVisible = false;
                await navigator.clipboard.writeText(text);
                this.$message({
                    showClose: true,
                    message: '复制成功！',
                    type: 'success',
                });
                this.historyVisible = false;
            } catch (err) {
                this.$message({
                    showClose: true,
                    message: '复制失败。',
                    type: 'error',
                });
            }
        },
        click_history(history) {
            this.selectedHistory = history;
            this.popoverVisible = true;
        },
        add_history(request, response) {
            const now = new Date();
            const time = now.getHours() + ':' + now.getMinutes().toString().padStart(2, '0');
            this.histories.unshift({
                request,
                response,
                time
            });
        },

        insertParagraph(mode, index_section, index) {    // 确保index_section在正确的范围内
            if (this.lesson_outline_markdown_split_new[index_section]) {
                if (mode === 0) {
                    // 在当前位置插入空字符串
                    this.lesson_outline_markdown_split_new[index_section].splice(index, 0, '');
                    // 更新visibleIndex
                    this.visibleIndex = [index_section, index];
                } else if (mode === 1) {
                    // 在下一个位置插入空字符串
                    this.lesson_outline_markdown_split_new[index_section].splice(index + 1, 0, '');
                    // 更新visibleIndex
                    this.visibleIndex = [index_section, index + 1];
                }
                // 这里可以添加更多模式的处理逻辑
            } else {
                console.error('Invalid section index:', index_section);
            }
        },
        customedRequest(x) {
            this.isAssistantEditable = 'preview';
            this.responseContent = '';
            this.messages = [];
            this.messages.push({
                type: 'response',
                content: "以下是我为您生成的此部分的教案：" + this.textAreaNow,
            });
            this.messages.push({
                type: 'request',
                content: "接下来我更关注的部分是：" + this.selectedText,
            });
            this.messages.push({
                type: 'response',
                content: "好的，我已知晓",
            });
            let prompt_to_send = this.askPrompt;
            if (x === 1) {
                prompt_to_send = "我想要重新生成，你只需要将我关注的部分重新生成即可，不要涉及任何超出此部分的内容。你只需要返还给我结果，不需要在这之前或之后有任何的提示。";
            }
            // alert(this.messages);
            fetchStream(
                'http://localhost:8000/lesson-edit/get-button-response/',
                {
                    buttonName: "重新生成",
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    goal: this.lesson_goal,
                    selection: this.selectedText,
                    textArea: this.textAreaNow,
                    outline: this.lesson_outline_markdown,
                    prompt: prompt_to_send,
                    isUsePrompt: true,
                    histories: this.messages,
                },
                (chunk) => {
                    // 成功接收到数据块时的处理逻辑
                    // 根据你的需求处理 chunk
                    this.responseContent += chunk;
                },
                (error) => {
                    // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                    this.responseContent = 'ERROR 请求失败';
                },
                () => {
                    this.add_history(this.askPrompt, this.responseContent);
                    // this.messages;
                    this.isAssistantEditable = 'edit';
                }
            );

        },
        updateMarkdown() {
            const markdownLines = [];
            for (const section of this.lesson_outline_markdown_split_new) {
                // 在每个 section 的每一行后面添加两个换行符
                // 最后一个换行符将在 join 方法中添加
                const sectionText = section.join("\n\n");
                markdownLines.push(sectionText);
            }
            // 使用 join("\n\n") 来保证 section 之间有两个换行符
            // 这样在每个 section 之间就有了三个换行符，我们需要移除额外的一个
            this.lesson_outline_markdown = markdownLines.join("\n\n").replace(/\n{3,}/g, "\n\n").trim();
            // console.log(this.lesson_outline_markdown);
        },


        handleContainerClick(event) {
            if (event.target === event.currentTarget) {
                // 直接点击了 el-container，设置 visibleIndex
                this.visibleIndex = [-1, -1];
            }
            // 如果点击的是子元素，则不执行任何操作
        },

        handleEditorBlur() {
            this.visibleIndex = [-1, -1];
            // this.isAssistantOpen = false;
            this.messages = [];
        },
        handleTextSelection() {
            // 假设 `getCurrentSelectedStr` 方法可以直接在 `v-md-editor` 实例上调用
            // alert('toggle');
            this.selectedText = this.getCurrentSelectedStr();

        },
        confirmAction() {
            // 确认操作
            // console.log("Confirm action for index", index);
            // this.visibleIndex = [-1, -1]; // 关闭Popover
            this.isAssistantOpen = false;
            this.messages = [];
        },
        cancelAction() {
            // 取消操作
            // console.log("Cancel action for index", index);
            // this.visibleIndex = [-1, -1]; // 关闭Popover
            this.isAssistantOpen = false;
            this.messages = [];
        },
        handleMarkdownClick(index_section, index) {
            this.textAreaNow = this.lesson_outline_markdown_split_new[index_section].join("\n\n");

            this.isAssistantEditable = 'preview';
            this.responseContent = '';
            const clickedContent = this.lesson_outline_markdown_split_new[index_section][index];
            this.selectedText = this.lesson_outline_markdown_split_new[index_section][index];
            const section = this.lesson_outline_markdown_split_new[index_section]
            // 构建并更新Popover的内容
            this.popoverContent = { Content: clickedContent, Section: section ? section.content : "" };

            // 调整按钮列表this.buttons: []
            // 如果config.sectionTypeToMethods中的一个key（字符串）在this.lesson_outline_markdown_split_new[index_section][1]（字符串）中
            // 就将config.sectionTypeToMethods[key]的方法加入到this.buttons中。
            this.buttons = [];
            const sectionType = this.lesson_outline_markdown_split_new[index_section][1]; // 假设章节类型在每个部分的第二个元素中
            for (const [key, methods] of Object.entries(config.sectionTypeToMethods)) {
                if (sectionType.includes(key)) {
                    // 对应方法名与generalMethods中的方法信息匹配，并加入到buttons中
                    methods.forEach(method => {
                        this.buttons.push(method);
                    });
                }
            }
            // 显示
            // 不允许显示### 这种
            if (!clickedContent.startsWith("### ")) {
                this.visibleIndex = [index_section, index];
                // this.isAssistantOpen = false;
            }
            else {
                this.visibleIndex = [-1, -1];
                // this.isAssistantOpen = false;
            }
        },

        async sendMessage() {
            this.isAssistantEditable = 'preview';
            if (!this.responseContent.trim()) return;
            const responsePart = this.responseContent;
            const requestPart = this.moreQuestion;

            // 如果存在 response 部分，将其添加到 messages 数组
            if (responsePart) {
                this.messages.push({
                    type: 'response',
                    content: responsePart,
                });
            }

            // 如果存在 request 部分，将其添加到 messages 数组
            if (requestPart) {
                this.messages.push({
                    type: 'request',
                    content: requestPart,
                });
            }

            // 清空输入框
            this.responseContent = '';

            // 使用 fetchStream 发送请求并处理流式响应
            fetchStream(
                'http://localhost:8000/lesson-edit/ask/', // URL
                {
                    name: this.lesson_name,
                    goal: this.lesson_goal,
                    theme: this.lesson_theme,
                    prompt: requestPart,
                    outline: this.lesson_outline_markdown,
                    textArea: this.textAreaNow,
                    histories: this.messages
                },
                (chunk) => { // 成功接收到数据块时的处理逻辑
                    this.responseContent += chunk;
                },
                (error) => { // 请求失败时的处理逻辑
                    this.responseContent = '请求失败:' + error;

                },
                () => { // onFinally: 流式响应结束
                    this.add_history(requestPart, this.responseContent);
                    this.isAssistantEditable = 'edit';
                }
            );
        },
        downloadLessonPlan() {
            const blob = new Blob([this.lesson_outline_markdown], { type: 'text/markdown;charset=utf-8' });
            // 创建一个指向该Blob的URL
            const url = URL.createObjectURL(blob);
            // 创建一个a元素用于触发下载
            const link = document.createElement('a');
            link.href = url;
            link.download = '我的教案.md'; // 文件名，你可以根据需要修改
            document.body.appendChild(link); // 需要添加到页面中去才能触发点击
            link.click(); // 模拟点击触发下载
            document.body.removeChild(link); // 下载后从页面中移除
            URL.revokeObjectURL(url); // 释放URL对象
        },
        buttonClicked(buttonName) {
            console.log('Button clicked:', buttonName);
            this.buttonResponse(buttonName);
            // 在这里处理点击事件，比如更新文本显示区域的内容
        },
        saveEdit() {
            // 保存编辑内容并退出编辑模式
            this.editing = false;
            localStorage.setItem('lesson_outline', this.lesson_outline_markdown);
            // 这里假设在退出编辑模式时保存，也可以根据需要调整
        },
        async buttonResponse(name) {
            if (name === '重新生成') {
                this.customedRequest(1);
                return;
            }
            this.isAssistantEditable = 'preview';
            this.responseContent = '';
            // console.log(this.selectedText);
            fetchStream(
                'http://localhost:8000/lesson-edit/get-button-response/',
                {
                    buttonName: name,
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    goal: this.lesson_goal,
                    selection: this.selectedText,
                    textArea: this.textAreaNow,
                    outline: this.lesson_outline_markdown,
                    prompt: this.askPrompt,
                    isUsePrompt: this.allowInput
                },
                (chunk) => {
                    // 成功接收到数据块时的处理逻辑
                    // 根据你的需求处理 chunk
                    this.responseContent += chunk;
                },
                (error) => {
                    // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                    this.responseContent = 'ERROR 请求失败';
                },
                () => {
                    this.add_history(name, this.responseContent);
                    // this.messages;
                    this.isAssistantEditable = 'edit';
                }
            );
        },

        async generateOutline() {
            this.lesson_outline_markdown = '';
            this.buttonType = Array(this.lesson_outline_markdown_split_new.length).fill('primary');
            this.buttonText = Array(this.lesson_outline_markdown_split_new.length).fill('根据大纲生成教案');
            this.buttonLoading = Array(this.lesson_outline_markdown_split_new.length).fill(true);
            fetchStream(
                'http://localhost:8000/lesson-edit/generate-outline/',
                {
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    goal: this.lesson_goal,
                    content: this.lesson_content,
                    // prompt: this.prompt_comm,
                    outline: this.lesson_outline_markdown,
                },
                (chunk) => { // 成功接收到数据块时的处理逻辑
                    this.buttonType = Array(this.lesson_outline_markdown_split_new.length).fill('primary');
                    this.buttonText = Array(this.lesson_outline_markdown_split_new.length).fill('根据大纲生成教案');
                    this.buttonLoading = Array(this.lesson_outline_markdown_split_new.length).fill(true);
                    this.lesson_outline_markdown += chunk;
                },
                (error) => { // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                    this.time_controller = '请求失败，请检查网络或重试。';
                },
                () => { // 请求结束时的处理逻辑
                    localStorage.setItem('lesson_outline', this.lesson_outline_markdown);
                    localStorage.setItem('lesson_outline_original', this.lesson_outline_markdown);
                    this.lesson_outline_original = this.lesson_outline_markdown;
                    this.buttonType = Array(this.lesson_outline_markdown_split_new.length).fill('primary');
                    this.buttonLoading = Array(this.lesson_outline_markdown_split_new.length).fill(false);
                    this.buttonText = Array(this.lesson_outline_markdown_split_new.length).fill('根据大纲生成教案');
                }
            );
        },
        delay(time) {
            return new Promise(resolve => setTimeout(resolve, time));
        },
        hasUnmatchedCodeBlocks(text) {
            // 使用正则表达式匹配所有的 ```
            const matches1 = text.match(/```/g);
            const matches2 = text.match(/\*/g);
            const matches3 = text.match(/\*\*/g);
            // 如果没有找到任何匹配项，表示没有未匹配的 ```
            if (!matches1 || !matches2 || matches3) {
                return false;
            }
            // 如果匹配项的数量是奇数，则表示有未匹配的 ```
            return matches1.length % 2 !== 0;
        },
        generateLessonPlan(sectionIndex) {
            this.buttonLoading[sectionIndex] = true;
            this.visibleIndex = [-1, -1];
            var sectionLines = this.lesson_outline_markdown_split_new[sectionIndex];
            var to_deliver = sectionLines.join('\n\n');
            // 清除第四个及其以后的内容
            this.lesson_outline_markdown_split_new[sectionIndex] = sectionLines.slice(0, 3);
            this.updateMarkdown();
            this.lesson_outline_markdown_split_new[sectionIndex].push('');
            let c = this.lesson_outline_markdown_split_new[sectionIndex].length;

            // 重新生成的请求：
            if (this.buttonType[sectionIndex] === 'success') {
                sectionLines = this.lesson_outline_markdown_split_original[sectionIndex];
                to_deliver = sectionLines.join('\n\n');
            }
            fetchStream(
                'http://localhost:8000/lesson-edit/generate-lesson-plan/',
                {
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    goal: this.lesson_goal,
                    content: to_deliver,
                    outline: this.lesson_outline_original
                },
                (chunk) => {
                    // 成功接收到数据块时的处理逻辑
                    // 根据你的需求处理 chunk
                    if (this.visibleIndex[0] == sectionIndex) {
                        this.visibleIndex = [-1, -1];
                    }
                    if (this.lesson_outline_markdown_split_new[sectionIndex][c - 1] === undefined) {
                        this.lesson_outline_markdown_split_new[sectionIndex][c - 1] = '';
                    }
                    // 强行更新响应。
                    if (!chunk.includes("\n") && !this.hasUnmatchedCodeBlocks(this.lesson_outline_markdown_split_new[sectionIndex][c - 1])) {
                        this.lesson_outline_markdown_split_new[sectionIndex][c - 1] += chunk;
                        this.updateMarkdown();
                    }
                    else {
                        if (!chunk.includes("\n\n")) {
                            this.lesson_outline_markdown_split_new[sectionIndex][c - 1] += chunk;
                        }
                        else {
                            // 切分开空格前后
                            const chunks = chunk.split("\n\n");
                            this.lesson_outline_markdown_split_new[sectionIndex][c - 1] += chunks[0];
                            this.lesson_outline_markdown_split_new[sectionIndex].push(chunks[1]);
                            c += 1;
                        }
                    }
                },
                (error) => {
                    // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                },
                () => {
                    // update一下。
                    this.updateMarkdown();
                    this.buttonLoading[sectionIndex] = false;
                    this.buttonType[sectionIndex] = 'success';
                    this.buttonText[sectionIndex] = '不满意，重新生成...';
                }
            );
        },



        goToMain() {
            // 设置目标路由的名称或路径
            const targetRoute = '/lesson-main';
            // 使用Vue Router进行导航
            this.$router.push(targetRoute);
        },
        async generateCommunication() {
            let elapsedTime = 0;
            this.response_time = `已耗时 ${elapsedTime} 秒`;
            const timerInterval = setInterval(() => {
                elapsedTime += 1;
                this.response_time = `已耗时 ${elapsedTime} 秒`;
            }, 1000);

            try {
                const response = await axios.post('http://localhost:8000/lesson-edit/ask/', {
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    goal: this.lesson_goal,
                    content: this.lesson_content,
                    outline: this.lesson_outline_markdown,
                    prompt: this.prompt_comm,
                    answer_num: this.sliderValue
                });

                // 请求成功，处理返回的回答列表
                const answers = response.data.responses; // 假设返回的列表存储在outline字段中
                // 使用Markdown的分割线将每个回答分隔开，并合并为一个字符串
                this.responses = answers.map((answer, index) => `## 回答${index + 1}\n\n${answer.trim()}\n`).join('\n---\n\n');

            } catch (error) {
                console.error('请求失败:', error);
                this.response_time = '生成回答失败，请检查网络或重试。';
            } finally {
                clearInterval(timerInterval);
            }
        },
    }
};
</script>

<style scoped>
/* lesson_edit.css 的 CSS 内容 */
.logo {
    width: 140px;
}

@font-face {
    font-family: "tree";
    src: url("~@/assets/figtree-regular.ttf");
}

body>>> {
    padding-bottom: 0;
    font-family: "tree", sans-serif;
    margin: 0;
    background: rgb(247, 249, 252);
}

header {
    display: flex;
    align-items: center;
    padding: 0 10%;
    border-bottom: 1px solid rgb(234, 230, 230);
}

header ul {
    margin-left: auto;
}

header li {
    cursor: pointer;
    /* 鼠标悬停时显示指针 */
    list-style: none;
    /* 移除列表标记 */
    display: inline-block;
    /* 元素行内显示 */
    margin-right: 20px;
    font-size: 14px;
    color: rgb(118, 112, 112);

}


header li#selected {
    border-bottom: 2px solid rgb(15, 212, 143);
    padding-bottom: 4px;
}

.banner {
    min-height: 70px;
    display: flex;
    justify-content: flex-start;
    /* 文本靠左 */
    align-items: center;
    text-align: start;
    /* 文本靠左 */
    padding: 0 30px;
    background: rgb(173, 216, 230);
    /* 淡蓝色背景 */
}

.nav {
    padding: 20px 170px;
    border: 1px solid rgb(234, 230, 230);
}

.icon {
    width: 15px;
}

.el-row {
    margin-bottom: 20px;
    margin-right: 0 !important;
}

.el-row:last-child {
    margin-bottom: 0;
    /* 最后一个.el-row底部外边距为0 */
}

.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
}

.menu {
    padding: 40px 125px;
}

.menu li {
    list-style: none;
    margin: 20px 0;
    display: flex;
    color: gray;
    align-items: center;
    cursor: pointer;
    padding-left: 20px;
}

.icon-xl {
    width: 30px;

    margin-right: 6px;
}

.menu li:first-child {
    padding-left: 15px;
    color: #15ac80;
    border-left: 3px solid #15ac80;
}

.content {
    padding: 45px 0px;
}

.bdg {
    background: rgb(53, 53, 53);
    display: inline-block;
    color: #fff;
    padding: 8px 15px;
    border-radius: 10px;
}

hr {
    background-color: rgb(238, 235, 235);
    height: 1px;
    border: none;
}

.content ul {
    padding-left: 20px;
}

.content li {
    margin: 4px 0;
}

.content p {
    line-height: 25px;
}

.left {

    display: inline-block;
    padding: 4px 8px;
    border-radius: 30px;
    border: 1px solid gray;
    margin-right: 20px;
    cursor: pointer;
}

.mainx {
    width: 75%;
    margin: 0 auto;
    padding: 40px 0;
}

.mainx h2 {
    color: rgb(86, 84, 84);
}

.gray-xl {
    color: rgb(152, 148, 148);
    font-size: 14px;

}

.el-radio-group {
    width: 100%;
    border-bottom: 1px solid rgb(217, 220, 221);
}

.radio-block {
    display: block;
    width: 100%;
    padding: 20px 30px;
    border: 1px solid rgb(217, 220, 221);
    border-bottom: none;


}

.radio-highlight {
    border: 1px solid rgb(45, 174, 218);
}

.editor-container {
    /* 编辑器容器样式，根据需要调整 */
    margin-top: 20px;
}

.markdown-editor {
    /* Markdown 编辑器样式，根据需要调整 */
    margin-bottom: 20px;
    /* 确保编辑器与按钮之间有足够的间距 */

    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
    font-size: 16px;
    /* 根据需要调整字体大小 */
    line-height: 1.2;
    /* 调整行高以提高可读性 */
    font-weight: 800;
    /* 调整字体粗细，400是正常，500稍微粗一点，根据需要调整 */
    color: #111;
    /* 调整字体颜色为深灰，也可以使用黑色或其他颜色 */
    /* 调整内边距 */
    padding: 10px;

    /* 可选：添加轻微的背景色 */
    background-color: #f9f9f9;

    /* 可选：设置边框样式 */
    border: 1px solid #ccc;
    border-radius: 4px;

    /* 可选：设置滚动条样式 */
    overflow-y: auto;
}


.v-md-preview-class ::v-deep p,
.v-md-preview-class ::v-deep h2,
.v-md-preview-class ::v-deep h3 {
    transition: background-color 0.3s ease;
}

.v-md-preview-class ::v-deep p:hover,
.v-md-preview-class ::v-deep li:hover,
.v-md-preview-class ::v-deep h2:hover,
.v-md-preview-class ::v-deep h3:hover {
    background-color: #e1f3d8;
}

.v-md-preview-class p {
    cursor: pointer;
    /* 添加鼠标悬停效果 */
}

.v-md-preview-class>>>.github-markdown-body {
    padding: 0 16px 0 16px;
    /* 或者设置为你想要的padding值 */
}


.text-display {
    height: 100px;
    /* Additional styles for text display */
}

.action-buttons {
    text-align: right;
    margin-top: 10px;
    /* Additional styles for action buttons */
}

.button-for-edit {
    margin: 0 12px 10px 0px;
    height: 30px;
}

.button-for-generate {
    margin: 0 12px 3px 12px;
    height: 30px;
}

.el-menu-h2 {
    height: 30px;
    /* 较窄的高度设置 */
    padding: 0 0 0 0;
    margin: 0 0 0 0;
}

.menu-after-h2 {
    display: flex;
    align-items: center;
    /* 垂直居中内部元素 */
    margin-bottom: 15px;
    padding: 10px;
    /* 内部填充 */
    border: 1px solid #dcdfe6;
    /* 边框样式 */
    border-radius: 4px;
    /* 边框圆角 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* 轻阴影效果 */
}

/* 第一个模块样式 */
.menu-after-h2>div:first-child {
    margin-right: 15px;
    /* 右侧间距为 15px */
    margin-left: 15px;
}

/* 调整按钮组和开关的高度和字号 */
.el-switch,
.el-button,
.el-button-group {
    height: 32px;
    /* 设置按钮和开关的高度 */
    line-height: 32px;
    /* 调整行高以垂直居中文本 */
    font-size: 14px;
    /* 设置字号 */
}

/* 调整按钮内图标的大小 */
.el-icon {
    font-size: 16px;
    /* 图标大小为 16px */
}

/* 特别为生成教案的按钮设置样式 */
.generate-plan-button {
    background-color: #409EFF;
    /* Element UI 蓝色 */
    color: white;
    border-color: #409EFF;
    margin-left: 10px;
}

.button-column {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    /* 这会在按钮之间添加等量间距 */
    margin: 5px 0 10px 0;
}

.infinite-list {
    list-style: none;
    /* 移除默认的列表样式 */
    padding: 0;
    /* 移除默认的内边距 */
}

.infinite-list-item {
    background-color: #fff;
    /* 卡片的背景色 */
    border: 1px solid #e1e1e1;
    /* 卡片边框 */
    border-radius: 8px;
    /* 边框圆角 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* 轻微的阴影效果 */
    margin-bottom: 10px;
    /* 卡片之间的间距 */
    padding: 10px;
    /* 卡片内部的填充空间 */
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    /* 平滑过渡效果 */
}

.infinite-list-item:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    /* 鼠标悬停时增加阴影 */
    transform: translateY(-2px);
    /* 鼠标悬停时轻微向上移动 */
    background-color: #f9f9f9;
    /* 鼠标悬停时改变背景色 */
}
</style>