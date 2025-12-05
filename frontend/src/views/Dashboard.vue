<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2>校园生活数据看板</h2>
      <div class="header-actions">
        <el-select v-model="timeRange" placeholder="选择时间范围" @change="handleTimeRangeChange">
          <el-option label="本周" value="week"></el-option>
          <el-option label="本月" value="month"></el-option>
          <el-option label="本学期" value="semester"></el-option>
        </el-select>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-info">
            <h3>{{ stats.totalOrders }}</h3>
            <p>外卖订单数</p>
          </div>
          <div class="stat-icon order-icon">
            <i class="el-icon-shopping-cart-2"></i>
          </div>
        </div>
        <div class="stat-change">
          <span class="change-text">环比 {{ stats.orderChange }}%</span>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-info">
            <h3>¥{{ stats.totalSpent }}</h3>
            <p>总消费金额</p>
          </div>
          <div class="stat-icon spend-icon">
            <i class="el-icon-money"></i>
          </div>
        </div>
        <div class="stat-change">
          <span class="change-text">环比 {{ stats.spentChange }}%</span>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-info">
            <h3>{{ stats.totalCourses }}</h3>
            <p>本周课程数</p>
          </div>
          <div class="stat-icon course-icon">
            <i class="el-icon-document"></i>
          </div>
        </div>
        <div class="stat-change">
          <span class="change-text">环比 {{ stats.courseChange }}%</span>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-info">
            <h3>{{ stats.totalPoints }}</h3>
            <p>当前积分</p>
          </div>
          <div class="stat-icon point-icon">
            <i class="el-icon-medal"></i>
          </div>
        </div>
        <div class="stat-change">
          <span class="change-text">环比 {{ stats.pointChange }}%</span>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-row">
        <el-card shadow="hover" class="chart-card">
          <h3 class="chart-title">消费趋势</h3>
          <div class="chart-container">
            <div class="chart-placeholder">消费趋势图表</div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="chart-card">
          <h3 class="chart-title">课程分布</h3>
          <div class="chart-container">
            <div class="chart-placeholder">课程分布图表</div>
          </div>
        </el-card>
      </div>
      
      <div class="chart-row">
        <el-card shadow="hover" class="chart-card">
          <h3 class="chart-title">积分获取记录</h3>
          <div class="chart-container">
            <div class="chart-placeholder">积分记录图表</div>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="chart-card">
          <h3 class="chart-title">学习-生活平衡</h3>
          <div class="chart-container">
            <div class="balance-meter">
              <div class="meter-header">
                <span>学习时间</span>
                <span>{{ balance.learningTime }}h</span>
              </div>
              <el-progress 
                :percentage="balance.learningPercentage" 
                :stroke-width="20" 
                :color="['#409EFF', '#67C23A']"
              ></el-progress>
              <div class="meter-footer">
                <span>生活时间</span>
                <span>{{ balance.lifeTime }}h</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <el-card shadow="hover" class="activity-card">
      <h3 class="section-title">最近活动</h3>
      <div class="activity-list">
        <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
          <div class="activity-icon" :class="activity.type"></div>
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <span class="activity-time">{{ formatTime(activity.time) }}</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapState(['userPoints'])
  },
  data() {
    return {
      timeRange: 'week',
      stats: {
        totalOrders: 12,
        orderChange: 15,
        totalSpent: 180,
        spentChange: 10,
        totalCourses: 25,
        courseChange: 5,
        totalPoints: 0,
        pointChange: 20
      },
      balance: {
        learningTime: 35,
        lifeTime: 45,
        learningPercentage: 44
      },
      recentActivities: [
        {
          id: 1,
          title: '购买外卖',
          description: '在学生餐厅购买了一份宫保鸡丁盖饭',
          time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          type: 'order'
        },
        {
          id: 2,
          title: '完成课程',
          description: '完成了高等数学课程',
          time: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
          type: 'course'
        },
        {
          id: 3,
          title: '获得积分',
          description: '发布二手商品获得了5积分',
          time: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
          type: 'points'
        },
        {
          id: 4,
          title: '购买外卖',
          description: '在清真餐厅购买了一份牛肉拉面',
          time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
          type: 'order'
        },
        {
          id: 5,
          title: '完成课程',
          description: '完成了大学英语课程',
          time: new Date(Date.now() - 26 * 60 * 60 * 1000).toISOString(),
          type: 'course'
        }
      ]
    }
  },
  watch: {
    // 监听userPoints变化，更新stats中的totalPoints
    userPoints(newPoints) {
      this.stats.totalPoints = newPoints
    }
  },
  created() {
    // 初始化时将Vuex中的userPoints赋值给stats
    this.stats.totalPoints = this.userPoints
  },
  methods: {
    handleTimeRangeChange() {
      // 模拟不同时间范围的数据变化
      this.$message.success(`已切换到${this.timeRange}数据`)
    },
    formatTime(timeString) {
      const date = new Date(timeString)
      const now = new Date()
      const diff = now - date
      
      const minutes = Math.floor(diff / (1000 * 60))
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (minutes < 60) {
        return `${minutes}分钟前`
      } else if (hours < 24) {
        return `${hours}小时前`
      } else if (days < 7) {
        return `${days}天前`
      } else {
        return date.toLocaleDateString()
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  transition: all 0.3s ease;
  border-radius: 8px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-info h3 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-info p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.order-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.spend-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.course-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.point-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-change {
  margin-top: 16px;
  text-align: right;
}

.change-text {
  font-size: 14px;
  color: #67c23a;
  font-weight: bold;
}

.charts-section {
  margin-bottom: 24px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chart-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 4px;
}

.chart-placeholder {
  color: #909399;
  font-size: 16px;
}

.balance-meter {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.meter-header, .meter-footer {
  display: flex;
  justify-content: space-between;
  margin: 16px 0;
  font-size: 14px;
  color: #606266;
}

.activity-card {
  border-radius: 8px;
  margin-bottom: 24px;
}

.section-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: #f0f0f0;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409EFF;
  flex-shrink: 0;
}

.activity-icon.order {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.activity-icon.course {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.activity-icon.points {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.activity-content p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.activity-time {
  font-size: 12px;
  color: #909399;
}

/* 深色模式 */
:deep(.dark-mode) .page-header h2 {
  color: #e0e0e0;
}

:deep(.dark-mode) .stat-info h3 {
  color: #e0e0e0;
}

:deep(.dark-mode) .stat-info p {
  color: #999;
}

:deep(.dark-mode) .chart-title {
  color: #e0e0e0;
}

:deep(.dark-mode) .chart-container {
  background: #333;
}

:deep(.dark-mode) .section-title {
  color: #e0e0e0;
}

:deep(.dark-mode) .activity-item {
  background: #333;
}

:deep(.dark-mode) .activity-content h4 {
  color: #e0e0e0;
}

:deep(.dark-mode) .activity-content p {
  color: #999;
}

:deep(.dark-mode) .activity-item:hover {
  background: #444;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>