<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="logo">智能校园生活助手</div>
        <div class="header-actions">
          <!-- 主题切换按钮 -->
          <el-button 
            type="text" 
            icon="el-icon-moon" 
            @click="toggleTheme"
            title="切换主题"
          >
            {{ isDarkMode ? '浅色模式' : '深色模式' }}
          </el-button>
          <div class="user-info">
            <el-dropdown>
              <span class="el-dropdown-link">
                {{ user ? user.name : '未登录' }} <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click="$router.push('/profile')">个人中心</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-container>
        <!-- 侧边栏导航 -->
        <el-aside width="200px" class="aside">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            router
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">
              <i class="el-icon-s-home"></i>
              <span slot="title">首页</span>
            </el-menu-item>
            
            <!-- 二手交易 -->
            <el-submenu index="/secondhand">
              <template slot="title">
                <i class="el-icon-s-goods"></i>
                <span>二手交易</span>
              </template>
              <el-menu-item index="/secondhand">商品列表</el-menu-item>
              <el-menu-item index="/secondhand/publish">发布商品</el-menu-item>
              <el-menu-item index="/secondhand/my-products">我的发布</el-menu-item>
            </el-submenu>
            
            <!-- 课程表管理 -->
            <el-submenu index="/timetable">
              <template slot="title">
                <i class="el-icon-document"></i>
                <span>课程表</span>
              </template>
              <el-menu-item index="/timetable">我的课程</el-menu-item>
              <el-menu-item index="/timetable/add">添加课程</el-menu-item>
              <el-menu-item index="/timetable/import">导入课程</el-menu-item>
            </el-submenu>
            
            <!-- 校园点餐 -->
            <el-submenu index="/foodorder">
              <template slot="title">
                <i class="el-icon-s-shop"></i>
                <span>校园点餐</span>
              </template>
              <el-menu-item index="/foodorder/restaurants">餐厅列表</el-menu-item>
              <el-menu-item index="/foodorder/cart">购物车</el-menu-item>
              <el-menu-item index="/foodorder/orders">我的订单</el-menu-item>
            </el-submenu>
          </el-menu>
        </el-aside>
        
        <!-- 主内容区域 -->
        <el-main class="main">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    },
    user() {
      return this.$store.state.user
    },
    isDarkMode() {
      return this.$store.getters.isDarkMode
    }
  },
  created() {
    // 从localStorage初始化Vuex状态
    this.initUser()
    // 监听系统主题变化
    this.initTheme()
  },
  methods: {
    handleMenuSelect(key, keyPath) {
      // 菜单选择由路由自动处理
    },
    logout() {
      // 使用Vuex logout action
      this.$store.dispatch('logout')
      // 跳转到登录页
      this.$router.push('/login')
    },
    // 切换主题
    toggleTheme() {
      this.$store.dispatch('toggleTheme')
    },
    // 初始化用户信息
    initUser() {
      const token = localStorage.getItem('token')
      const userStr = localStorage.getItem('user')
      if (token && userStr) {
        try {
          const user = JSON.parse(userStr)
          this.$store.commit('SET_TOKEN', token)
          this.$store.commit('SET_USER', user)
        } catch (error) {
          console.error('解析用户信息失败:', error)
          // 清除无效的本地存储
          localStorage.removeItem('token')
          localStorage.removeItem('user')
        }
      }
    },
    // 初始化主题
    initTheme() {
      // 检查系统主题偏好
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        this.$store.commit('SET_THEME', 'dark')
      }
      // 监听系统主题变化
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        this.$store.commit('SET_THEME', e.matches ? 'dark' : 'light')
      })
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  margin: 0;
  transition: all 0.3s ease;
}

/* 深色模式 */
#app.dark-mode {
  background-color: #1a1a1a;
  color: #e0e0e0;
}

.el-container {
  height: 100vh;
}

.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  cursor: pointer;
}

.aside {
  background-color: #545c64;
  color: white;
  transition: all 0.3s ease;
}

.el-menu-vertical-demo {
  background-color: #545c64;
  border-right: none;
  transition: all 0.3s ease;
}

.el-menu-item,
.el-submenu__title {
  color: white;
  transition: all 0.3s ease;
}

.el-menu-item:hover,
.el-submenu__title:hover {
  background-color: #616e7c;
}

.el-menu-item.is-active {
  background-color: #409EFF;
  color: white;
}

.main {
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
  transition: all 0.3s ease;
}

/* 深色模式下的样式覆盖 */
#app.dark-mode .main {
  background-color: #2c2c2c;
}

#app.dark-mode .aside {
  background-color: #2c2c2c;
}

#app.dark-mode .el-menu-vertical-demo {
  background-color: #2c2c2c;
}

#app.dark-mode .el-menu-item,
#app.dark-mode .el-submenu__title {
  color: #e0e0e0;
}

#app.dark-mode .el-menu-item:hover,
#app.dark-mode .el-submenu__title:hover {
  background-color: #3a3a3a;
}

#app.dark-mode .el-card {
  background-color: #3a3a3a;
  border-color: #4a4a4a;
  color: #e0e0e0;
}

#app.dark-mode .el-input__inner,
#app.dark-mode .el-select-dropdown {
  background-color: #3a3a3a;
  border-color: #4a4a4a;
  color: #e0e0e0;
}

#app.dark-mode .el-table {
  background-color: #3a3a3a;
  color: #e0e0e0;
}

#app.dark-mode .el-table th,
#app.dark-mode .el-table tr {
  background-color: #3a3a3a;
  border-bottom-color: #4a4a4a;
}

#app.dark-mode .el-dialog {
  background-color: #3a3a3a;
  color: #e0e0e0;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
