<script setup>
import { ref } from 'vue'

const pdfUrl = ref('/academic-project-page-template-vue/pdf/rtdnet.pdf')
</script>

<template>
  <div>
    <el-divider />
    
    <el-row justify="center">
      <h1 class="section-title">Paper</h1>
    </el-row>

    <el-row justify="center">
      <el-col :xs="24" :sm="20" :md="16" :lg="14" :xl="14">
        <div class="pdf-container">
          <iframe 
            :src="pdfUrl"
            width="100%" 
            height="800px"
            type="application/pdf"
            style="background-color: white;"
          >
          </iframe>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.pdf-container {
  margin: 20px;
  border: 1px solid #fff;
  border-radius: 4px;
  overflow: hidden;
  background-color: white;
}
</style>
