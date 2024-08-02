<template>
    <div id="app">
        <header>
            <!-- <img class="logo" src="~@/assets/icon.svg" /> -->
            <ul>
                <li id="selected">课程</li>
                <li>大纲编辑</li>
                <!-- <li>Design Units</li> -->
                <!-- <li>Give Feedback</li> -->
                <!-- <li>The Studio</li> -->
                <li style="margin-left: 14px;">
                    <!-- <div> -->
                        <!-- <el-avatar> F </el-avatar> -->
                    <!-- </div> -->
                </li>
            </ul>

            <!-- </el-menu> -->
        </header>
        <!-- <div class="banner">
            Your robot is ready and standing by...<a href="#">
                tell me more <el-button style="margin: 0 20px;" type="danger">Upgrade Robot</el-button>
            </a>

        </div> -->
        <div class="nav">
            <el-breadcrumb separator=">">
                <el-breadcrumb-item :to="{ path: '/' }"><img class="icon"
                        src="~@/assets/home.png" /></el-breadcrumb-item>
                <el-breadcrumb-item>课程创建</el-breadcrumb-item>
                <!-- <el-breadcrumb-item>promotion list</el-breadcrumb-item> -->
                <!-- <el-breadcrumb-item>promotion detail</el-breadcrumb-item> -->
            </el-breadcrumb>
        </div>
        <div class="mainx">

            <h2> <img class="icon-xl" src="~@/assets/pen.png" />创建您的课程</h2>
            <p>您的课程名称?（必填）

            </p>
            <div>
                <!-- <el-input v-model="lesson_name" placeholder="数据结构与算法" @blur="sendCourseNameStream" /> -->
                <el-input v-model="lesson_name" placeholder="数据结构与算法" />
            </div>

            <p class="gray-xl">{{ time_controller }} </p>
            <p class="gray-xl">{{ lesson_description }} </p>
            <p>您的课程关于?（必填，请填写您本次课希望讲解的课程内容）

            </p>
            <div>
                <el-input v-model="lesson_theme" placeholder="快速排序" />
            </div>

            <p>您的课程是为哪个阶段的学生设计？（必填）

            </p>
            <div>
                <el-input v-model="lesson_type" placeholder="大学二年级" />
            </div>
            <!-- <hr />
            <p>What'Vue pronounced /vjuː About?
            </p> -->

            <!-- 标签页 -->
            <div>
                <el-tabs v-model="activeName" class="demo-tabs">
                    <!-- 第一个Tab -->
                    <el-tab-pane label="课程目标" name="first">
                        <div>
                            <p>请填写您本节课的课程目标（选填，关键词即可，如果不填将会自动生成）。

                            </p>

                            <div>
                                <el-input type="textarea" :rows="10" v-model="lesson_goal" placeholder="请输入" />
                            </div>
                        </div>
                        <!-- <div>
                            <p>请填写预设的prompt，课程名称用{lesson_name}代替， 课程关于{lesson_theme}，原课程目标{lesson_goal}。

                            </p>
                            <div>
                                <el-input type="textarea" :rows="10" v-model="prompt" placeholder="请输入" />
                            </div>
                        </div> -->
                        <p>{{ timerMessage }}</p>
                        <div style="margin: 20px 0;float: right;">
                <el-button type="success" @click="openNewTabWithOutline">生成大纲</el-button>
            </div>
                        <div style="margin: 20px 20px 20px 20px;float: right;">
                            <el-button type="primary" @click="sendCourseGoal">生成目标</el-button>
                        </div>
                        

                    </el-tab-pane>
                    <!-- 第二个Tab -->
                    <!-- <el-tab-pane label="课程内容" name="second">
                        <p>课程内容：
                        </p>
                        <div>
                            <el-input type="textarea" :rows="6" v-model="lesson_content" placeholder="请输入" />
                        </div>
                        <div style="margin: 20px 0;float: right;">
                            <el-button type="primary">生成课程内容</el-button>
                        </div>
                    </el-tab-pane> -->
                </el-tabs>
            </div>

            <!-- <hr /> -->

            <!-- <div style="display: flex;justify-content: space-between;align-items: center;"> -->
            <!-- <p style="width: 60%;">Enchanced Declarative Rendering:
                    <br /> <span class="gray-xl">
                        Declarative Rendering: Vue extends standard HTML with a template syntax that allows us to
                        declaratively describe HTML output based on JavaScript state.
                    </span>
                </p> -->
            <!-- 双向绑定switch
                <el-switch v-model="value1" /> -->
            <!-- </div> -->
            <!-- <hr /> -->



            <!-- <h2>TODO 知识库</h2> -->
            <div style="margin: 20px 0;float: right;">
                <!-- <el-button type="success" @click="openNewTabWithOutline">生成大纲</el-button> -->
            </div>
        </div>
    </div>
    <!-- <script src="js/lesson_create.js" type="module"></script> -->
</template>

<script>
// lesson_create.js 的 JavaScript 内容
import fetchStream from '@/utils/fetchStream';
import axios from 'axios';


export default {
    data() {
        return {
            lesson_name: '',
            lesson_goal: '',
            lesson_content: '',
            lesson_theme: '',
            lesson_type: '',
            lesson_description: '',
            time_controller: '',
            prompt: `我现在要为{lesson_name}的{lesson_theme}课程备课，对象是没有学过该课程的{lesson_type}学生，
请你按照Bloom's Taxonomy，为我制定若干点课程目标。请注意，这是一个textarea框，不要出现markdown格式的排版，并确保结果在15行以内。

例子：
输入：数据结构与算法  快速排序  
课程目标：
    1. 学生将会记忆快速排序算法的步骤以及它的基本原则如“分而治之”和递归。
    2. 学生能够理解快速排序的工作机制，包括如何选择基准点以及如何进行分区操作。
    3. 学生能应用快速排序算法，手动对一组数进行排序，并且在计算机上用编程语言实现该算法。
    4. 学生能够分析快速排序的执行过程，识别在不同的基准点选择下算法性能可能发生的变化。
    5. 学生将会评价快速排序算法的性能，了解它与冒泡、选择和插入排序算法在不同场景下效率的差异。
    6. 学生将探索快速排序算法的改进方法，比如三数取中法或随机化基准点，以优化算法性能。`,
            prompt2: `我现在要为{lesson_name}的{lesson_theme}课程备课，对象是没有学过该课程的本科生，
请你按照Bloom's Taxonomy，为我制定若干点课程目标。请注意，这是一个textarea框，不要出现markdown格式的排版，并确保结果在8行以内。

我给你一些我想要、倾向要的内容，请你务必将这些内容囊括在其中，当然，也有可能是教师对其中内容进行了部分删减，你需要自行判断。'{lesson_goal}'.
以下是一个输出的例子：
课程目标：
    1. 学生将会记忆快速排序算法的步骤以及它的基本原则如“分而治之”和递归。
    2. 学生能够理解快速排序的工作机制，包括如何选择基准点以及如何进行分区操作。
    3. 学生能应用快速排序算法，手动对一组数进行排序，并且在计算机上用编程语言实现该算法。
    4. 学生能够分析快速排序的执行过程，识别在不同的基准点选择下算法性能可能发生的变化。
    5. 学生将会评价快速排序算法的性能，了解它与冒泡、选择和插入排序算法在不同场景下效率的差异。
    6. 学生将探索快速排序算法的改进方法，比如三数取中法或随机化基准点，以优化算法性能。`,
            activeName: 'first',
            timerMessage: '', // 用于显示计时信息的数据属性
        };
    },
    methods: {
        setCookie(name, value, days) {
            let expires = "";
            if (days) {
                const date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "") + expires + "; path=/";
        },

        async sendCourseName() {
            // 初始化计时
            let elapsedTime = 0;
            // 启动计时，直接更新lesson_description来显示计时信息
            this.lesson_description = `已耗时 ${elapsedTime} 秒`;
            const timerInterval = setInterval(() => {
                elapsedTime += 1;
                this.lesson_description = `已耗时 ${elapsedTime} 秒`;
            }, 1000);

            // 发送请求
            try {
                const response = await axios.post('http://localhost:8000/lesson-create/course-name/', {
                    name: this.lesson_name
                });
                // 请求成功，更新lesson_description来显示请求结果
                this.lesson_description = response.data.summary;
            } catch (error) {
                console.error('请求失败:', error);
                // 请求失败，更新lesson_description来显示错误信息
                this.lesson_description = '请求失败，请检查网络或重试。';
            } finally {
                clearInterval(timerInterval); // 请求结束，清除定时器
            }
        },

        // async sendCourseGoal() {
        //     // 初始化计时
        //     let elapsedTime = 0;
        //     // 启动计时，更新timerMessage来显示计时信息
        //     this.timerMessage = `已耗时 ${elapsedTime} 秒`;
        //     const timerInterval = setInterval(() => {
        //         elapsedTime += 1;
        //         this.timerMessage = `已耗时 ${elapsedTime} 秒`;
        //     }, 1000);

        //     // 发送请求
        //     try {
        //         const response = await axios.post('http://localhost:8000/lesson-create/course-goal/', {
        //             goal: this.lesson_goal, // 这里使用用户输入的目标
        //             name: this.lesson_name,
        //             theme: this.lesson_theme,
        //             prompt: this.prompt
        //         });

        //         // 请求成功，更新lesson_goal来显示请求结果
        //         this.lesson_goal = response.data;
        //     } catch (error) {
        //         console.error('请求失败:', error);
        //         // 请求失败，不更新lesson_goal，因为它绑定到用户输入
        //     } finally {
        //         clearInterval(timerInterval); // 请求结束，清除定时器
        //         this.timerMessage = ''; // 清空计时信息
        //     }
        // },
        async sendCourseGoal() {
            var prompt_to_send;
            // alert(this.lesson_type);
            if (this.lesson_goal === '') {
                prompt_to_send = this.prompt;
            }
            else {
                prompt_to_send = this.prompt2;

            }
            const goal = this.lesson_goal;
            this.lesson_goal = '';
            fetchStream(
                'http://localhost:8000/lesson-create/course-goal/',
                {
                    goal: goal, // 这里使用用户输入的目标
                    name: this.lesson_name,
                    theme: this.lesson_theme,
                    prompt: prompt_to_send,
                    lesson_type: this.lesson_type,
                },
                (chunk) => { // 成功接收到数据块时的处理逻辑
                    this.lesson_goal += chunk;
                },
                (error) => { // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                    this.lesson_goal = '请求失败！'
                },
                () => { // 请求结束时的处理逻辑
                }
            );
        },

        // openNewTabWithOutline() {
        //     window.open('http://localhost:8000/edit/', '_blank');
        // }

        async openNewTabWithOutline() {
            try {
                // 发送请求到后端并包含所有课程数据
                // await axios.post('http://localhost:8000/edit/', {
                //     name: this.lesson_name,
                //     goal: this.lesson_goal,
                //     content: this.lesson_content,
                //     theme: this.lesson_theme
                // });
                // 存储数据到localStorage
                localStorage.setItem('lesson_name', this.lesson_name);
                localStorage.setItem('lesson_goal', this.lesson_goal);
                localStorage.setItem('lesson_type', this.lesson_type);
                localStorage.setItem('lesson_content', this.lesson_content);
                localStorage.setItem('lesson_theme', this.lesson_theme);
                localStorage.setItem('lesson_description', this.lesson_description);
                // 直接在新标签页中打开lesson_edit.html
                const url = "/lesson-edit";
                window.open(url, '_blank');
            } catch (error) {
                console.error(error);
            }
        },
        async sendCourseNameStream() {
            // 初始化计时
            let elapsedTime = 0;
            this.lesson_description = '';
            this.time_controller = `已耗时 ${elapsedTime} 秒`;
            const timerInterval = setInterval(() => {
                elapsedTime += 1;
                this.time_controller = `已耗时 ${elapsedTime} 秒`;
            }, 1000);

            // 使用fetchStream发送请求并处理流式响应
            fetchStream(
                'http://localhost:8000/lesson-create/course-name/',
                { name: this.lesson_name },
                (chunk) => { // 成功接收到数据块时的处理逻辑
                    this.lesson_description += chunk;
                },
                (error) => { // 请求失败时的处理逻辑
                    console.error('请求失败:', error);
                    this.time_controller = '请求失败，请检查网络或重试。';
                },
                () => { // 请求结束时的处理逻辑
                    clearInterval(timerInterval); // 清除定时器
                }
            );
        },
        toggleEdit(index) {
            this.lesson_sections[index].editing = !this.lesson_sections[index].editing;
        },
        saveEdit(index) {
            this.lesson_sections[index].editing = false;
            // 保存你的修改
            // ...
        }
    }
};
</script>



<style scoped>
/* lesson_create.css 的 CSS 内容 */
.logo {
    width: 140px;
}

@font-face {
    font-family: "tree";
    src: url("../assets/figtree-regular.ttf");
}

body {
    padding-bottom: 300px;
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
    width: 65%;
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


/* 增加行高 */
p,
.gray-xl,
.content p,
.radio-block {
    line-height: 1.6;
    /* 调整为适当的值 */
}

/* 调整内边距和外边距 */
.mainx {
    padding: 60px 0;
    /* 增加垂直方向的内边距 */
}

.el-input,
.el-textarea__inner {
    padding: 10px;
    /* 为输入框增加内边距 */
    margin-bottom: 20px;
    /* 增加输入框下方的外边距 */
}

/* 如果需要，调整元素宽度 */
.mainx {
    max-width: 1000px;
    /* 或其他适合你布局的宽度 */
    margin: 0 auto;
    /* 水平居中 */
}

/* 调整标题和段落之间的间距 */
.mainx h2 {
    margin-bottom: 20px;
    /* 增加标题下方的外边距 */
}

/* 调整列表项的外边距 */
.content li {
    margin: 8px 0;
    /* 增加列表项的垂直外边距 */
}

/* 为面包屑导航增加更多空间 */
.nav {
    padding: 30px 170px;
    /* 增加垂直方向的内边距 */
}

/* 为按钮增加外边距，防止紧贴其他元素 */
.el-button {
    margin: 10px 0;
    /* 为按钮增加上下外边距 */
}
</style>