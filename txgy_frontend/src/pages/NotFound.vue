<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-description">
        抱歉，您访问的页面不存在或已被移除
      </p>
      <div class="error-actions">
        <el-button type="primary" @click="goHome">
          返回首页
        </el-button>
        <el-button @click="goBack">
          返回上页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 25%, #3730a3 50%, #312e81 75%, #1e1b4b 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.not-found-page::before {
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

.not-found-page::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="tech-grid" width="50" height="50" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="50" height="50" fill="none"/><circle cx="25" cy="25" r="1.5" fill="rgba(59,130,246,0.4)"/><rect x="22" y="22" width="6" height="6" fill="none" stroke="rgba(99,102,241,0.3)" stroke-width="0.5"/><line x1="0" y1="25" x2="50" y2="25" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><line x1="25" y1="0" x2="25" y2="50" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><polygon points="25,10 30,20 20,20" fill="none" stroke="rgba(139,92,246,0.2)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23tech-grid)"/></svg>');
  z-index: 2;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
  padding: 40px;
  position: relative;
  z-index: 3;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.error-code {
  font-size: 120px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(96, 165, 250, 0.5);
}

.error-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 16px;
  color: white;
}

.error-description {
  font-size: 16px;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

:deep(.el-button:not(.el-button--primary)) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

:deep(.el-button:not(.el-button--primary):hover) {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .error-code {
    font-size: 80px;
  }

  .error-title {
    font-size: 24px;
  }

  .error-actions {
    flex-direction: column;
    align-items: center;
  }

  .not-found-content {
    margin: 20px;
    padding: 30px 20px;
  }
}
</style>
