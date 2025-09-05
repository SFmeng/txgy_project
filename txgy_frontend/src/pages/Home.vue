<template>
  <div class="home-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-icon">
            <el-icon :size="32" color="#667eea">
              <Shop />
            </el-icon>
          </div>
          <span class="brand-text">防腐保温智慧平台</span>
        </div>
        <div class="nav-menu">
          <a href="#features" class="nav-link">核心功能</a>
          <a href="#solutions" class="nav-link">解决方案</a>
          <a href="#about" class="nav-link">关于我们</a>
          <a href="#contact" class="nav-link">联系我们</a>
        </div>
        <div class="nav-actions">
          <el-button @click="handleLogin" class="login-btn">登录</el-button>
          <el-button type="primary" @click="handleRegister" class="register-btn">注册</el-button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-pattern"></div>
      </div>
      <div class="hero-container">
        <div class="hero-content">
          <div class="hero-badge">
            <el-icon><Star /></el-icon>
            <span>专业的防腐保温行业服务平台</span>
          </div>

          <h1 class="hero-title">
            <span class="title-main">防腐保温</span>
            <span class="title-highlight">智慧管理平台</span>
          </h1>

          <p class="hero-description">
            致力于为防腐保温行业提供全方位的数字化解决方案<br>
            整合行业资源，提升管理效率，推动行业创新发展
          </p>

          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-number">500+</div>
              <div class="stat-label">合作企业</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">10000+</div>
              <div class="stat-label">项目案例</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">98%</div>
              <div class="stat-label">客户满意度</div>
            </div>
          </div>

          <div class="hero-actions">
            <el-button type="primary" size="large" @click="handleGetStarted" class="primary-btn">
              <el-icon><Right /></el-icon>
              进入平台
            </el-button>
            <el-button size="large" @click="handleLearnMore" class="secondary-btn">
              <el-icon><View /></el-icon>
              了解详情
            </el-button>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="about-section">
      <div class="section-container">
        <div class="about-content">
          <div class="about-text">
            <div class="section-badge">
              <el-icon><Setting /></el-icon>
              <span>关于平台</span>
            </div>
            <h2 class="section-title">专业的行业服务平台</h2>
            <p class="section-description">
              防腐保温智慧平台是专门为防腐保温行业打造的综合性服务平台，
              集成了项目管理、资源整合、技术交流、市场信息等多项功能，
              为行业内企业和从业人员提供一站式的数字化解决方案。
            </p>
            <div class="about-features">
              <div class="about-feature">
                <el-icon><Check /></el-icon>
                <span>专业的行业知识库</span>
              </div>
              <div class="about-feature">
                <el-icon><Check /></el-icon>
                <span>完善的项目管理体系</span>
              </div>
              <div class="about-feature">
                <el-icon><Check /></el-icon>
                <span>高效的资源配置方案</span>
              </div>
            </div>
          </div>
          <div class="about-image">
            <div class="image-placeholder">
              <el-icon :size="120"><DataBoard /></el-icon>
              <p>平台管理界面</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section id="features" class="services-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">核心服务</h2>
          <p class="section-subtitle">
            为防腐保温行业提供全方位的专业服务
          </p>
        </div>

        <div class="services-grid">
          <div class="service-card" v-for="feature in features" :key="feature.id">
            <div class="service-icon">
              <el-icon :size="40">
                <component :is="feature.icon" />
              </el-icon>
            </div>
            <h3 class="service-title">{{ feature.title }}</h3>
            <p class="service-description">{{ feature.description }}</p>
            <div class="service-link">
              <el-icon><Right /></el-icon>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer Section -->
    <footer class="footer-section">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-main">
            <div class="footer-brand">
              <div class="brand-logo">
                <el-icon :size="32" color="#667eea">
                  <Shop />
                </el-icon>
                <span class="brand-name">防腐保温智慧平台</span>
              </div>
              <p class="brand-description">
                专业的防腐保温行业服务平台，致力于推动行业数字化发展
              </p>
            </div>

            <div class="footer-links">
              <div class="link-group">
                <h4 class="link-title">平台服务</h4>
                <ul class="link-list">
                  <li><a href="#" class="footer-link">项目管理</a></li>
                  <li><a href="#" class="footer-link">资源整合</a></li>
                  <li><a href="#" class="footer-link">技术支持</a></li>
                  <li><a href="#" class="footer-link">市场信息</a></li>
                </ul>
              </div>

              <div class="link-group">
                <h4 class="link-title">关于我们</h4>
                <ul class="link-list">
                  <li><a href="#" class="footer-link">公司介绍</a></li>
                  <li><a href="#" class="footer-link">发展历程</a></li>
                  <li><a href="#" class="footer-link">团队介绍</a></li>
                  <li><a href="#" class="footer-link">联系我们</a></li>
                </ul>
              </div>

              <div class="link-group">
                <h4 class="link-title">帮助中心</h4>
                <ul class="link-list">
                  <li><a href="#" class="footer-link">使用指南</a></li>
                  <li><a href="#" class="footer-link">常见问题</a></li>
                  <li><a href="#" class="footer-link">技术文档</a></li>
                  <li><a href="#" class="footer-link">意见反馈</a></li>
                </ul>
              </div>
            </div>
          </div>

          <div class="footer-bottom">
            <div class="footer-copyright">
              <p>&copy; 2024 防腐保温智慧平台. 保留所有权利.</p>
              <p>
                <a href="#" class="footer-link">隐私政策</a> |
                <a href="#" class="footer-link">服务条款</a> |
                <a href="#" class="footer-link">法律声明</a>
              </p>
            </div>
            <div class="footer-info">
              <p>技术支持：智慧平台技术团队</p>
              <p>服务热线：400-123-4567</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Shop,
  Search,
  ChatDotRound,
  DataBoard,
  Document,
  Star,
  Check,
  Right,
  View,
  Connection,
  Setting,
  Monitor
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

// 核心服务数据
const features = ref([
  {
    id: 1,
    icon: Shop,
    title: '项目管理',
    description: '提供完整的防腐保温项目管理解决方案，从项目立项到竣工验收的全流程管理'
  },
  {
    id: 2,
    icon: Search,
    title: '资源整合',
    description: '整合行业优质资源，包括材料供应商、施工队伍、技术专家等'
  },
  {
    id: 3,
    icon: ChatDotRound,
    title: '技术交流',
    description: '搭建行业技术交流平台，促进新技术、新工艺的推广应用'
  },
  {
    id: 4,
    icon: DataBoard,
    title: '质量监控',
    description: '建立完善的质量监控体系，确保工程质量符合行业标准'
  },
  {
    id: 5,
    icon: Monitor,
    title: '数据分析',
    description: '提供行业数据分析服务，为企业决策提供科学依据'
  },
  {
    id: 6,
    icon: Document,
    title: '标准规范',
    description: '制定和维护行业标准规范，推动行业规范化发展'
  }
])

// 方法
const handleGetStarted = () => {
  if (authStore.isLoggedIn) {
    router.push('/admin')
  } else {
    router.push('/auth/login')
  }
}

const handleLearnMore = () => {
  const featuresSection = document.querySelector('#features')
  if (featuresSection) {
    featuresSection.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleLogin = () => {
  router.push('/auth/login')
}

const handleRegister = () => {
  router.push('/auth/register')
}

// 页面初始化
onMounted(() => {
  document.title = '防腐保温智慧平台 - 专业的行业解决方案'
})
</script>

<style scoped>
/* 全局样式 */
.home-page {
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}

/* 导航栏样式 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(30, 58, 138, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 18px;
  color: #ffffff;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-menu {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #9ca3af;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #60a5fa;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: #60a5fa;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  gap: 12px;
}

.login-btn {
  border: 1px solid rgba(120, 119, 198, 0.4);
  color: #9ca3af;
  background: transparent;
}

.login-btn:hover {
  border-color: #60a5fa;
  color: #60a5fa;
}

.register-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  border: none;
  color: white;
}

/* Hero Section */
.hero-section {
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 25%, #3730a3 50%, #312e81 75%, #1e1b4b 100%);
  color: white;
  text-align: center;
  padding: 120px 20px;
  position: relative;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(139, 92, 246, 0.25) 0%, transparent 50%);
}

.hero-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="tech-grid" width="50" height="50" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="50" height="50" fill="none"/><circle cx="25" cy="25" r="1.5" fill="rgba(59,130,246,0.4)"/><rect x="22" y="22" width="6" height="6" fill="none" stroke="rgba(99,102,241,0.3)" stroke-width="0.5"/><line x1="0" y1="25" x2="50" y2="25" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><line x1="25" y1="0" x2="25" y2="50" stroke="rgba(59,130,246,0.15)" stroke-width="0.5"/><polygon points="25,10 30,20 20,20" fill="none" stroke="rgba(139,92,246,0.2)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23tech-grid)"/></svg>');
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.geometric-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 5s;
}

.shape-3 {
  width: 80px;
  height: 80px;
  bottom: 30%;
  left: 20%;
  animation-delay: 10s;
}

.shape-4 {
  width: 120px;
  height: 120px;
  top: 10%;
  right: 30%;
  animation-delay: 15s;
}

.shape-5 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  right: 40%;
  animation-delay: 8s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-30px) rotate(120deg); }
  66% { transform: translateY(-60px) rotate(240deg); }
}

.floating-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: particle-float 15s linear infinite;
}

.particle:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.particle:nth-child(2) { top: 20%; left: 20%; animation-delay: 2s; }
.particle:nth-child(3) { top: 30%; left: 30%; animation-delay: 4s; }
.particle:nth-child(4) { top: 40%; left: 40%; animation-delay: 6s; }
.particle:nth-child(5) { top: 50%; left: 50%; animation-delay: 8s; }
.particle:nth-child(6) { top: 60%; left: 15%; animation-delay: 10s; }
.particle:nth-child(7) { top: 70%; left: 35%; animation-delay: 12s; }
.particle:nth-child(8) { top: 80%; left: 25%; animation-delay: 14s; }
.particle:nth-child(9) { top: 15%; left: 60%; animation-delay: 16s; }
.particle:nth-child(10) { top: 35%; left: 80%; animation-delay: 18s; }

@keyframes particle-float {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-50px) translateX(50px);
    opacity: 0;
  }
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  z-index: 2;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(120, 119, 198, 0.2);
  backdrop-filter: blur(10px);
  padding: 10px 20px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 32px;
  border: 1px solid rgba(120, 119, 198, 0.4);
  animation: badge-glow 3s ease-in-out infinite;
}

/* Hero文本样式 */
.hero-text {
  color: white;
  position: relative;
  z-index: 20;
}

@keyframes badge-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(120, 119, 198, 0.3); }
  50% { box-shadow: 0 0 30px rgba(255, 119, 48, 0.4); }
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 24px;
  color: white;
}

.title-main {
  display: block;
  color: white;
}

.title-highlight {
  display: block;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 20px;
  line-height: 1.6;
  margin-bottom: 48px;
  color: rgba(255, 255, 255, 0.9);
  max-width: 700px;
}

.hero-stats {
  display: flex;
  gap: 60px;
  margin-bottom: 48px;
  justify-content: center;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 800;
  color: #ff7730;
  margin-bottom: 8px;
  display: block;
}

.stat-label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.primary-btn {
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%) !important;
  border: none !important;
  color: white !important;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(255, 119, 48, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 119, 48, 0.5);
}

.secondary-btn {
  background: rgba(120, 119, 198, 0.2) !important;
  border: 1px solid rgba(120, 119, 198, 0.4) !important;
  color: white !important;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: rgba(120, 119, 198, 0.3) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(120, 119, 198, 0.3);
}

/* 通用区域样式 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 20px;
  color: #ffffff;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 18px;
  color: #9ca3af;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* Services Section */
.services-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
}

.service-card {
  background: rgba(45, 45, 45, 0.9);
  padding: 40px 32px;
  border-radius: 20px;
  text-align: left;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(120, 119, 198, 0.3);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.service-card:hover::before {
  transform: scaleX(1);
}

.service-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 20px 50px rgba(255, 119, 48, 0.3);
}

.service-icon {
  margin-bottom: 24px;
  color: #ff7730;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.service-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #ffffff;
}

.service-description {
  font-size: 16px;
  line-height: 1.6;
  color: #9ca3af;
  margin-bottom: 20px;
}

.service-link {
  color: #7877c6;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.service-card:hover .service-link {
  opacity: 1;
  transform: translateX(0);
}

/* Footer Section */
.footer-section {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  color: white;
  padding: 60px 0 30px;
  border-top: 1px solid rgba(120, 119, 198, 0.3);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.footer-content {
  display: flex;
  flex-direction: column;
}

.footer-main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 60px;
  margin-bottom: 40px;
}

.footer-brand {
  max-width: 300px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  color: white;
}

.brand-description {
  font-size: 16px;
  line-height: 1.6;
  color: #9ca3af;
  margin: 0;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.link-group {
  display: flex;
  flex-direction: column;
}

.link-title {
  font-size: 18px;
  font-weight: 600;
  color: white;
  margin-bottom: 20px;
}

.link-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-link {
  color: #9ca3af;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #ff7730;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 30px;
  border-top: 1px solid #374151;
}

.footer-copyright {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-copyright p {
  margin: 0;
  font-size: 14px;
  color: #9ca3af;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: right;
}

.footer-info p {
  margin: 0;
  font-size: 14px;
  color: #9ca3af;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-description {
    font-size: 16px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .section-title {
    font-size: 32px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .cta-title {
    font-size: 32px;
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
}

.hero-features {
  display: flex;
  gap: 16px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 16px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.hero-actions {
  display: flex;
  gap: 20px;
  margin-bottom: 48px;
}

.cta-primary {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
  border: none !important;
  color: #1f2937 !important;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
  transition: all 0.3s ease;
}

.cta-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.4);
}

.cta-secondary {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: white !important;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 0.2) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.1);
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-card {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px 24px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-5px);
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 8px;
  display: block;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.9);
}

/* Hero视觉部分 */
.visual-container {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.main-dashboard {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: dashboard-float 6s ease-in-out infinite;
}

@keyframes dashboard-float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(1deg); }
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.header-dots {
  display: flex;
  gap: 6px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #10b981; }

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-area {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
}

.chart-title {
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: 8px;
  height: 60px;
}

.bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  width: 20px;
  animation: bar-grow 2s ease-out;
}

@keyframes bar-grow {
  from { height: 0; }
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.metric-icon {
  font-size: 16px;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2px;
}

.metric-label {
  font-size: 10px;
  color: #6b7280;
}

.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.float-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  animation: float-card 8s ease-in-out infinite;
}

.card-1 {
  top: 10%;
  left: -20%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: -25%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 20%;
  left: -15%;
  animation-delay: 4s;
}

@keyframes float-card {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(2deg); }
}

.float-card .el-icon {
  font-size: 16px;
  color: #667eea;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-stats {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

/* 通用区域样式 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 80px;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  color: white;
  padding: 8px 20px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 24px;
}

/* About Section */
.about-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}

.about-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.about-text {
  max-width: 500px;
}

.section-description {
  font-size: 18px;
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 32px;
}

.about-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.about-feature {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  color: #ffffff;
}

.about-feature .el-icon {
  color: #ff7730;
}

.about-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-placeholder {
  background: linear-gradient(135deg, #3d3d3d 0%, #2d2d2d 100%);
  border-radius: 20px;
  padding: 60px;
  text-align: center;
  border: 2px dashed rgba(120, 119, 198, 0.4);
}

.image-placeholder .el-icon {
  color: #ff7730;
  margin-bottom: 16px;
}

.image-placeholder p {
  color: #9ca3af;
  font-size: 16px;
  margin: 0;
}

.section-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  color: #1f2937;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 18px;
  color: #6b7280;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* Features Section */
.features-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
  position: relative;
  z-index: 1;
}

.feature-card {
  background: white;
  padding: 40px 32px;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
}

.feature-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.card-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover .card-background {
  opacity: 1;
}

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.15);
}

.feature-icon {
  margin-bottom: 24px;
  color: #667eea;
  position: relative;
  z-index: 1;
}

.feature-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1f2937;
  position: relative;
  z-index: 1;
}

.feature-description {
  font-size: 16px;
  line-height: 1.6;
  color: #6b7280;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.feature-arrow {
  color: #667eea;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.feature-card:hover .feature-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* Solutions Section */
.solutions-section {
  padding: 120px 0;
  background: white;
}

.solutions-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.solutions-text {
  max-width: 500px;
}

.section-description {
  font-size: 18px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 40px;
}

.solution-features {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 40px;
}

.solution-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  opacity: 0;
  transform: translateX(-20px);
  transition: all 0.5s ease;
}

.solution-item.animate-in {
  opacity: 1;
  transform: translateX(0);
}

.solution-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.solution-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.solution-content p {
  font-size: 16px;
  color: #6b7280;
  line-height: 1.5;
}

.solution-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  color: white !important;
  font-weight: 600;
  padding: 16px 32px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.solution-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.solutions-visual {
  display: flex;
  justify-content: center;
}

.process-flow {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  min-width: 120px;
}

.flow-step:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.15);
}

.step-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 12px;
}

.step-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.flow-arrow {
  font-size: 24px;
  color: #667eea;
  font-weight: bold;
}

/* Stats Section */
.stats-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.stats-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.stats-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
}

.stats-content {
  position: relative;
  z-index: 1;
}

.stats-title {
  text-align: center;
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 80px;
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
}

.stats-section .stat-card {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 40px 24px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(30px);
}

.stats-section .stat-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.stats-section .stat-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-10px);
}

.stats-section .stat-icon {
  margin-bottom: 20px;
  color: #fbbf24;
}

.stats-section .stat-number {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 12px;
  color: #fbbf24;
  display: block;
}

.stats-section .stat-label {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  opacity: 0.9;
}

.stats-section .stat-description {
  font-size: 14px;
  opacity: 0.7;
}

/* CTA Section */
.cta-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.cta-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="hexagon" width="50" height="50" patternUnits="userSpaceOnUse"><polygon points="25,5 45,17 45,33 25,45 5,33 5,17" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23hexagon)"/></svg>');
}

.cta-content {
  max-width: 700px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.cta-icon {
  margin-bottom: 32px;
  color: #fbbf24;
}

.cta-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cta-description {
  font-size: 20px;
  margin-bottom: 48px;
  opacity: 0.9;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 32px;
}

.cta-actions .cta-primary {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
  border: none !important;
  color: #1f2937 !important;
  font-weight: 600;
  padding: 18px 36px;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
}

.cta-actions .cta-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.4);
}

.cta-actions .cta-secondary {
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: white !important;
  font-weight: 600;
  padding: 18px 36px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.cta-actions .cta-secondary:hover {
  background: rgba(255, 255, 255, 0.2) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.1);
}

.cta-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  opacity: 0.7;
  color: #fbbf24;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .solutions-content {
    grid-template-columns: 1fr;
    gap: 60px;
  }

  .process-flow {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .flow-arrow {
    transform: rotate(90deg);
  }
}

@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-stats {
    justify-content: center;
    flex-wrap: wrap;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }

  .cta-title {
    font-size: 36px;
  }

  .section-title {
    font-size: 36px;
  }
}

@media (max-width: 480px) {
  .hero-stats {
    flex-direction: column;
    gap: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .hero-features {
    flex-direction: column;
    align-items: center;
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>
