<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <div slot="header" class="welcome-header">
        <h3>欢迎回来，{{ user ? user.name : '用户' }}</h3>
      </div>
      <div class="welcome-content">
        <p>智能校园生活助手为您提供二手交易、课程表管理和校园点餐三大核心功能，让您的校园生活更加便捷！</p>
      </div>
    </el-card>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon secondhand">
              <i class="el-icon-s-goods"></i>
            </div>
            <div class="stat-info">
              <h4>二手交易</h4>
              <p class="stat-number">{{ secondhandStats.productCount }}</p>
              <p class="stat-desc">件商品</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon timetable">
              <i class="el-icon-document"></i>
            </div>
            <div class="stat-info">
              <h4>课程表</h4>
              <p class="stat-number">{{ timetableStats.courseCount }}</p>
              <p class="stat-desc">门课程</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon foodorder">
              <i class="el-icon-s-shop"></i>
            </div>
            <div class="stat-info">
              <h4>校园点餐</h4>
              <p class="stat-number">{{ foodorderStats.restaurantCount }}</p>
              <p class="stat-desc">家餐厅</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="quick-actions-row">
      <el-col :span="12">
        <el-card class="action-card">
          <div slot="header" class="action-header">
            <h4>快速操作</h4>
          </div>
          <div class="action-content">
            <el-button
              type="primary"
              icon="el-icon-s-goods"
              class="action-button"
              @click="$router.push('/secondhand/publish')"
            >
              发布二手商品
            </el-button>
            <el-button
              type="success"
              icon="el-icon-document"
              class="action-button"
              @click="$router.push('/timetable/add')"
            >
              添加课程
            </el-button>
            <el-button
              type="warning"
              icon="el-icon-s-shop"
              class="action-button"
              @click="$router.push('/foodorder/restaurants')"
            >
              浏览餐厅
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="action-card">
          <div slot="header" class="action-header">
            <h4>最近动态</h4>
          </div>
          <div class="recent-activities">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in recentActivities"
                :key="index"
                :timestamp="activity.time"
                placement="top"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      user: null,
      secondhandStats: {
        productCount: 0
      },
      timetableStats: {
        courseCount: 0
      },
      foodorderStats: {
        restaurantCount: 0
      },
      recentActivities: [
        { time: '今天 10:30', content: '您发布了一件二手商品：《Python编程从入门到精通》' },
        { time: '昨天 14:20', content: '您添加了一门新课程：高等数学' },
        { time: '昨天 12:00', content: '您完成了一笔订单，订单号：20251126001' },
        { time: '11月25日', content: '您收藏了一件二手商品：无线鼠标' }
      ]
    }
  },
  created() {
    // 从本地存储获取用户信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
    }
    
    // 获取统计数据
    this.getStats()
  },
  methods: {
    getStats() {
      // 这里应该调用 API 获取实际的统计数据
      // 暂时使用模拟数据
      this.secondhandStats.productCount = 128
      this.timetableStats.courseCount = 8
      this.foodorderStats.restaurantCount = 15
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 0;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-content {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 150px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px 0 rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  height: 110px;
}

.stat-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 32px;
  margin-right: 20px;
  color: white;
}

.stat-icon.secondhand {
  background-color: #409EFF;
}

.stat-icon.timetable {
  background-color: #67C23A;
}

.stat-icon.foodorder {
  background-color: #E6A23C;
}

.stat-info h4 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.stat-number {
  margin: 0 0 5px 0;
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-desc {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.quick-actions-row {
  margin-bottom: 20px;
}

.action-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-button {
  margin-bottom: 10px;
}

.recent-activities {
  max-height: 200px;
  overflow-y: auto;
}
</style>