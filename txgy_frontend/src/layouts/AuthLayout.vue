<template>
  <div class="auth-layout">
    <div class="auth-container">
      <!-- 左侧背景区域 -->
      <div class="auth-background">
        <div class="background-content">
          <h1 class="platform-title">防腐保温智慧平台</h1>
          <p class="platform-description">
            专为防腐保温行业打造的综合性信息交互与资源整合平台
          </p>
          <div class="features">
            <div class="feature-item">
              <el-icon class="feature-icon"><Shop /></el-icon>
              <span>信息发布与匹配</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><ChatDotRound /></el-icon>
              <span>沟通互动</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><DataBoard /></el-icon>
              <span>商务服务</span>
            </div>
            <div class="feature-item">
              <el-icon class="feature-icon"><TrendCharts /></el-icon>
              <span>智能分析</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧表单区域 -->
      <div class="auth-form">
        <div class="form-container">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  Shop,
  ChatDotRound,
  DataBoard,
  TrendCharts
} from '@element-plus/icons-vue'
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 1000px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  min-height: 600px;
}

.auth-background {
  flex: 1;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 25%, #3730a3 50%, #312e81 75%, #1e1b4b 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(139, 92, 246, 0.25) 0%, transparent 50%);
  z-index: 1;
}

.auth-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="tech-grid" width="50" height="50" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="50" height="50" fill="none"/><circle cx="25" cy="25" r="1.5" fill="rgba(59,130,246,0.4)"/><rect x="22" y="22" width="6" height="6" fill="none" stroke="rgba(99,102,241,0.3)" stroke-width="0.5"/><line x1="0" y1="25" x2="50" y2="25" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><line x1="25" y1="0" x2="25" y2="50" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><polygon points="25,10 30,20 20,20" fill="none" stroke="rgba(139,92,246,0.2)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23tech-grid)"/></svg>');
  z-index: 2;
}

.background-content {
  position: relative;
  z-index: 3;
  text-align: center;
}

.platform-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.2;
}

.platform-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.9;
}

.features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-2px);
}

.feature-icon {
  font-size: 20px;
  color: #60a5fa;
}

.auth-form {
  flex: 1;
  padding: 60px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

@media (max-width: 768px) {
  .auth-container {
    flex-direction: column;
    max-width: 400px;
  }
  
  .auth-background {
    padding: 40px 20px;
  }
  
  .platform-title {
    font-size: 24px;
  }
  
  .platform-description {
    font-size: 14px;
  }
  
  .features {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .feature-item {
    padding: 12px;
  }
  
  .auth-form {
    padding: 40px 20px;
  }
}
</style>
