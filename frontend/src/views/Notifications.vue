<template>
  <div class="notifications-container">
    <div class="page-header">
      <h2>通知中心</h2>
      <div class="header-actions">
        <el-button type="primary" @click="markAllAsRead" :disabled="unreadCount === 0">
          全部已读
        </el-button>
        <el-button @click="clearAllNotifications">清空通知</el-button>
      </div>
    </div>
    
    <el-tabs v-model="activeTab" class="notifications-tabs">
      <el-tab-pane label="全部通知" name="all">
        <div class="notifications-list">
          <div v-if="notifications.length === 0" class="empty-state">
            <el-empty description="暂无通知"></el-empty>
          </div>
          <el-card 
            v-for="notification in notifications" 
            :key="notification.id" 
            class="notification-card" 
            shadow="hover"
            :class="{ 'unread': !notification.read }"
            @click="markAsRead(notification)"
          >
            <div class="notification-content">
              <div class="notification-header">
                <div class="notification-type" :class="notification.type">
                  <i :class="getNotificationIcon(notification.type)"></i>
                  <span>{{ getNotificationTypeName(notification.type) }}</span>
                </div>
                <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
              </div>
              <div class="notification-body">
                <h4>{{ notification.title }}</h4>
                <p>{{ notification.content }}</p>
              </div>
              <div v-if="notification.data" class="notification-data">
                <div class="data-item" v-for="(value, key) in notification.data" :key="key">
                  <span class="data-label">{{ key }}:</span>
                  <span class="data-value">{{ value }}</span>
                </div>
              </div>
              <div class="notification-actions" v-if="notification.actions && notification.actions.length > 0">
                <el-button 
                  v-for="action in notification.actions" 
                  :key="action.id" 
                  :type="action.type" 
                  size="small"
                  @click.stop="handleAction(action, notification)"
                >
                  {{ action.text }}
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="未读通知" name="unread">
        <div class="notifications-list">
          <div v-if="unreadNotifications.length === 0" class="empty-state">
            <el-empty description="暂无未读通知"></el-empty>
          </div>
          <el-card 
            v-for="notification in unreadNotifications" 
            :key="notification.id" 
            class="notification-card" 
            shadow="hover"
            :class="{ 'unread': !notification.read }"
            @click="markAsRead(notification)"
          >
            <div class="notification-content">
              <div class="notification-header">
                <div class="notification-type" :class="notification.type">
                  <i :class="getNotificationIcon(notification.type)"></i>
                  <span>{{ getNotificationTypeName(notification.type) }}</span>
                </div>
                <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
              </div>
              <div class="notification-body">
                <h4>{{ notification.title }}</h4>
                <p>{{ notification.content }}</p>
              </div>
              <div v-if="notification.data" class="notification-data">
                <div class="data-item" v-for="(value, key) in notification.data" :key="key">
                  <span class="data-label">{{ key }}:</span>
                  <span class="data-value">{{ value }}</span>
                </div>
              </div>
              <div class="notification-actions" v-if="notification.actions && notification.actions.length > 0">
                <el-button 
                  v-for="action in notification.actions" 
                  :key="action.id" 
                  :type="action.type" 
                  size="small"
                  @click.stop="handleAction(action, notification)"
                >
                  {{ action.text }}
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="通知分类" name="categories">
        <el-card shadow="hover" class="category-card">
          <el-menu class="category-menu" @select="handleCategorySelect">
            <el-menu-item index="course">
              <i class="el-icon-document"></i>
              <span slot="title">课程提醒 ({{ getCategoryCount('course') }})</span>
            </el-menu-item>
            <el-menu-item index="order">
              <i class="el-icon-shopping-cart-2"></i>
              <span slot="title">外卖订单 ({{ getCategoryCount('order') }})</span>
            </el-menu-item>
            <el-menu-item index="secondhand">
              <i class="el-icon-s-goods"></i>
              <span slot="title">二手交易 ({{ getCategoryCount('secondhand') }})</span>
            </el-menu-item>
            <el-menu-item index="points">
              <i class="el-icon-medal"></i>
              <span slot="title">积分变动 ({{ getCategoryCount('points') }})</span>
            </el-menu-item>
            <el-menu-item index="system">
              <i class="el-icon-message"></i>
              <span slot="title">系统通知 ({{ getCategoryCount('system') }})</span>
            </el-menu-item>
          </el-menu>
          
          <div class="category-content">
            <div v-if="selectedCategoryNotifications.length === 0" class="empty-state">
              <el-empty description="暂无该类型通知"></el-empty>
            </div>
            <el-card 
              v-for="notification in selectedCategoryNotifications" 
              :key="notification.id" 
              class="notification-card" 
              shadow="hover"
              :class="{ 'unread': !notification.read }"
              @click="markAsRead(notification)"
            >
              <div class="notification-content">
                <div class="notification-header">
                  <div class="notification-type" :class="notification.type">
                    <i :class="getNotificationIcon(notification.type)"></i>
                    <span>{{ getNotificationTypeName(notification.type) }}</span>
                  </div>
                  <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
                </div>
                <div class="notification-body">
                  <h4>{{ notification.title }}</h4>
                  <p>{{ notification.content }}</p>
                </div>
                <div v-if="notification.data" class="notification-data">
                  <div class="data-item" v-for="(value, key) in notification.data" :key="key">
                    <span class="data-label">{{ key }}:</span>
                    <span class="data-value">{{ value }}</span>
                  </div>
                </div>
                <div class="notification-actions" v-if="notification.actions && notification.actions.length > 0">
                  <el-button 
                    v-for="action in notification.actions" 
                    :key="action.id" 
                    :type="action.type" 
                    size="small"
                    @click.stop="handleAction(action, notification)"
                  >
                    {{ action.text }}
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: 'Notifications',
  data() {
    return {
      activeTab: 'all',
      selectedCategory: '',
      notifications: [
        {
          id: 1,
          title: '课程提醒',
          content: '您的高等数学课程将在15分钟后开始，记得按时上课！',
          type: 'course',
          read: false,
          created_at: new Date().toISOString(),
          data: {
            '课程名称': '高等数学',
            '上课时间': '10:00-11:40',
            '上课地点': '教1-101'
          },
          actions: [
            { id: 1, text: '查看课程表', type: 'primary', action: 'navigate', target: '/timetable' }
          ]
        },
        {
          id: 2,
          title: '点餐提醒',
          content: '您的课程将在1小时后结束，是否需要提前点外卖？',
          type: 'order',
          read: false,
          created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
          data: {
            '课程名称': '大学英语',
            '结束时间': '11:40',
            '推荐餐厅': '学生餐厅'
          },
          actions: [
            { id: 1, text: '去点餐', type: 'primary', action: 'navigate', target: '/foodorder/restaurants' }
          ]
        },
        {
          id: 3,
          title: '订单状态更新',
          content: '您的外卖订单已送达，请及时取餐！',
          type: 'order',
          read: true,
          created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          data: {
            '订单号': '20231204123456',
            '餐厅名称': '学生餐厅',
            '订单金额': '¥15.00'
          },
          actions: [
            { id: 1, text: '查看订单', type: 'primary', action: 'navigate', target: '/foodorder/orders' }
          ]
        },
        {
          id: 4,
          title: '二手交易消息',
          content: '您发布的《高等数学》教材有人咨询，快去查看！',
          type: 'secondhand',
          read: false,
          created_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
          data: {
            '商品名称': '高等数学教材',
            '咨询人': '小明',
            '消息内容': '这本书还在吗？' 
          },
          actions: [
            { id: 1, text: '查看消息', type: 'primary', action: 'navigate', target: '/secondhand/my-products' }
          ]
        },
        {
          id: 5,
          title: '积分变动通知',
          content: '您成功兑换了外卖5元优惠券，扣除500积分！',
          type: 'points',
          read: true,
          created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
          data: {
            '变动类型': '积分兑换',
            '变动积分': '-500',
            '当前积分': '1250'
          },
          actions: [
            { id: 1, text: '查看积分', type: 'primary', action: 'navigate', target: '/settings?tab=points' }
          ]
        },
        {
          id: 6,
          title: '系统通知',
          content: '智能校园生活助手已更新至1.0.0版本，新增了多项功能！',
          type: 'system',
          read: true,
          created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          actions: [
            { id: 1, text: '查看更新日志', type: 'primary', action: 'navigate', target: '/settings?tab=about' }
          ]
        }
      ]
    }
  },
  computed: {
    unreadCount() {
      return this.notifications.filter(n => !n.read).length
    },
    unreadNotifications() {
      return this.notifications.filter(n => !n.read).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    },
    selectedCategoryNotifications() {
      if (!this.selectedCategory) {
        return []
      }
      return this.notifications.filter(n => n.type === this.selectedCategory).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  },
  methods: {
    // 获取通知图标
    getNotificationIcon(type) {
      const icons = {
        course: 'el-icon-document',
        order: 'el-icon-shopping-cart-2',
        secondhand: 'el-icon-s-goods',
        points: 'el-icon-medal',
        system: 'el-icon-message'
      }
      return icons[type] || 'el-icon-message'
    },
    
    // 获取通知类型名称
    getNotificationTypeName(type) {
      const typeNames = {
        course: '课程提醒',
        order: '外卖订单',
        secondhand: '二手交易',
        points: '积分变动',
        system: '系统通知'
      }
      return typeNames[type] || '通知'
    },
    
    // 格式化时间
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
      } else if (days < 30) {
        return `${days}天前`
      } else {
        return date.toLocaleDateString()
      }
    },
    
    // 标记为已读
    markAsRead(notification) {
      if (!notification.read) {
        notification.read = true
        this.$message.success('已标记为已读')
      }
    },
    
    // 标记全部为已读
    markAllAsRead() {
      this.notifications.forEach(notification => {
        notification.read = true
      })
      this.$message.success('全部通知已标记为已读')
    },
    
    // 清空所有通知
    clearAllNotifications() {
      this.$confirm('确定要清空所有通知吗？', '确认清空', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.notifications = []
        this.$message.success('所有通知已清空')
      }).catch(() => {
        this.$message.info('已取消清空')
      })
    },
    
    // 处理通知分类选择
    handleCategorySelect(key) {
      this.selectedCategory = key
    },
    
    // 获取某类型通知数量
    getCategoryCount(type) {
      return this.notifications.filter(n => n.type === type).length
    },
    
    // 处理通知操作
    handleAction(action, notification) {
      if (action.action === 'navigate') {
        this.$router.push(action.target)
      } else if (action.action === 'refresh') {
        // 刷新页面或数据
        this.$message.success('刷新成功')
      }
    }
  }
}
</script>

<style scoped>
.notifications-container {
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

.header-actions {
  display: flex;
  gap: 12px;
}

.notifications-tabs {
  margin-top: 20px;
}

.notifications-list {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin-bottom: 16px;
}

.notification-card.unread {
  border-left: 4px solid #409EFF;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
}

.notification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.notification-content {
  padding: 10px 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.notification-type {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: bold;
}

.notification-type.course {
  background: #e6f7ff;
  color: #1890ff;
}

.notification-type.order {
  background: #f6ffed;
  color: #52c41a;
}

.notification-type.secondhand {
  background: #fff7e6;
  color: #fa8c16;
}

.notification-type.points {
  background: #fff0f6;
  color: #eb2f96;
}

.notification-type.system {
  background: #f0f5ff;
  color: #2f54eb;
}

.notification-time {
  font-size: 12px;
  color: #909399;
}

.notification-body h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.notification-body p {
  margin: 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.notification-data {
  margin-top: 12px;
  padding: 12px;
  background: #fafafa;
  border-radius: 4px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
}

.data-item:last-child {
  margin-bottom: 0;
}

.data-label {
  color: #909399;
}

.data-value {
  font-weight: bold;
  color: #333;
}

.notification-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.empty-state {
  margin: 40px 0;
  text-align: center;
}

/* 分类页面样式 */
.category-card {
  display: flex;
  height: 500px;
}

.category-menu {
  width: 200px;
  border-right: 1px solid #eee;
}

.category-content {
  flex: 1;
  padding: 0 20px;
  overflow-y: auto;
}

.category-content .notification-card {
  margin-bottom: 12px;
}

/* 深色模式 */
:deep(.dark-mode) .page-header h2 {
  color: #e0e0e0;
}

:deep(.dark-mode) .notification-card {
  background: #333;
}

:deep(.dark-mode) .notification-body h4 {
  color: #e0e0e0;
}

:deep(.dark-mode) .notification-body p {
  color: #999;
}

:deep(.dark-mode) .data-value {
  color: #e0e0e0;
}

:deep(.dark-mode) .category-menu {
  background: #333;
  border-right-color: #444;
}

:deep(.dark-mode) .category-content {
  background: #333;
}

:deep(.dark-mode) .category-content {
  background: #2c2c2c;
}

:deep(.dark-mode) .notification-card.unread {
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

:deep(.dark-mode) .notification-data {
  background: #444;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .category-card {
    flex-direction: column;
    height: auto;
  }
  
  .category-menu {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #eee;
  }
  
  .category-content {
    padding: 20px 0;
  }
}
</style>