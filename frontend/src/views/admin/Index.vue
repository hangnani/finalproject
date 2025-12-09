<template>
  <div class="admin-dashboard">
    <el-card shadow="hover" class="welcome-card">
      <div slot="header" class="clearfix">
        <span>管理员控制台</span>
      </div>
      <div class="welcome-content">
        <h3>欢迎，{{ user ? user.name : '管理员' }}！</h3>
        <p class="welcome-text">这里是智能校园生活助手的管理员控制台，您可以在这里管理系统数据和测试功能。</p>
        <el-row :gutter="20" class="dashboard-stats">
          <el-col :span="8">
            <el-card class="stat-card" body-style="padding: 15px;">
              <div class="stat-content">
                <div class="stat-icon user-icon">
                  <i class="el-icon-user"></i>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.userCount }}</div>
                  <div class="stat-label">用户总数</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card" body-style="padding: 15px;">
              <div class="stat-content">
                <div class="stat-icon lecture-icon">
                  <i class="el-icon-document"></i>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.lectureCount }}</div>
                  <div class="stat-label">讲座数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card" body-style="padding: 15px;">
              <div class="stat-content">
                <div class="stat-icon exam-icon">
                  <i class="el-icon-edit"></i>
                </div>
                <div class="stat-info">
                  <div class="stat-number">{{ stats.examCount }}</div>
                  <div class="stat-label">考试数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <div class="quick-actions">
          <h4>快速操作</h4>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card class="action-card" @click="$router.push('/admin/users')">
                <div class="action-content">
                  <i class="el-icon-user"></i>
                  <span>用户管理</span>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="action-card" @click="$router.push('/admin/lectures')">
                <div class="action-content">
                  <i class="el-icon-document"></i>
                  <span>讲座管理</span>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="action-card" @click="$router.push('/admin/exams')">
                <div class="action-content">
                  <i class="el-icon-edit"></i>
                  <span>考试管理</span>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="action-card" @click="$router.push('/admin/restaurants')">
                <div class="action-content">
                  <i class="el-icon-s-shop"></i>
                  <span>餐厅管理</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <div class="system-info">
          <h4>系统信息</h4>
          <el-table :data="systemInfo" border style="width: 100%">
            <el-table-column prop="name" label="项目" width="180"></el-table-column>
            <el-table-column prop="value" label="信息"></el-table-column>
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AdminIndex',
  data() {
    return {
      systemInfo: [
        { name: '系统版本', value: 'v1.0.0' },
        { name: '当前用户', value: this.$store.state.user ? this.$store.state.user.name : '管理员' },
        { name: '用户角色', value: this.$store.getters.isAdmin ? '超级管理员' : '管理员' },
        { name: '登录时间', value: new Date().toLocaleString() },
        { name: '服务器状态', value: '运行正常' }
      ],
      // 统计数据
      stats: {
        userCount: 0,
        lectureCount: 0,
        examCount: 0
      }
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  created() {
    // 加载统计数据
    this.loadStats()
  },
  methods: {
    // 加载统计数据
    loadStats() {
      // 获取用户总数
      this.$axios.get('/users/users/').then(response => {
        this.stats.userCount = response.data.count
      }).catch(error => {
        console.error('获取用户总数失败:', error)
      })
      
      // 获取讲座数量
      this.$axios.get('/timetable/lectures/').then(response => {
        this.stats.lectureCount = response.data.count
      }).catch(error => {
        console.error('获取讲座数量失败:', error)
      })
      
      // 获取考试数量
      this.$axios.get('/timetable/exams/').then(response => {
        this.stats.examCount = response.data.count
      }).catch(error => {
        console.error('获取考试数量失败:', error)
      })
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-content {
  text-align: center;
}

.welcome-content h3 {
  color: #333;
  margin-bottom: 10px;
}

.welcome-text {
  color: #666;
  margin-bottom: 30px;
}

.dashboard-stats {
  margin-bottom: 30px;
}

.stat-card {
  border-left: 4px solid #409EFF;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.user-icon {
  background-color: #ecf5ff;
  color: #409EFF;
}

.lecture-icon {
  background-color: #f0f9eb;
  color: #67C23A;
}

.exam-icon {
  background-color: #fef0f0;
  color: #F56C6C;
}

.stat-info {
  flex: 1;
  text-align: left;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.quick-actions {
  margin-bottom: 30px;
  text-align: left;
}

.quick-actions h4 {
  margin-bottom: 15px;
  color: #333;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e4e7ed;
}

.action-card:hover {
  border-color: #409EFF;
  background-color: #ecf5ff;
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.action-content {
  text-align: center;
}

.action-content i {
  font-size: 32px;
  color: #409EFF;
  margin-bottom: 10px;
  display: block;
}

.action-content span {
  font-size: 16px;
  color: #333;
}

.system-info {
  text-align: left;
}

.system-info h4 {
  margin-bottom: 15px;
  color: #333;
}
</style>