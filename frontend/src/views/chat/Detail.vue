<template>
  <div class="chat-detail-container">
    <div class="page-header">
      <el-button icon="el-icon-back" @click="goBack"></el-button>
      <h2>{{ chatUser }}</h2>
    </div>
    
    <div class="chat-detail-content">
      <!-- 消息列表 -->
      <div class="message-list" ref="messageList">
        <div v-for="message in messages" :key="message.id" class="message-item">
          <div 
            :class="[
              'message-bubble',
              message.sender === currentUser ? 'message-sent' : 'message-received'
            ]"
          >
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.created_at) }}</div>
          </div>
        </div>
      </div>
      
      <!-- 消息输入区域 -->
      <div class="message-input-area">
        <el-input
          v-model="newMessage"
          type="textarea"
          :rows="3"
          placeholder="请输入消息"
          resize="none"
          @keyup.enter.native="sendMessage"
        ></el-input>
        <div class="message-actions">
          <el-button type="primary" @click="sendMessage">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatDetail',
  data() {
    return {
      messages: [],
      newMessage: '',
      chatUser: '卖家',
      currentUser: null,
      conversationId: null
    }
  },
  created() {
    this.conversationId = this.$route.params.id
    this.getCurrentUser()
    this.fetchMessages()
  },
  methods: {
    async getCurrentUser() {
      // 获取当前登录用户信息
      this.currentUser = this.$store.state.user?.username || 'user'
    },
    
    async fetchMessages() {
      try {
        const response = await this.$axios.get(`/chat/conversations/${this.conversationId}/messages/`)
        this.messages = response.data.results || response.data
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        console.error('获取消息列表失败:', error)
        this.$message.error('获取消息列表失败，请稍后重试')
      }
    },
    
    async sendMessage() {
      if (!this.newMessage.trim()) return
      
      try {
        const messageData = {
          content: this.newMessage.trim(),
          message_type: 0 // 文本消息
        }
        
        const response = await this.$axios.post(`/chat/conversations/${this.conversationId}/messages/`, messageData)
        
        // 添加新消息到列表
        this.messages.push(response.data)
        this.newMessage = ''
        
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        console.error('发送消息失败:', error)
        this.$message.error('发送消息失败，请稍后重试')
      }
    },
    
    scrollToBottom() {
      // 滚动到底部
      const messageList = this.$refs.messageList
      if (messageList) {
        messageList.scrollTop = messageList.scrollHeight
      }
    },
    
    goBack() {
      this.$router.go(-1)
    },
    
    formatTime(time) {
      if (!time) {
        return ''
      }
      
      try {
        const date = new Date(time)
        if (isNaN(date.getTime())) {
          return ''
        }
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        console.error('格式化时间失败:', error)
        return ''
      }
    }
  }
}
</script>

<style scoped>
.chat-detail-container {
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
  border-bottom: 1px solid #ebeef5;
}

.page-header h2 {
  margin: 0 10px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.chat-detail-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 20px 20px;
  overflow: hidden;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.message-item {
  margin-bottom: 15px;
  display: flex;
  justify-content: flex-start;
}

.message-item.message-sent {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 15px;
  border-radius: 8px;
  position: relative;
  word-wrap: break-word;
  word-break: break-word;
}

.message-received {
  background-color: #f5f7fa;
  border: 1px solid #ebeef5;
  border-top-left-radius: 0;
}

.message-sent {
  background-color: #409eff;
  color: white;
  border-top-right-radius: 0;
}

.message-content {
  margin-bottom: 5px;
  line-height: 1.5;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  text-align: right;
}

.message-input-area {
  margin-top: 15px;
}

.message-actions {
  text-align: right;
  margin-top: 10px;
}

.message-actions .el-button {
  width: 100px;
}
</style>