<script setup>
</script>

<template>
  <div>
    <el-divider />

    <el-row justify="center">
      <h1 class="section-title">Training Curve</h1>
    </el-row>

    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="14">
        <div class="iframe-container">
          <iframe
            src="https://wandb.ai/csbarista/real-my-eve-transformer/reports/RTDNet-Training-Curve--VmlldzoxMDk2ODg0NA"
            width="100%"
            height="800px"
            frameborder="0"
            style="background-color: white;"
          >
          </iframe>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.iframe-container {
  margin: 20px;
  border: 1px solid #fff;
  border-radius: 4px;
  overflow: hidden;
  background-color: white;
}
</style>
