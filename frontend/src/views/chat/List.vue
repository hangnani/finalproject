<template>
  <div class="chat-list-container">
    <div class="page-header">
      <h2>消息中心</h2>
    </div>
    
    <div class="chat-list-content">
      <!-- 聊天列表 -->
      <div class="chat-list">
        <div v-if="conversations.length === 0" class="empty-state">
          <el-empty description="暂无消息"></el-empty>
        </div>
        
        <div 
          v-for="conversation in conversations" 
          :key="conversation.id" 
          class="chat-item"
          :class="{ 'unread': conversation.has_unread }"
          @click="goToChatDetail(conversation.id)"
        >
          <div class="chat-avatar">
            <el-avatar size="medium">{{ getOtherUser(conversation).charAt(0) }}</el-avatar>
          </div>
          <div class="chat-info">
            <div class="chat-header">
              <span class="chat-name">{{ getOtherUser(conversation) }}</span>
              <span class="chat-time">{{ formatTime(conversation.updated_at) }}</span>
            </div>
            <div class="chat-last-message">
              <span>{{ conversation.last_message }}</span>
              <el-badge v-if="conversation.unread_count > 0" :value="conversation.unread_count" type="danger" class="unread-badge"></el-badge>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatList',
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
      // 根据当前登录用户判断对方用户名
      const currentUser = this.$store.state.user?.username || ''
      // 这里假设conversation中有seller和buyer字段
      // 实际情况需要根据后端返回的数据结构调整
      return currentUser === conversation.seller ? conversation.buyer : conversation.seller || '卖家'
    },
    formatTime(time) {
      return new Date(time).toLocaleString()
    }
  }
}
</script>

<style scoped>
.chat-list-container {
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

.chat-list-content {
  display: flex;
  height: calc(100vh - 120px);
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  border-right: 1px solid #ebeef5;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid #f0f0f0;
}

.chat-item:hover {
  background-color: #f5f7fa;
}

.chat-item.unread {
  background-color: #f0f9ff;
}

.chat-avatar {
  margin-right: 15px;
}

.chat-info {
  flex: 1;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.chat-name {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.chat-time {
  font-size: 12px;
  color: #909399;
}

.chat-last-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.unread-badge {
  margin-left: 10px;
}

.empty-state {
  padding: 50px 0;
}
</style>