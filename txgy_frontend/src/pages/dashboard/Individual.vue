<template>
  <div class="individual-dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">
          欢迎回来，{{ authStore.userInfo?.real_name || '个人用户' }}
        </h1>
        <p class="welcome-subtitle">
          今天是 {{ currentDate }}，开启您的职业之旅！
        </p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" @click="$router.push('/jobs')">
          寻找工作
        </el-button>
        <el-button @click="$router.push('/tech-service')">
          技术咨询
        </el-button>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><Search /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.job_applications }}</div>
            <div class="stat-label">投递简历</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.consultations }}</div>
            <div class="stat-label">技术咨询</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><Star /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.favorites }}</div>
            <div class="stat-label">收藏内容</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon><Trophy /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.achievements }}</div>
            <div class="stat-label">获得成就</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <h2 class="section-title">快捷操作</h2>
      <div class="actions-grid">
        <div class="action-card" @click="$router.push('/jobs/search')">
          <el-icon class="action-icon"><Search /></el-icon>
          <div class="action-title">找工作</div>
          <div class="action-desc">搜索合适的工作机会</div>
        </div>
        
        <div class="action-card" @click="$router.push('/profile/resume')">
          <el-icon class="action-icon"><Document /></el-icon>
          <div class="action-title">完善简历</div>
          <div class="action-desc">更新个人简历信息</div>
        </div>
        
        <div class="action-card" @click="$router.push('/tech-service/ask')">
          <el-icon class="action-icon"><QuestionFilled /></el-icon>
          <div class="action-title">技术提问</div>
          <div class="action-desc">向专家咨询技术问题</div>
        </div>
        
        <div class="action-card" @click="$router.push('/learning')">
          <el-icon class="action-icon"><Reading /></el-icon>
          <div class="action-title">在线学习</div>
          <div class="action-desc">提升专业技能</div>
        </div>
      </div>
    </div>

    <!-- 推荐内容 -->
    <div class="recommendations">
      <h2 class="section-title">为您推荐</h2>
      <div class="recommendation-tabs">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="推荐职位" name="jobs">
            <div class="job-list">
              <div class="job-item" v-for="job in recommendedJobs" :key="job.id">
                <div class="job-info">
                  <h3 class="job-title">{{ job.title }}</h3>
                  <p class="job-company">{{ job.company }}</p>
                  <div class="job-details">
                    <span class="job-salary">{{ job.salary }}</span>
                    <span class="job-location">{{ job.location }}</span>
                  </div>
                </div>
                <el-button type="primary" size="small">投递简历</el-button>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="技术文章" name="articles">
            <div class="article-list">
              <div class="article-item" v-for="article in recommendedArticles" :key="article.id">
                <div class="article-info">
                  <h3 class="article-title">{{ article.title }}</h3>
                  <p class="article-summary">{{ article.summary }}</p>
                  <div class="article-meta">
                    <span class="article-author">{{ article.author }}</span>
                    <span class="article-time">{{ article.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {
  Search,
  ChatDotRound,
  Star,
  Trophy,
  Document,
  QuestionFilled,
  Reading
} from '@element-plus/icons-vue'

const authStore = useAuthStore()
const activeTab = ref('jobs')

const stats = ref({
  job_applications: 5,
  consultations: 12,
  favorites: 28,
  achievements: 3
})

const recommendedJobs = ref([
  {
    id: 1,
    title: '防腐工程师',
    company: '某防腐科技有限公司',
    salary: '8K-12K',
    location: '北京'
  },
  {
    id: 2,
    title: '保温施工员',
    company: '某建筑工程公司',
    salary: '6K-10K',
    location: '上海'
  },
  {
    id: 3,
    title: '质量检测员',
    company: '某检测机构',
    salary: '5K-8K',
    location: '广州'
  }
])

const recommendedArticles = ref([
  {
    id: 1,
    title: '防腐涂料施工工艺详解',
    summary: '详细介绍防腐涂料的施工步骤和注意事项...',
    author: '张工程师',
    time: '2天前'
  },
  {
    id: 2,
    title: '保温材料选择指南',
    summary: '如何根据不同环境选择合适的保温材料...',
    author: '李专家',
    time: '3天前'
  },
  {
    id: 3,
    title: '工程质量控制要点',
    summary: '防腐保温工程质量控制的关键环节...',
    author: '王总工',
    time: '5天前'
  }
])

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

onMounted(() => {
  // TODO: 获取统计数据和推荐内容
})
</script>

<style scoped>
.individual-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  border-radius: 12px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 16px;
  opacity: 0.9;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.stats-section {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: #f0f9ff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 24px;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
}

.quick-actions {
  margin-bottom: 30px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 32px;
  color: #3b82f6;
  margin-bottom: 12px;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.action-desc {
  font-size: 14px;
  color: #6b7280;
}

.recommendations {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.job-list, .article-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-item, .article-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.job-title, .article-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.job-company {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.job-details {
  display: flex;
  gap: 16px;
}

.job-salary, .job-location {
  font-size: 14px;
  color: #3b82f6;
}

.article-summary {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .job-item, .article-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
