<template>

    <router-view></router-view>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
.logo {
    width: 140px;
}

@font-face {
    font-family: "tree";
    src: url("~@/assets/figtree-regular.ttf");
}

body {
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
</style>