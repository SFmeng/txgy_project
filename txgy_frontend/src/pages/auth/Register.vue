<template>
  <div class="register-container" role="main" aria-label="用户注册页面">
    <!-- 注册表单区域 -->
    <div class="form-section">
        <div class="form-container">
          <!-- Logo和标题 -->
          <div class="logo-section">
            <div class="logo-icon">
              <el-icon :size="40">
                <Platform />
              </el-icon>
            </div>
            <h1 class="platform-title">防腐保温行业平台</h1>
          </div>

          <!-- 步骤指示器 -->
          <div class="steps-indicator">
            <div class="step" :class="{ active: currentStep >= 1 }">
              <div class="step-number">1</div>
              <div class="step-label">选择类型</div>
            </div>
            <div class="step" :class="{ active: currentStep >= 2 }">
              <div class="step-number">2</div>
              <div class="step-label">基本信息</div>
            </div>
            <div class="step" :class="{ active: currentStep >= 3 }">
              <div class="step-number">3</div>
              <div class="step-label">完成注册</div>
            </div>
          </div>

          <div class="form-header">
            <h2 class="form-title">
              <span v-if="currentStep === 1">选择账户类型</span>
              <span v-else-if="currentStep === 2">填写基本信息</span>
              <span v-else>完成注册</span>
            </h2>
            <p class="form-subtitle">
              <span v-if="currentStep === 1">请选择适合您的账户类型</span>
              <span v-else-if="currentStep === 2">请填写您的基本信息</span>
              <span v-else>确认信息并完成注册</span>
            </p>
          </div>

          <!-- 步骤1: 用户类型选择 -->
          <div class="user-type-selection" v-if="currentStep === 1">
            <div class="type-cards">
              <div
                class="type-card"
                :class="{ active: registerForm.user_type === 'individual' }"
                @click="selectUserType('individual')"
                @keyup.enter="selectUserType('individual')"
                @keyup.space="selectUserType('individual')"
                tabindex="0"
                role="button"
                :aria-pressed="registerForm.user_type === 'individual'"
                aria-label="选择个人用户类型"
              >
                <div class="card-icon">
                  <el-icon :size="28"><User /></el-icon>
                </div>
                <h4>个人用户</h4>
                <p>适合个人技术专家、施工人员等</p>
              </div>

              <div
                class="type-card"
                :class="{ active: registerForm.user_type === 'enterprise' }"
                @click="selectUserType('enterprise')"
                @keyup.enter="selectUserType('enterprise')"
                @keyup.space="selectUserType('enterprise')"
                tabindex="0"
                role="button"
                :aria-pressed="registerForm.user_type === 'enterprise'"
                aria-label="选择企业用户类型"
              >
                <div class="card-icon">
                  <el-icon :size="28"><OfficeBuilding /></el-icon>
                </div>
                <h4>企业用户</h4>
                <p>适合各类防腐保温相关企业</p>
              </div>
            </div>

            <el-button
              type="primary"
              class="next-step-btn"
              :disabled="!registerForm.user_type"
              @click="nextStep"
            >
              下一步
            </el-button>
          </div>

          <!-- 步骤2: 基本信息表单 -->
          <el-form
            v-if="currentStep === 2"
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            class="register-form"
            size="large"
          >
            <el-form-item prop="username">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.username"
                  placeholder="请输入用户名（3-20个字符）"
                  prefix-icon="User"
                  clearable
                  class="modern-input"
                  autocomplete="username"
                  @blur="validateField('username')"
                />
              </div>
            </el-form-item>

            <el-form-item prop="email">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.email"
                  placeholder="请输入邮箱地址"
                  prefix-icon="Message"
                  clearable
                  class="modern-input"
                  autocomplete="email"
                  @blur="validateField('email')"
                />
              </div>
            </el-form-item>

            <el-form-item prop="phone">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.phone"
                  placeholder="请输入手机号"
                  prefix-icon="Phone"
                  clearable
                  class="modern-input"
                  autocomplete="tel"
                />
              </div>
            </el-form-item>



            <el-form-item prop="password">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.password"
                  type="password"
                  placeholder="请输入密码（至少6位）"
                  prefix-icon="Lock"
                  show-password
                  clearable
                  class="modern-input"
                  autocomplete="new-password"
                  @input="debouncedPasswordCheck"
                />
                <div v-if="registerForm.password" class="password-strength">
                  <div class="strength-bar">
                    <div
                      class="strength-fill"
                      :class="passwordStrength.level"
                      :style="{ width: passwordStrength.width }"
                    ></div>
                  </div>
                  <span class="strength-text" :class="passwordStrength.level">
                    {{ passwordStrength.text }}
                  </span>
                </div>
              </div>
            </el-form-item>

            <el-form-item prop="password_confirm">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.password_confirm"
                  type="password"
                  placeholder="请确认密码"
                  prefix-icon="Lock"
                  show-password
                  clearable
                  class="modern-input"
                  autocomplete="new-password"
                />
                <div v-if="registerForm.password_confirm && registerForm.password" class="password-match">
                  <span
                    :class="{
                      'match-success': registerForm.password === registerForm.password_confirm,
                      'match-error': registerForm.password !== registerForm.password_confirm
                    }"
                  >
                    {{ registerForm.password === registerForm.password_confirm ? '✓ 密码匹配' : '✗ 密码不匹配' }}
                  </span>
                </div>
              </div>
            </el-form-item>

            <el-form-item prop="real_name">
              <div class="input-wrapper">
                <el-input
                  v-model="registerForm.real_name"
                  placeholder="请输入真实姓名"
                  prefix-icon="UserFilled"
                  clearable
                  class="modern-input"
                />
              </div>
            </el-form-item>

            <!-- 企业信息 -->
            <template v-if="registerForm.user_type === 'enterprise'">
              <div class="enterprise-section">
                <h4 class="section-subtitle">企业信息</h4>

                <el-form-item prop="company_name">
                  <div class="input-wrapper">
                    <el-input
                      v-model="registerForm.company_name"
                      placeholder="请输入企业名称"
                      prefix-icon="OfficeBuilding"
                      clearable
                      class="modern-input"
                    />
                  </div>
                </el-form-item>

                <el-form-item prop="company_type">
                  <div class="input-wrapper">
                    <el-select
                      v-model="registerForm.company_type"
                      placeholder="请选择企业类型"
                      class="modern-select"
                      style="width: 100%"
                    >
                      <el-option label="生产制造企业" value="manufacturer" />
                      <el-option label="施工安装企业" value="constructor" />
                      <el-option label="工程甲方企业" value="owner" />
                      <el-option label="供应商企业" value="supplier" />
                    </el-select>
                  </div>
                </el-form-item>
              </div>
            </template>

            <div class="form-actions">
              <el-button class="back-btn" @click="prevStep">
                上一步
              </el-button>
              <el-button
                type="primary"
                class="next-btn"
                @click="nextStep"
              >
                下一步
              </el-button>
            </div>
          </el-form>

          <!-- 步骤3: 确认注册 -->
          <div v-if="currentStep === 3" class="confirm-section">
            <div class="info-summary">
              <h4>请确认您的信息</h4>
              <div class="summary-item">
                <span class="label">账户类型：</span>
                <span class="value">{{ registerForm.user_type === 'enterprise' ? '企业用户' : '个人用户' }}</span>
              </div>
              <div class="summary-item">
                <span class="label">用户名：</span>
                <span class="value">{{ registerForm.username }}</span>
              </div>
              <div class="summary-item">
                <span class="label">邮箱：</span>
                <span class="value">{{ registerForm.email }}</span>
              </div>
              <div class="summary-item">
                <span class="label">手机号：</span>
                <span class="value">{{ registerForm.phone }}</span>
              </div>
              <div class="summary-item">
                <span class="label">真实姓名：</span>
                <span class="value">{{ registerForm.real_name }}</span>
              </div>
              <div v-if="registerForm.user_type === 'enterprise'" class="summary-item">
                <span class="label">企业名称：</span>
                <span class="value">{{ registerForm.company_name }}</span>
              </div>
            </div>

            <el-form-item>
              <el-checkbox v-model="registerForm.agree_terms" class="terms-checkbox">
                我已阅读并同意
                <el-link type="primary" @click="showTerms">《用户协议》</el-link>
                和
                <el-link type="primary" @click="showPrivacy">《隐私政策》</el-link>
              </el-checkbox>
            </el-form-item>

            <div class="form-actions">
              <el-button class="back-btn" @click="prevStep">
                上一步
              </el-button>
              <el-button
                type="primary"
                class="register-button"
                :loading="loading"
                :disabled="!registerForm.agree_terms || loading"
                @click="handleRegister"
              >
                <span v-if="!loading">完成注册</span>
                <span v-else>注册中...</span>
              </el-button>
            </div>
          </div>

          <div class="form-footer">
            <p class="login-prompt">
              已有账号？
              <router-link to="/auth/login" class="login-link">
                立即登录
              </router-link>
            </p>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { Platform, User, OfficeBuilding } from '@element-plus/icons-vue'

const router = useRouter()
const registerFormRef = ref()
const loading = ref(false)
const currentStep = ref(1)
const passwordStrength = ref({
  level: 'weak',
  width: '0%',
  text: ''
})
let passwordCheckTimer = null

const registerForm = reactive({
  user_type: '',
  username: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: '',
  real_name: '',
  company_name: '',
  company_type: '',
  agree_terms: false
})

const registerRules = {
  user_type: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3到20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],

  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  company_name: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.user_type === 'enterprise' && !value) {
          callback(new Error('请输入企业名称'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  company_type: [
    {
      validator: (rule, value, callback) => {
        if (registerForm.user_type === 'enterprise' && !value) {
          callback(new Error('请选择企业类型'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

// 步骤控制方法
const selectUserType = (type) => {
  registerForm.user_type = type
}

// 检查密码强度
const checkPasswordStrength = () => {
  const password = registerForm.password
  if (!password) {
    passwordStrength.value = { level: 'weak', width: '0%', text: '' }
    return
  }

  let score = 0
  let feedback = []

  // 长度检查
  if (password.length >= 8) score += 2
  else if (password.length >= 6) score += 1
  else feedback.push('至少6位')

  // 包含数字
  if (/\d/.test(password)) score += 1
  else feedback.push('包含数字')

  // 包含小写字母
  if (/[a-z]/.test(password)) score += 1
  else feedback.push('包含小写字母')

  // 包含大写字母
  if (/[A-Z]/.test(password)) score += 1
  else feedback.push('包含大写字母')

  // 包含特殊字符
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1
  else feedback.push('包含特殊字符')

  // 根据得分设置强度
  if (score <= 2) {
    passwordStrength.value = {
      level: 'weak',
      width: '33%',
      text: '弱 - ' + feedback.slice(0, 2).join('、')
    }
  } else if (score <= 4) {
    passwordStrength.value = {
      level: 'medium',
      width: '66%',
      text: '中等'
    }
  } else {
    passwordStrength.value = {
      level: 'strong',
      width: '100%',
      text: '强'
    }
  }
}

// 防抖密码检查
const debouncedPasswordCheck = () => {
  if (passwordCheckTimer) {
    clearTimeout(passwordCheckTimer)
  }
  passwordCheckTimer = setTimeout(() => {
    checkPasswordStrength()
  }, 300)
}

// 单个字段验证
const validateField = async (field) => {
  try {
    await registerFormRef.value.validateField(field)
  } catch (error) {
    // 验证失败时不需要特殊处理，Element Plus会自动显示错误
  }
}

const nextStep = async () => {
  if (currentStep.value === 1) {
    if (!registerForm.user_type) {
      ElMessage.warning('请选择用户类型')
      return
    }
    currentStep.value = 2
  } else if (currentStep.value === 2) {
    // 验证表单
    if (!registerFormRef.value) return

    try {
      await registerFormRef.value.validate()
      currentStep.value = 3
    } catch (error) {
      console.log('表单验证失败:', error)
    }
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}



// 处理注册
const handleRegister = async () => {
  if (!registerForm.agree_terms) {
    ElMessage.error('请先同意用户协议和隐私政策')
    return
  }

  // 检查密码匹配
  if (registerForm.password !== registerForm.password_confirm) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  try {
    await registerFormRef.value.validate()
    loading.value = true

    const registerData = {
      username: registerForm.username,
      email: registerForm.email,
      phone: registerForm.phone,
      password: registerForm.password,
      password_confirm: registerForm.password_confirm,
      user_type: registerForm.user_type,
      real_name: registerForm.real_name
    }

    // 如果是企业用户，添加企业信息
    if (registerForm.user_type === 'enterprise') {
      registerData.enterprise_info = {
        company_name: registerForm.company_name,
        company_type: registerForm.company_type
      }
    }

    await authAPI.register(registerData)
    ElMessage.success('注册成功！请前往登录页面登录')

    // 延迟跳转，让用户看到成功消息
    setTimeout(() => {
      router.push('/auth/login')
    }, 2000)
  } catch (error) {
    console.error('Register error:', error)

    // 根据错误类型提供更友好的提示
    let errorMessage = '注册失败，请重试'
    if (error.message) {
      if (error.message.includes('用户名')) {
        errorMessage = '用户名已存在，请更换'
      } else if (error.message.includes('邮箱')) {
        errorMessage = '邮箱已被注册，请更换'
      } else if (error.message.includes('手机')) {
        errorMessage = '手机号已被注册，请更换'
      } else if (error.message.includes('网络')) {
        errorMessage = '网络连接失败，请检查网络'
      } else if (error.message.includes('服务器')) {
        errorMessage = '服务器暂时无法访问，请稍后重试'
      } else {
        errorMessage = error.message
      }
    }

    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 显示用户协议
const showTerms = () => {
  ElMessage.info('用户协议功能待实现')
}

// 显示隐私政策
const showPrivacy = () => {
  ElMessage.info('隐私政策功能待实现')
}

onMounted(() => {
  // 设置页面标题
  document.title = '用户注册 - 防腐保温行业平台'
})
</script>

<style scoped>
/* 当使用AuthLayout时，移除背景样式 */





@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表单区域 - 简洁白色风格 */
.form-section {
  width: 100%;
  padding: 0;
}

.form-container {
  width: 100%;
  max-width: 450px;
  margin: 0 auto;
}

@keyframes formSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  border-radius: 14px;
  margin-bottom: 12px;
  color: white;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 20px rgba(255, 119, 48, 0.3);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.platform-title {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 步骤指示器 */
.steps-indicator {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.4;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3d3d3d 0%, #2d2d2d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 6px;
  transition: all 0.3s ease;
  color: #9ca3af;
}

.step.active .step-number {
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(255, 119, 48, 0.4);
}

.step-label {
  font-size: 11px;
  color: #9ca3af;
  font-weight: 500;
}

/* 用户类型选择 */
.user-type-selection {
  width: 100%;
}

.type-cards {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
}

.type-card {
  flex: 1;
  background: rgba(45, 45, 45, 0.8);
  border: 2px solid rgba(120, 119, 198, 0.3);
  border-radius: 16px;
  padding: 24px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.type-card:hover {
  background: rgba(45, 45, 45, 0.9);
  border-color: rgba(255, 119, 48, 0.5);
  transform: translateY(-2px);
}

.type-card.active {
  background: linear-gradient(135deg, rgba(255, 119, 48, 0.2) 0%, rgba(120, 119, 198, 0.2) 100%);
  border-color: #ff7730;
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(255, 119, 48, 0.3);
}

.type-card:focus {
  outline: none;
  border-color: #ff7730;
  box-shadow: 0 0 0 3px rgba(255, 119, 48, 0.2);
}

.card-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  border-radius: 12px;
  margin-bottom: 14px;
  color: white;
}

.type-card.active .card-icon {
  background: linear-gradient(135deg, #7877c6 0%, #ff7730 100%);
}

.type-card h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #ffffff;
}

.type-card p {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
  line-height: 1.4;
}

.next-step-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(255, 119, 48, 0.3);
}

.next-step-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 119, 48, 0.5);
}

.next-step-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}



.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #ff7730 0%, #7877c6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-subtitle {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.register-form {
  margin-bottom: 30px;
}

.input-wrapper {
  position: relative;
  margin-bottom: 4px;
}

.modern-input {
  transition: all 0.3s ease;
}

.modern-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  box-shadow: none;
  transition: all 0.3s ease;
  background: #f9fafb;
}

.modern-input :deep(.el-input__wrapper:hover) {
  border-color: #764ba2;
  background: #ffffff;
}

.modern-input :deep(.el-input__wrapper.is-focus) {
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
  background: #ffffff;
}

.modern-input :deep(.el-input__inner) {
  font-size: 15px;
  color: #374151;
  height: 48px;
}

.modern-input :deep(.el-input__prefix) {
  color: #9ca3af;
}

.modern-select :deep(.el-select__wrapper) {
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  box-shadow: none;
  transition: all 0.3s ease;
  background: #f9fafb;
  height: 52px;
}

.modern-select :deep(.el-select__wrapper:hover) {
  border-color: #764ba2;
  background: #ffffff;
}

.modern-select :deep(.el-select__wrapper.is-focused) {
  border-color: #764ba2;
  box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
  background: #ffffff;
}



.enterprise-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.section-subtitle {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 20px;
  text-align: center;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.back-btn {
  flex: 1;
  height: 48px;
  border-radius: 12px;
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  color: #6b7280;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
  color: #374151;
}

.next-btn {
  flex: 2;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(118, 75, 162, 0.3);
}

/* 确认注册部分 */
.confirm-section {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-summary {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
}

.info-summary h4 {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
  text-align: center;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item .label {
  font-weight: 500;
  color: #6b7280;
  font-size: 14px;
}

.summary-item .value {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.terms-checkbox :deep(.el-checkbox__label) {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.register-button {
  flex: 2;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.register-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.register-button:hover:not(:disabled)::before {
  left: 100%;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(118, 75, 162, 0.3);
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.form-footer {
  text-align: center;
  margin-top: 30px;
}

.login-prompt {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.login-link {
  color: #764ba2;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #667eea;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-section {
    padding: 20px 15px;
  }

  .form-container {
    max-width: 100%;
    padding: 40px 30px;
    border-radius: 20px;
  }

  .platform-title {
    font-size: 18px;
  }

  .form-title {
    font-size: 24px;
  }

  .logo-icon {
    width: 50px;
    height: 50px;
  }

  .steps-indicator {
    gap: 15px;
  }

  .step-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  .step-label {
    font-size: 10px;
  }

  .type-cards {
    flex-direction: column;
    gap: 12px;
  }

  .type-card {
    padding: 20px;
  }

  .card-icon {
    width: 45px;
    height: 45px;
  }

  .form-actions {
    flex-direction: column;
  }

  .back-btn,
  .next-btn,
  .register-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .form-section {
    padding: 15px 10px;
  }

  .form-container {
    padding: 30px 25px;
    border-radius: 16px;
  }

  .platform-title {
    font-size: 16px;
  }

  .form-title {
    font-size: 22px;
  }

  .logo-icon {
    width: 45px;
    height: 45px;
  }

  .steps-indicator {
    gap: 12px;
  }

  .step-number {
    width: 26px;
    height: 26px;
    font-size: 11px;
  }

  .step-label {
    font-size: 9px;
  }
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #ef4444;
}

.strength-fill.medium {
  background: #f59e0b;
}

.strength-fill.strong {
  background: #10b981;
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
  min-width: 60px;
}

.strength-text.weak {
  color: #ef4444;
}

.strength-text.medium {
  color: #f59e0b;
}

.strength-text.strong {
  color: #10b981;
}

/* 密码匹配指示器 */
.password-match {
  margin-top: 6px;
  font-size: 12px;
}

.match-success {
  color: #10b981;
}

.match-error {
  color: #ef4444;
}
</style>
