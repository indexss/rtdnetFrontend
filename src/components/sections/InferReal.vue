<template>
   <el-divider />

  <el-row justify="center">
    <h1 class="section-title">Try RTDNet on your own video</h1>
  </el-row>
  <div class="infer-real-container">
    <!-- <h2>Gaze Estimation</h2> -->
    
    <!-- 视频上传和预览区域 -->
    <div class="upload-section">
      <!-- 添加重新选择按钮 -->
      <div v-if="uploadedVideo" class="reselect-button-container">
        <button 
          class="reselect-button" 
          @click="resetVideo"
          :disabled="isUploading || isProcessing"
        >
          <i class="fas fa-sync-alt"></i> Reselect Video
        </button>
      </div>

      <div 
        class="upload-box" 
        @drop.prevent="handleDrop" 
        @dragover.prevent
      >
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          accept="video/*" 
          style="display: none"
        >
        <div 
          v-if="!uploadedVideo" 
          class="upload-placeholder"
          @click="triggerFileInput"
        >
          <i class="fas fa-cloud-upload-alt"></i>
          <p>Click or drag video file here</p>
        </div>
        <video 
          v-else 
          ref="previewVideo" 
          controls 
          class="preview-video"
        >
          <source :src="uploadedVideoUrl" type="video/mp4">
        </video>
      </div>
    </div>

    <!-- 按钮组 -->
    <div class="button-group">
      <button 
        class="action-button upload-button" 
        @click="startUpload"
        :disabled="!uploadedVideo || isUploading"
      >
        {{ isUploading ? 'Uploading...' : 'Upload Video' }}
      </button>

      <button 
        class="action-button infer-button" 
        @click="startInference"
        :disabled="!uploadSuccess || isProcessing"
      >
        {{ isProcessing ? 'Processing...' : 'Start Inference' }}
      </button>
    </div>

    <!-- 日志控制台 -->
    <div class="console-output" ref="consoleOutput">
      <div v-for="(log, index) in logs" :key="index" :class="log.type">
        {{ log.message }}
      </div>
      <div v-if="progress > 0" class="progress-bar">
        <div class="progress-fill" :style="{width: `${progress}%`}"></div>
        <span>{{ progress }}%</span>
      </div>
    </div>

    <!-- 结果视频展示 -->
    <div v-if="resultVideo" class="result-section">
      <h3>Inference Result</h3>
      <div class="download-buttons">
        <button 
          class="download-button"
          @click="downloadVideo('original')"
        >
          <i class="fas fa-download"></i>
          Download Original Result
        </button>
        <button 
          class="download-button"
          @click="downloadVideo('face')"
        >
          <i class="fas fa-download"></i>
          Download Face Result
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InferReal',
  data() {
    return {
      uploadedVideo: null,
      uploadedVideoUrl: null,
      resultVideo: null,
      resultVideoUrl: null,
      isUploading: false,
      isProcessing: false,
      uploadSuccess: false,
      progress: 0,
      logs: [],
      inferenceEventSource: null,
      faceVideoUrl: null,
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.processVideoFile(file)
      }
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0]
      if (file && file.type.startsWith('video/')) {
        this.processVideoFile(file)
      }
    },
    processVideoFile(file) {
      this.uploadedVideo = file
      this.uploadedVideoUrl = URL.createObjectURL(file)
    },
    addLog(message, type = 'info') {
      this.logs.push({ message, type })
      // Auto scroll to latest log
      this.$nextTick(() => {
        const console = this.$refs.consoleOutput
        console.scrollTop = console.scrollHeight
      })
    },
    async startUpload() {
      if (!this.uploadedVideo) return
      
      this.isUploading = true
      this.progress = 0
      this.logs = []
      this.addLog('Starting video upload...', 'info')

      try {
        await new Promise((resolve, reject) => {
          const formData = new FormData()
          formData.append('video', this.uploadedVideo)

          const xhr = new XMLHttpRequest()
          
          xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
              const percentComplete = Math.round((event.loaded / event.total) * 100)
              this.progress = percentComplete
              this.addLog(`Upload progress: ${percentComplete}%`, 'info')
            }
          }

          xhr.onload = () => {
            if (xhr.status === 200) {
              const result = JSON.parse(xhr.responseText)
              this.addLog('✅ ' + result.message, 'success')
              this.progress = 100
              this.uploadSuccess = true
              resolve(result)
            } else {
              let errorMessage = 'Upload failed'
              try {
                const errorResponse = JSON.parse(xhr.responseText)
                errorMessage = errorResponse.detail || 'Upload failed'
              } catch (e) {}
              this.addLog('❌ ' + errorMessage, 'error')
              reject(new Error(errorMessage))
            }
          }

          xhr.onerror = () => {
            this.addLog('❌ Network error, please check network connection', 'error')
            reject(new Error('Network error'))
          }

          xhr.onabort = () => {
            this.addLog('❌ Upload cancelled', 'error')
            reject(new Error('Upload cancelled'))
          }

          xhr.open('POST', 'http://localhost:6006/upload-video')
          xhr.send(formData)
        })
        
      } catch (error) {
        this.progress = 0
        this.uploadSuccess = false
        this.addLog(`❌ ${error.message}`, 'error')
      } finally {
        this.isUploading = false
      }
    },
    async startInference() {
      if (!this.uploadSuccess) return
      
      this.isProcessing = true
      this.progress = 0
      this.logs = []
      this.addLog('Starting inference...', 'info')

      try {
        // Close any existing SSE connection
        if (this.inferenceEventSource) {
          this.inferenceEventSource.close()
        }

        // Establish new SSE connection
        this.inferenceEventSource = new EventSource('http://localhost:6006/inference-progress')
        
        this.inferenceEventSource.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.progress !== undefined && data.progress !== null) {
            this.progress = data.progress
          }
          if (data.message) {
            this.addLog(data.message, data.type || 'info')
          }
        }

        this.inferenceEventSource.onerror = (error) => {
          console.error('SSE connection error:', error)
          this.inferenceEventSource.close()
          this.addLog('❌ Progress update connection failed', 'error')
        }

        // Send inference request
        const response = await fetch('http://localhost:6006/start-inference', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Inference request failed')
        }

        const result = await response.json()
        
        // Close SSE connection
        if (this.inferenceEventSource) {
          this.inferenceEventSource.close()
          this.inferenceEventSource = null
        }
        
        // Set result status
        this.resultVideo = true
        
        this.addLog('✅ Inference completed!', 'success')
      } catch (error) {
        this.progress = 0
        this.addLog(`❌ Inference failed: ${error.message}`, 'error')
        
        // Ensure error closes SSE connection
        if (this.inferenceEventSource) {
          this.inferenceEventSource.close()
          this.inferenceEventSource = null
        }
      } finally {
        this.isProcessing = false
      }
    },
    // Add new method: Check if videos are available
    async checkVideosAvailable() {
      const timeout = 30000 // 30 seconds timeout
      const startTime = Date.now()
      
      while (Date.now() - startTime < timeout) {
        try {
          // Check if both videos can be accessed
          const [originalRes, faceRes] = await Promise.all([
            fetch(this.resultVideoUrl, { method: 'HEAD' }),
            fetch(this.faceVideoUrl, { method: 'HEAD' })
          ])
          
          if (originalRes.ok && faceRes.ok) {
            return true // Both videos can be accessed
          }
        } catch (error) {
          console.log('Waiting for videos to be available...')
        }
        
        // Wait 1 second before retrying
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
      
      throw new Error('Videos load timeout')
    },
    resetVideo() {
      // Release previously created URL
      if (this.uploadedVideoUrl) {
        URL.revokeObjectURL(this.uploadedVideoUrl)
      }
      
      // Reset all related states
      this.uploadedVideo = null
      this.uploadedVideoUrl = null
      this.uploadSuccess = false
      this.resultVideo = null
      this.resultVideoUrl = null
      this.progress = 0
      this.logs = []
      
      // Clear file input
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      
      // Close SSE connection
      if (this.inferenceEventSource) {
        this.inferenceEventSource.close()
        this.inferenceEventSource = null
      }
      
      // Clear video URL when faceVideoUrl is cleared
      if (this.faceVideoUrl) {
        URL.revokeObjectURL(this.faceVideoUrl)
      }
      
      this.faceVideoUrl = null
    },
    async downloadVideo(type) {
      try {
        const url = type === 'original' 
          ? `http://localhost:6006/videos/infer_original.mp4`
          : `http://localhost:6006/videos/infer_face.mp4`
        
        const filename = type === 'original' 
          ? 'infer_original.mp4'
          : 'infer_face.mp4'

        this.addLog(`Starting download of ${type === 'original' ? 'original' : 'face'} video...`, 'info')
        
        const response = await fetch(url)
        if (!response.ok) throw new Error('Download failed')
        
        const blob = await response.blob()
        const downloadUrl = window.URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = downloadUrl
        link.download = filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        // Clean up URL objects
        window.URL.revokeObjectURL(downloadUrl)
        
        this.addLog(`✅ ${type === 'original' ? 'Original' : 'Face'} video download complete`, 'success')
      } catch (error) {
        this.addLog(`❌ Download failed: ${error.message}`, 'error')
      }
    }
  }
}
</script>

<style scoped>
.infer-real-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.upload-section {
  margin: 20px 0;
}

.upload-box {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-placeholder {
  color: #666;
  cursor: pointer;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.preview-video, .result-video {
  max-width: 100%;
  max-height: 400px;
  cursor: default;
}

.button-group {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.action-button {
  flex: 1;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.upload-button {
  background-color: #2196F3;
  color: white;
}

.upload-button:disabled {
  background-color: #90CAF9;
  cursor: not-allowed;
}

.infer-button {
  background-color: #4CAF50;
  color: white;
}

.infer-button:disabled {
  background-color: #A5D6A7;
  cursor: not-allowed;
}

.console-output {
  background-color: #1e1e1e;
  color: #fff;
  padding: 15px;
  border-radius: 8px;
  height: 200px;
  overflow-y: auto;
  font-family: monospace;
  margin: 20px 0;
  line-height: 1.4;
}

.progress-bar {
  background-color: #2d2d2d;
  height: 20px;
  border-radius: 10px;
  margin: 10px 0;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
}

.progress-fill {
  background-color: #4CAF50;
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
  position: relative;
  background-image: linear-gradient(
    45deg,
    rgba(255,255,255,0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255,255,255,0.15) 50%,
    rgba(255,255,255,0.15) 75%,
    transparent 75%,
    transparent
  );
  background-size: 20px 20px;
  animation: progress-animation 1s linear infinite;
}

@keyframes progress-animation {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 20px 0;
  }
}

.progress-bar span {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
  z-index: 1;
  font-size: 12px;
}

.info {
  color: #fff;
  padding: 4px 8px;
  margin: 4px 0;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.1);
}

.error {
  color: #ff6b6b;
  padding: 4px 8px;
  margin: 4px 0;
  border-radius: 4px;
  background-color: rgba(255, 107, 107, 0.1);
}

.success {
  color: #4CAF50;
  padding: 4px 8px;
  margin: 4px 0;
  border-radius: 4px;
  background-color: rgba(76, 175, 80, 0.1);
}

.result-section {
  margin-top: 20px;
}

.reselect-button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.reselect-button {
  background-color: #ff9800;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}

.reselect-button:hover {
  background-color: #f57c00;
}

.reselect-button:disabled {
  background-color: #ffcc80;
  cursor: not-allowed;
}

.reselect-button i {
  font-size: 14px;
}

.download-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
}

.download-button {
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 24px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease;
}

.download-button:hover {
  background-color: #1976D2;
}

.download-button:disabled {
  background-color: #90CAF9;
  cursor: not-allowed;
}

.download-button i {
  font-size: 16px;
}
</style> 