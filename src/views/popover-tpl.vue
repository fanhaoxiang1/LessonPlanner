<template>
    <el-container>
        <!-- Top section with radio buttons and textarea -->
        <el-header style="display: flex; justify-content: space-between; align-items: center;">
            <!-- Radio buttons -->
            <el-radio-group v-model="radio">
                <el-radio label="1">Option 1</el-radio>
                <el-radio label="2">Option 2</el-radio>
            </el-radio-group>

            <!-- Textarea -->
            <el-input type="textarea" rows="2" placeholder="Please input" style="width: 50%; margin-top: 0;"></el-input>
        </el-header>

        <!-- Middle layout area -->
        <el-main>
            <el-row justify="center">
                <el-col :span="6">
                    <el-button class="button-for-edit"><el-icon>
                            <Edit />
                        </el-icon> Button 1</el-button>
                    <el-button class="button-for-edit"><el-icon>
                            <Edit />
                        </el-icon> Button 2</el-button>
                    <el-button class="button-for-edit"><el-icon>
                            <Edit />
                        </el-icon> Button 3</el-button>
                    <el-button class="button-for-edit"><el-icon>
                            <Edit />
                        </el-icon> Button 4</el-button>
                </el-col>

                <el-col :span="18">
                    <el-row :gutter="10">
                        <el-col :span="12">
                            <el-button class="button-for-generate">Button A</el-button>
                            <br />
                            <el-button class="button-for-generate">Button B</el-button>
                            <br />
                            <el-button class="button-for-generate">Button C</el-button>
                        </el-col>

                        <el-col :span="12">
                            <el-button class="button-for-generate">Button D</el-button>
                            <br />
                            <el-button class="button-for-generate">Button E</el-button>
                            <br />
                            <el-button class="button-for-generate">Button F</el-button>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
        </el-main>

        <!-- Bottom section with text display and buttons -->
        <el-footer>
            <div class="action-buttons">
                <el-button size="small" @click="cancelAction">Cancel</el-button>
                <el-button size="small" type="primary" @click="confirmAction">Confirm</el-button>
            </div>
        </el-footer>
    </el-container>
</template>

<script>
</script>

<style scoped>
.text-display {
    height: 150px;
    /* Additional styles for text display */
}

.action-buttons {
    text-align: right;
    margin-top: 10px;
    /* Additional styles for action buttons */
}

.button-for-edit {
    margin: 0 12px 3px 12px;
    height: 30px;
}

.button-for-generate {
    margin: 0 12px 3px 12px;
    height: 30px;
}</style>