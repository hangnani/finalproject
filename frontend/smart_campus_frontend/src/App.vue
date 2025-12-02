<template>
  <div id="app">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="logo">智能校园生活助手</div>
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
  data() {
    return {
      activeMenu: '/',
      user: null
    }
  },
  created() {
    // 从本地存储获取用户信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
    }
    // 设置默认激活菜单
    this.activeMenu = this.$route.path
  },
  watch: {
    // 监听路由变化，更新激活菜单
    $route(to) {
      this.activeMenu = to.path
    }
  },
  methods: {
    handleMenuSelect(key, keyPath) {
      this.activeMenu = key
    },
    logout() {
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.user = null
      // 跳转到登录页
      this.$router.push('/login')
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
}

.el-menu-vertical-demo {
  background-color: #545c64;
  border-right: none;
}

.el-menu-item,
.el-submenu__title {
  color: white;
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
}
</style>
