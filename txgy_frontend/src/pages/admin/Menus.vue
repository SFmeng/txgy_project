<template>
  <div class="admin-menus">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon><Menu /></el-icon>
            菜单管理
          </h1>
          <p class="page-description">管理系统菜单结构，实时控制左侧导航栏</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="handleAdd" class="add-btn">
            <el-icon><Plus /></el-icon>
            新增菜单
          </el-button>
          <el-button @click="handleExpandAll" class="expand-btn">
            <el-icon><Expand /></el-icon>
            展开全部
          </el-button>
          <el-button @click="handleCollapseAll" class="collapse-btn">
            <el-icon><Fold /></el-icon>
            收起全部
          </el-button>
          <el-button type="info" @click="handleRefreshSidebar" class="refresh-btn">
            <el-icon><Refresh /></el-icon>
            手动同步
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索和统计栏 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="18">
          <el-form :model="searchForm" inline class="search-form">
            <el-form-item label="菜单名称">
              <el-input
                v-model="searchForm.menu_name"
                placeholder="请输入菜单名称"
                clearable
                class="search-input"
                prefix-icon="Search"
              />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="菜单状态" clearable class="search-select">
                <el-option label="启用" value="active" />
                <el-option label="禁用" value="inactive" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch" class="search-btn">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="handleReset" class="reset-btn">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="6">
          <div class="stats-info">
            <el-statistic title="菜单总数" :value="getTotalMenuCount()" />
            <el-statistic title="启用菜单" :value="getActiveMenuCount()" />
          </div>
        </el-col>
      </el-row>

      <!-- 调试信息 -->
      <el-divider />
      <div class="debug-info">
        <el-tag type="info">刷新触发器: {{ menuStore.refreshTrigger }}</el-tag>
        <el-tag type="success">侧边栏菜单数: {{ menuStore.menuList.length }}</el-tag>
        <el-tag type="warning">管理菜单数: {{ menuTree.length }}</el-tag>
      </div>
    </el-card>

    <!-- 菜单列表 -->
    <el-card class="data-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon class="header-icon"><Menu /></el-icon>
            <span class="header-title">菜单名称</span>
            <el-tag type="info" class="count-tag">共 {{ getTotalMenuCount() }} 个菜单</el-tag>
          </div>
          <div class="header-right">
            <el-tooltip content="菜单会自动同步到左侧导航栏，如有异常可手动同步" placement="top">
              <el-button type="success" size="small" disabled>
                <el-icon><Warning /></el-icon>
                自动同步
              </el-button>
            </el-tooltip>
          </div>
        </div>
      </template>

      <div class="table-container">
        <el-table
          :data="filteredMenuData"
          row-key="menu_id"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
          :expand-row-keys="expandedKeys"
          @expand-change="handleExpandChange"
          class="menu-table"
          v-loading="loading"
          element-loading-text="加载菜单数据中..."
          default-expand-all
          :row-class-name="getRowClassName"
        >
          <!-- 菜单名称 -->
          <el-table-column prop="menu_name" label="菜单名称" min-width="300" show-overflow-tooltip>
            <template #default="scope">
              <div class="menu-name-cell" :class="getMenuLevelClass(scope.row)">
                <!-- 层级缩进指示器 -->
                <div class="menu-level-indicator">
                  <div v-if="scope.row.parent_id" class="level-line">
                    <div class="indent-line"></div>
                    <div class="branch-line"></div>
                  </div>
                </div>

                <!-- 菜单图标 -->
                <div class="menu-icon-wrapper">
                  <el-icon v-if="scope.row.icon" class="menu-icon">
                    <component :is="scope.row.icon" />
                  </el-icon>
                  <el-icon v-else class="menu-icon default-icon">
                    <Document />
                  </el-icon>
                </div>

                <!-- 菜单名称和标签 -->
                <div class="menu-content">
                  <div class="menu-name-wrapper">
                    <span class="menu-text">{{ scope.row.menu_name }}</span>
                    <el-tag
                      v-if="scope.row.menu_type === 'directory'"
                      type="info"
                      size="small"
                      class="menu-type-tag"
                    >
                      目录
                    </el-tag>
                    <el-tag
                      v-else-if="scope.row.menu_type === 'menu'"
                      type="success"
                      size="small"
                      class="menu-type-tag"
                    >
                      菜单
                    </el-tag>
                    <el-tag
                      v-else
                      type="warning"
                      size="small"
                      class="menu-type-tag"
                    >
                      按钮
                    </el-tag>
                  </div>

                  <!-- 路径信息 -->
                  <div v-if="scope.row.path" class="menu-path">
                    <el-icon class="path-icon"><Link /></el-icon>
                    <span class="path-text">{{ scope.row.path }}</span>
                  </div>
                </div>
              </div>
            </template>
          </el-table-column>

          <!-- 排序 -->
          <el-table-column prop="sort_order" label="排序" width="80" align="center">
            <template #default="scope">
              <el-tag type="info" size="small">{{ scope.row.sort_order || 0 }}</el-tag>
            </template>
          </el-table-column>

          <!-- 组件路径 -->
          <el-table-column prop="component" label="组件路径" min-width="180" show-overflow-tooltip>
            <template #default="scope">
              <el-text class="component-text">{{ scope.row.component || '-' }}</el-text>
            </template>
          </el-table-column>

          <!-- 状态 -->
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template #default="scope">
              <el-switch
                v-model="scope.row.status"
                active-value="active"
                inactive-value="inactive"
                active-text="启用"
                inactive-text="禁用"
                @change="handleToggleStatus(scope.row)"
                :loading="scope.row.statusLoading"
              />
            </template>
          </el-table-column>

          <!-- 操作 -->
          <el-table-column label="操作" width="400" fixed="right">
            <template #default="scope">
              <div class="action-buttons-wrapper">
                <el-button size="small" type="primary" @click="handleEdit(scope.row)" class="action-btn">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button size="small" type="success" @click="handleAddChild(scope.row)" class="action-btn">
                  <el-icon><Plus /></el-icon>
                  新增
                </el-button>
                <el-button size="small" type="warning" @click="handleMoveUp(scope.row)" :disabled="isFirstInLevel(scope.row)" class="action-btn">
                  <el-icon><ArrowUp /></el-icon>
                  上移
                </el-button>
                <el-button size="small" type="warning" @click="handleMoveDown(scope.row)" :disabled="isLastInLevel(scope.row)" class="action-btn">
                  <el-icon><ArrowDown /></el-icon>
                  下移
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(scope.row)" class="action-btn">
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 菜单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑菜单' : '新增菜单'"
      width="700px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="menuFormRef"
        :model="menuForm"
        :rules="menuRules"
        label-width="100px"
        class="menu-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="上级菜单" prop="parent_id">
              <el-tree-select
                v-model="menuForm.parent_id"
                :data="parentMenuOptions"
                :render-after-expand="false"
                placeholder="选择上级菜单"
                check-strictly
                :props="{ value: 'menu_id', label: 'menu_name', children: 'children' }"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单类型" prop="menu_type">
              <el-radio-group v-model="menuForm.menu_type">
                <el-radio value="directory">目录</el-radio>
                <el-radio value="menu">菜单</el-radio>
                <el-radio value="button">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="菜单名称" prop="menu_name">
              <el-input v-model="menuForm.menu_name" placeholder="请输入菜单名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="显示排序" prop="sort_order">
              <el-input-number v-model="menuForm.sort_order" :min="0" :max="999" controls-position="right" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-if="menuForm.menu_type !== 'button'">
          <el-col :span="12">
            <el-form-item label="路由地址" prop="path">
              <el-input v-model="menuForm.path" placeholder="请输入路由地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="menuForm.menu_type === 'menu'">
            <el-form-item label="组件路径" prop="component">
              <el-input v-model="menuForm.component" placeholder="请输入组件路径" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="权限字符" prop="permission">
              <el-input v-model="menuForm.permission" placeholder="请输入权限字符" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="菜单图标" prop="icon">
              <el-input v-model="menuForm.icon" placeholder="请输入图标名称">
                <template #append>
                  <el-button @click="showIconSelector = true">选择</el-button>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="菜单状态" prop="status">
              <el-radio-group v-model="menuForm.status">
                <el-radio value="active">启用</el-radio>
                <el-radio value="inactive">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-if="menuForm.menu_type !== 'button'">
            <el-form-item label="显示状态" prop="is_show">
              <el-radio-group v-model="menuForm.is_show">
                <el-radio :value="true">显示</el-radio>
                <el-radio :value="false">隐藏</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注" prop="remark">
          <el-input v-model="menuForm.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 图标选择器对话框 -->
    <el-dialog v-model="showIconSelector" title="选择图标" width="800px">
      <div class="icon-selector">
        <div class="icon-grid">
          <div 
            v-for="icon in iconList" 
            :key="icon" 
            class="icon-item"
            :class="{ active: menuForm.icon === icon }"
            @click="selectIcon(icon)"
          >
            <el-icon><component :is="icon" /></el-icon>
            <span>{{ icon }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showIconSelector = false">取消</el-button>
        <el-button type="primary" @click="showIconSelector = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMenuStore } from '@/stores/menu'
import {
  Plus, Search, Refresh, Edit, Delete, Expand, Fold, Menu, View, Warning, ArrowUp, ArrowDown,
  Document, Link
} from '@element-plus/icons-vue'

// Store
const menuStore = useMenuStore()

// 响应式数据
const loading = ref(false)
const menuTree = ref([])
const expandedKeys = ref([])
const dialogVisible = ref(false)
const showIconSelector = ref(false)
const isEdit = ref(false)
const submitLoading = ref(false)
const menuFormRef = ref()

// 搜索表单
const searchForm = reactive({
  menu_name: '',
  status: ''
})

// 菜单表单
const menuForm = reactive({
  menu_id: null,
  parent_id: null,
  menu_name: '',
  menu_type: 'menu',
  path: '',
  component: '',
  icon: '',
  sort_order: 0,
  status: 'active',
  is_show: true,
  permission: '',
  remark: ''
})

// 表单验证规则
const menuRules = {
  menu_name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' }
  ],
  menu_type: [
    { required: true, message: '请选择菜单类型', trigger: 'change' }
  ],
  sort_order: [
    { required: true, message: '请输入显示排序', trigger: 'blur' }
  ]
}

// 图标列表
const iconList = [
  'DataBoard', 'User', 'UserFilled', 'Menu', 'OfficeBuilding', 'DocumentChecked', 'Shop',
  'Setting', 'Lock', 'Key', 'Document', 'Folder', 'FolderOpened', 'Files', 'Tickets',
  'Monitor', 'Phone', 'Message', 'ChatDotRound', 'Bell', 'Warning', 'InfoFilled',
  'SuccessFilled', 'CircleClose', 'Plus', 'Minus', 'Edit', 'Delete', 'View', 'Hide',
  'Refresh', 'Search', 'Filter', 'Sort', 'Upload', 'Download', 'Share', 'Star',
  'Collection', 'Flag', 'Location', 'Timer', 'Calendar', 'Clock', 'Stopwatch',
  'Tools', 'Connection', 'Globe', 'Box', 'Lightning', 'CircleCheck', 'RefreshLeft',
  'Check', 'House', 'Operation', 'Cpu', 'UploadFilled'
]

// 计算属性
const filteredMenuData = computed(() => {
  let data = menuTree.value

  if (searchForm.menu_name) {
    data = filterMenuByName(data, searchForm.menu_name)
  }

  if (searchForm.status) {
    data = filterMenuByStatus(data, searchForm.status)
  }

  return data
})

const parentMenuOptions = computed(() => {
  const options = [{ menu_id: null, menu_name: '主类目', children: [] }]
  const buildOptions = (menus, level = 0) => {
    return menus.map(menu => ({
      menu_id: menu.menu_id,
      menu_name: '　'.repeat(level) + menu.menu_name,
      children: menu.children ? buildOptions(menu.children, level + 1) : []
    }))
  }
  options[0].children = buildOptions(menuTree.value)
  return options
})

// 工具函数
const filterMenuByName = (menus, name) => {
  const result = []
  for (const menu of menus) {
    if (menu.menu_name.includes(name)) {
      result.push(menu)
    } else if (menu.children && menu.children.length > 0) {
      const filteredChildren = filterMenuByName(menu.children, name)
      if (filteredChildren.length > 0) {
        result.push({ ...menu, children: filteredChildren })
      }
    }
  }
  return result
}

const filterMenuByStatus = (menus, status) => {
  const result = []
  for (const menu of menus) {
    if (menu.status === status) {
      result.push(menu)
    }
    if (menu.children && menu.children.length > 0) {
      const filteredChildren = filterMenuByStatus(menu.children, status)
      if (filteredChildren.length > 0) {
        result.push({ ...menu, children: filteredChildren })
      }
    }
  }
  return result
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

const getSiblings = (row) => {
  if (!row.parent_id) {
    return menuTree.value.filter(menu => !menu.parent_id)
  }

  const findParent = (menus, parentId) => {
    for (const menu of menus) {
      if (menu.menu_id === parentId) {
        return menu.children || []
      }
      if (menu.children) {
        const found = findParent(menu.children, parentId)
        if (found) return found
      }
    }
    return []
  }

  return findParent(menuTree.value, row.parent_id)
}

const isFirstInLevel = (row) => {
  const siblings = getSiblings(row)
  return siblings.length > 0 && siblings[0].menu_id === row.menu_id
}

const isLastInLevel = (row) => {
  const siblings = getSiblings(row)
  return siblings.length > 0 && siblings[siblings.length - 1].menu_id === row.menu_id
}

// 获取菜单统计
const getTotalMenuCount = () => {
  const countMenus = (menus) => {
    let count = 0
    for (const menu of menus) {
      count++
      if (menu.children) {
        count += countMenus(menu.children)
      }
    }
    return count
  }
  return countMenus(menuTree.value)
}

const getActiveMenuCount = () => {
  const countActiveMenus = (menus) => {
    let count = 0
    for (const menu of menus) {
      if (menu.status === 'active') {
        count++
      }
      if (menu.children) {
        count += countActiveMenus(menu.children)
      }
    }
    return count
  }
  return countActiveMenus(menuTree.value)
}

// 获取菜单层级样式类
const getMenuLevelClass = (menu) => {
  if (!menu.parent_id) {
    return 'menu-level-root'
  }
  return 'menu-level-child'
}

// 获取表格行的样式类名
const getRowClassName = ({ row, rowIndex }) => {
  let className = ''

  // 根据是否有父级添加层级类
  if (row.parent_id) {
    className += 'menu-row-child '
  } else {
    className += 'menu-row-root '
  }

  // 根据菜单类型添加类
  if (row.menu_type === 'directory') {
    className += 'menu-row-directory '
  } else if (row.menu_type === 'menu') {
    className += 'menu-row-menu '
  } else {
    className += 'menu-row-button '
  }

  // 根据状态添加类
  if (row.status === 'inactive') {
    className += 'menu-row-disabled '
  }

  return className.trim()
}

// 事件处理函数
const loadMenuTree = async () => {
  loading.value = true
  try {
    await menuStore.loadMenus()
    menuTree.value = menuStore.menuTree

    // 自动展开所有菜单
    const getAllMenuIds = (menus) => {
      let ids = []
      for (const menu of menus) {
        ids.push(menu.menu_id)
        if (menu.children) {
          ids.push(...getAllMenuIds(menu.children))
        }
      }
      return ids
    }
    expandedKeys.value = getAllMenuIds(menuTree.value)
  } catch (error) {
    console.error('加载菜单失败:', error)
    ElMessage.error('加载菜单失败')
    menuTree.value = []
  } finally {
    loading.value = false
  }
}

const handleExpandChange = (row, expanded) => {
  if (expanded) {
    if (!expandedKeys.value.includes(row.menu_id)) {
      expandedKeys.value.push(row.menu_id)
    }
  } else {
    const index = expandedKeys.value.indexOf(row.menu_id)
    if (index > -1) {
      expandedKeys.value.splice(index, 1)
    }
  }
}

const handleExpandAll = () => {
  const getAllMenuIds = (menus) => {
    let ids = []
    for (const menu of menus) {
      ids.push(menu.menu_id)
      if (menu.children) {
        ids.push(...getAllMenuIds(menu.children))
      }
    }
    return ids
  }
  expandedKeys.value = getAllMenuIds(menuTree.value)
  ElMessage.success('已展开全部菜单')
}

const handleCollapseAll = () => {
  expandedKeys.value = []
  ElMessage.success('已收起全部菜单')
}

const handleSearch = () => {
  ElMessage.success('搜索完成')
}

const handleReset = () => {
  searchForm.menu_name = ''
  searchForm.status = ''
  ElMessage.success('搜索条件已重置')
}

// 状态切换
const handleToggleStatus = async (row) => {
  // 先保存原始状态，以便出错时恢复
  const originalStatus = row.status === 'active' ? 'inactive' : 'active'

  row.statusLoading = true
  try {
    const newStatus = row.status
    const action = newStatus === 'active' ? '启用' : '禁用'

    console.log(`🔄 切换菜单状态: ${row.menu_name} -> ${newStatus}`)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 更新菜单store中的状态，这会自动触发左侧菜单栏的动态更新
    await menuStore.updateMenuStatus(row.menu_id, newStatus)

    // 重新加载菜单数据以确保状态同步
    await loadMenuTree()

    ElMessage.success(`${action}菜单成功`)

    // 不需要手动刷新侧边栏，菜单栏会通过响应式数据自动更新

  } catch (error) {
    console.error('更新菜单状态失败:', error)
    ElMessage.error('更新菜单状态失败')
    // 恢复原状态
    row.status = originalStatus
  } finally {
    row.statusLoading = false
  }
}

// 手动同步侧边栏
const handleRefreshSidebar = async () => {
  try {
    console.log('🔄 手动同步侧边栏...')

    // 强制刷新菜单store
    await menuStore.refreshMenus()

    // 等待一下确保状态更新完成
    await new Promise(resolve => setTimeout(resolve, 200))

    console.log('✅ 侧边栏同步完成')
    ElMessage.success('菜单已手动同步')
  } catch (error) {
    console.error('同步侧边栏失败:', error)
    ElMessage.error('同步侧边栏失败')
  }
}

// 新增菜单
const handleAdd = () => {
  resetForm()
  isEdit.value = false
  dialogVisible.value = true
}

// 新增子菜单
const handleAddChild = (row) => {
  resetForm()
  menuForm.parent_id = row.menu_id
  isEdit.value = false
  dialogVisible.value = true
}

// 编辑菜单
const handleEdit = (row) => {
  resetForm()
  Object.assign(menuForm, {
    menu_id: row.menu_id,
    parent_id: row.parent_id,
    menu_name: row.menu_name,
    menu_type: row.menu_type || 'menu',
    path: row.path || '',
    component: row.component || '',
    icon: row.icon || '',
    sort_order: row.sort_order || 0,
    status: row.status || 'active',
    is_show: row.is_show !== false,
    permission: row.permission || '',
    remark: row.remark || ''
  })
  isEdit.value = true
  dialogVisible.value = true
}

// 删除菜单
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除菜单"${row.menu_name}"吗？删除后不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    loading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    // 更新菜单store，这会自动触发左侧菜单栏的动态更新
    await menuStore.deleteMenu(row.menu_id)

    ElMessage.success('删除菜单成功')

    // 重新加载菜单数据
    await loadMenuTree()

    // 菜单栏会通过响应式数据自动更新，无需手动刷新

  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除菜单失败:', error)
      ElMessage.error('删除菜单失败')
    }
  } finally {
    loading.value = false
  }
}

// 上移菜单
const handleMoveUp = async (row) => {
  try {
    const siblings = getSiblings(row)
    const currentIndex = siblings.findIndex(menu => menu.menu_id === row.menu_id)

    if (currentIndex > 0) {
      // 交换排序
      const prevMenu = siblings[currentIndex - 1]
      const tempOrder = row.sort_order
      row.sort_order = prevMenu.sort_order
      prevMenu.sort_order = tempOrder

      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 300))

      ElMessage.success('菜单上移成功')
      await loadMenuTree()

      // 菜单栏会通过响应式数据自动更新排序
    }
  } catch (error) {
    console.error('菜单上移失败:', error)
    ElMessage.error('菜单上移失败')
  }
}

// 下移菜单
const handleMoveDown = async (row) => {
  try {
    const siblings = getSiblings(row)
    const currentIndex = siblings.findIndex(menu => menu.menu_id === row.menu_id)

    if (currentIndex < siblings.length - 1) {
      // 交换排序
      const nextMenu = siblings[currentIndex + 1]
      const tempOrder = row.sort_order
      row.sort_order = nextMenu.sort_order
      nextMenu.sort_order = tempOrder

      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 300))

      ElMessage.success('菜单下移成功')
      await loadMenuTree()

      // 菜单栏会通过响应式数据自动更新排序
    }
  } catch (error) {
    console.error('菜单下移失败:', error)
    ElMessage.error('菜单下移失败')
  }
}

// 表单提交
const handleSubmit = async () => {
  try {
    await menuFormRef.value.validate()

    submitLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    if (isEdit.value) {
      await menuStore.updateMenu(menuForm.menu_id, menuForm)
      ElMessage.success('更新菜单成功')
    } else {
      await menuStore.createMenu(menuForm)
      ElMessage.success('创建菜单成功')
    }

    dialogVisible.value = false

    // 重新加载菜单数据
    await loadMenuTree()

    // 菜单栏会通过响应式数据自动更新，无需手动刷新

  } catch (error) {
    console.error('保存菜单失败:', error)
    ElMessage.error('保存菜单失败')
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(menuForm, {
    menu_id: null,
    parent_id: null,
    menu_name: '',
    menu_type: 'menu',
    path: '',
    component: '',
    icon: '',
    sort_order: 0,
    status: 'active',
    is_show: true,
    permission: '',
    remark: ''
  })

  if (menuFormRef.value) {
    menuFormRef.value.clearValidate()
  }
}

// 选择图标
const selectIcon = (icon) => {
  menuForm.icon = icon
}

// 生命周期
onMounted(() => {
  loadMenuTree()
})
</script>

<style scoped>
.admin-menus {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-description {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.add-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.add-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.expand-btn, .collapse-btn, .refresh-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.expand-btn:hover, .collapse-btn:hover, .refresh-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

/* 搜索卡片 */
.search-card {
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.search-form {
  margin: 0;
}

.search-input, .search-select {
  width: 200px;
}

.stats-info {
  display: flex;
  gap: 40px;
  justify-content: flex-end;
  align-items: center;
}

/* 调试信息 */
.debug-info {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 8px 0;
}

.debug-info .el-tag {
  font-size: 12px;
}

/* 数据卡片 */
.data-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #409eff;
  font-size: 18px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.count-tag {
  margin-left: 8px;
}

/* 表格样式 */
.menu-table {
  width: 100%;
}

/* 菜单名称单元格样式 */
.menu-name-cell {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 0;
  min-height: 60px;
}

/* 根级菜单样式 */
.menu-level-root {
  background: linear-gradient(90deg, rgba(64, 158, 255, 0.05) 0%, transparent 100%);
  border-left: 3px solid #409eff;
  padding-left: 12px;
  margin-left: -12px;
}

/* 子级菜单样式 */
.menu-level-child {
  background: linear-gradient(90deg, rgba(103, 194, 58, 0.05) 0%, transparent 100%);
  border-left: 3px solid #67c23a;
  padding-left: 12px;
  margin-left: 30px;
  position: relative;
}

.menu-level-child::before {
  content: '';
  position: absolute;
  left: -30px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #e4e7ed 0%, #e4e7ed 80%, transparent 80%);
}

/* 层级指示器 */
.menu-level-indicator {
  display: flex;
  align-items: center;
  width: 20px;
  height: 100%;
  position: relative;
}

.level-line {
  position: relative;
  width: 100%;
  height: 100%;
}

.indent-line {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 1px;
  background: #e4e7ed;
}

.branch-line {
  position: absolute;
  left: 0;
  top: 50%;
  width: 12px;
  height: 1px;
  background: #e4e7ed;
}

.branch-line::before {
  content: '';
  position: absolute;
  right: -3px;
  top: -2px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #67c23a;
}

/* 菜单图标包装器 */
.menu-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(64, 158, 255, 0.1);
  flex-shrink: 0;
}

.menu-icon {
  color: #409eff;
  font-size: 16px;
}

.default-icon {
  color: #909399;
}

/* 菜单内容 */
.menu-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-name-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.menu-text {
  font-weight: 500;
  font-size: 14px;
  color: #303133;
}

.menu-type-tag {
  font-size: 10px;
  height: 18px;
  line-height: 16px;
  padding: 0 6px;
}

/* 路径信息 */
.menu-path {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
  width: fit-content;
}

.path-icon {
  font-size: 12px;
}

.path-text {
  font-family: 'Courier New', monospace;
}

.table-icon {
  color: #409eff;
  font-size: 18px;
}

.no-icon {
  color: #c0c4cc;
  font-style: italic;
}

.permission-text {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  background: #f0f9ff;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e1f5fe;
}

.component-text {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #666;
}

/* 表单样式 */
.menu-form {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}

/* 图标选择器 */
.icon-selector {
  max-height: 400px;
  overflow-y: auto;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  padding: 12px;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
}

.icon-item:hover {
  border-color: #409eff;
  background: #ecf5ff;
  transform: translateY(-2px);
}

.icon-item.active {
  border-color: #409eff;
  background: #409eff;
  color: white;
}

.icon-item .el-icon {
  font-size: 24px;
}

.icon-item span {
  font-size: 12px;
  text-align: center;
  word-break: break-all;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-menus {
    padding: 12px;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .search-form {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input, .search-select {
    width: 100%;
  }

  .stats-info {
    justify-content: flex-start;
    gap: 20px;
  }

  .icon-grid {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  }
}

/* 动画效果 */
.el-table__row {
  transition: all 0.3s ease;
}

.el-table__row:hover {
  background-color: #f5f7fa !important;
}

/* 表格行高度调整 */
.menu-table .el-table__row {
  height: auto;
}

.menu-table .el-table__cell {
  padding: 12px 0;
}

/* 根菜单行样式 */
.menu-table .menu-row-root {
  background-color: rgba(64, 158, 255, 0.02);
  border-left: 3px solid transparent;
}

.menu-table .menu-row-root:hover {
  background-color: rgba(64, 158, 255, 0.08) !important;
  border-left-color: #409eff;
}

/* 子菜单行样式 */
.menu-table .menu-row-child {
  background-color: rgba(103, 194, 58, 0.02);
  border-left: 3px solid transparent;
  position: relative;
}

.menu-table .menu-row-child:hover {
  background-color: rgba(103, 194, 58, 0.08) !important;
  border-left-color: #67c23a;
}

.menu-table .menu-row-child::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(to bottom, #e4e7ed 0%, #e4e7ed 50%, transparent 50%);
}

/* 目录类型行样式 */
.menu-table .menu-row-directory {
  font-weight: 600;
}

/* 禁用菜单行样式 */
.menu-table .menu-row-disabled {
  opacity: 0.6;
  background-color: rgba(245, 108, 108, 0.05) !important;
}

.menu-table .menu-row-disabled:hover {
  background-color: rgba(245, 108, 108, 0.1) !important;
}

.el-button-group .el-button {
  margin: 0;
}

.el-button-group .el-button + .el-button {
  margin-left: 0;
}

/* 加载状态 */
.table-container {
  position: relative;
  min-height: 200px;
}

/* 状态开关样式 */
.el-switch {
  --el-switch-on-color: #13ce66;
  --el-switch-off-color: #ff4949;
}

/* 统计信息样式 */
.el-statistic {
  text-align: center;
}

.el-statistic__content {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
}

.el-statistic__title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

/* 操作按钮样式 */
.action-buttons-wrapper {
  display: flex;
  flex-wrap: nowrap;
  gap: 3px;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0 4px;
}

.action-btn {
  padding: 3px 6px !important;
  font-size: 11px !important;
  min-width: auto !important;
  white-space: nowrap;
  flex-shrink: 0;
  height: 24px !important;
  line-height: 1 !important;
}

.action-btn .el-icon {
  margin-right: 2px !important;
  font-size: 11px !important;
}

/* 确保操作列内容不换行 */
.el-table .el-table__cell {
  white-space: nowrap;
}

/* 操作列特定样式 */
.el-table__fixed-right {
  background: #fff;
}
</style>
