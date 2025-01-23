<script setup>
import { ref } from 'vue'

const responseText = ref('')

const fetchData = async () => {
  try {
    const response = await fetch('http://localhost:6006')
    const data = await response.text()
    responseText.value = data
  } catch (error) {
    responseText.value = '获取数据失败: ' + error.message
  }
}
</script>

<template>
  <div class="video-section">
    <el-divider />

    <el-row justify="center">
      <h1 class="section-title">Explainer Video</h1>
    </el-row>

    <!-- 每个网站的视频的iframe可能不一致，最好在这里手动调整 -->
    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="10" >

        <!-- local -->
        <el-container class="video-container">
          <video controls muted preload playsinline class="video-player">
            <source src="/video/visulization_video.mp4" type="video/mp4">
          </video>
        </el-container>
        
        <!-- bilibili -->
        <!-- <el-container class="video-container">
          <iframe src="//www.bilibili.com/blackboard/html5mobileplayer.html?bvid=BV1zw68YsEP9" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
        </el-container> -->

        <!-- youtube -->
        <!-- <el-container class="video-container">
          <iframe src="https://www.youtube.com/embed/wjZofJX0v4M?si=BFvRyc3n3fFV_f1G" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </el-container> -->
      </el-col>
    </el-row>

    <!-- <el-row justify="center" class="button-container">
      <el-button type="primary" size="large" @click="fetchData" class="fetch-button">
        获取数据
      </el-button>
    </el-row> -->

    <el-row justify="center" v-if="responseText" class="response-container">
      <el-col :xs="24" :sm="20" :md="16" :lg="12" :xl="10">
        <div class="response-text">{{ responseText }}</div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.video-section {
  padding: 2rem 0;
}

.section-title {
  font-size: 2.5rem;
  color: #303133;
  margin-bottom: 2rem;
  font-weight: 600;
}

.video-container {
  margin: 20px 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-player {
  aspect-ratio: 16 / 9;
  width: 100%;
  background-color: #000;
}

iframe {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.button-container {
  margin-top: 2rem;
}

.fetch-button {
  padding: 12px 24px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.fetch-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.response-container {
  margin-top: 2rem;
}

.response-text {
  padding: 1.5rem;
  background-color: #f5f7fa;
  border-radius: 8px;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 1.1rem;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style>