<template>
  <div class="secondhand-messages-container">
    <div class="page-header">
      <h2>二手交易消息</h2>
    </div>
    
    <el-card class="messages-card">
      <div v-if="conversations.length === 0" class="empty-messages">
        <el-empty description="暂无消息"></el-empty>
      </div>
      
      <div v-else class="messages-list">
        <div 
          v-for="conversation in conversations" 
          :key="conversation.id" 
          class="message-item"
          :class="{ 'unread': conversation.unread_count > 0 }"
          @click="goToChatDetail(conversation.id)"
        >
          <div class="message-avatar">
            <el-avatar size="medium">{{ getOtherUser(conversation).charAt(0) }}</el-avatar>
          </div>
          <div class="message-info">
            <div class="message-header">
              <span class="message-user">{{ getOtherUser(conversation) }}</span>
              <span class="message-time">{{ formatTime(conversation.updated_at) }}</span>
            </div>
            <div class="message-content">
              <span class="product-name">{{ conversation.product.name }}</span>
              <span class="last-message">{{ conversation.last_message || '暂无消息' }}</span>
              <el-badge 
                v-if="conversation.unread_count > 0" 
                :value="conversation.unread_count" 
                type="danger" 
                class="unread-badge"
              ></el-badge>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SecondhandMessages',
  data() {
    return {
      conversations: []
    }
  },
  created() {
    this.fetchConversations()
  },
  methods: {
    async fetchConversations() {
      try {
        // 调用后端API获取二手交易相关的对话列表
        const response = await this.$axios.get('/chat/conversations/')
        this.conversations = response.data.results || response.data
      } catch (error) {
        console.error('获取对话列表失败:', error)
        this.$message.error('获取消息列表失败，请稍后重试')
      }
    },
    goToChatDetail(conversationId) {
      this.$router.push(`/chat/${conversationId}`)
    },
    getOtherUser(conversation) {
      // 获取当前用户
      const currentUser = this.$store.state.user?.username || ''
      
      // 确定对方用户
      return conversation.buyer?.username === currentUser ? conversation.seller?.username : conversation.buyer?.username || '未知用户'
    },
    formatTime(time) {
      return new Date(time).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.secondhand-messages-container {
  padding: 0;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.messages-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.empty-messages {
  padding: 50px 0;
}

.messages-list {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.message-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.message-item:hover {
  background-color: #f5f7fa;
}

.message-item.unread {
  background-color: #f0f9ff;
  font-weight: bold;
}

.message-avatar {
  margin-right: 15px;
}

.message-info {
  flex: 1;
  overflow: hidden;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.message-user {
  font-weight: bold;
  font-size: 16px;
  color: #333;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #666;
}

.product-name {
  font-weight: bold;
  color: #409eff;
  margin-right: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.last-message {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 10px;
}

.unread-badge {
  margin-left: 10px;
}

/* 深色模式适配 */
:deep(.dark-mode) .page-header h2 {
  color: #e0e0e0;
}

:deep(.dark-mode) .message-user {
  color: #e0e0e0;
}

:deep(.dark-mode) .message-item:hover {
  background-color: #3a3a3a;
}

:deep(.dark-mode) .message-item.unread {
  background-color: #2a3a4a;
}

:deep(.dark-mode) .product-name {
  color: #66b1ff;
}
</style>