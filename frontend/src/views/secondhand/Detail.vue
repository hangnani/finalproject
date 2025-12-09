<template>
  <div class="secondhand-detail-container">
    <h2>商品详情</h2>
    <el-card>
      <div v-if="product" class="product-detail">
        <div class="product-header">
          <h3>{{ product.name }}</h3>
          <span class="product-price">¥{{ parseFloat(product.price).toFixed(2) }}</span>
        </div>
        <div class="product-info">
          <div class="product-basic-info">
            <p><strong>状态：</strong>{{ product.status === 0 ? '在售' : '已售出' }}</p>
            <p><strong>发布时间：</strong>{{ formatTime(product.created_at) }}</p>
            <p><strong>联系方式：</strong>{{ product.contact }}</p>
            <p v-if="product.user"><strong>发布者：</strong>{{ product.user.username }}</p>
          </div>
          <div class="product-description">
            <h4>商品描述</h4>
            <p>{{ product.description }}</p>
          </div>
        </div>
        <div class="product-actions">
          <el-button type="primary" @click="addToFavorite(product.id)">收藏</el-button>
          <!-- 只有当商品发布者不是当前用户时，才显示联系卖家按钮 -->
          <el-button 
            v-if="product.user && product.user.username !== currentUser" 
            type="success" 
            @click="contactSeller(product.contact)"
          >
            联系卖家
          </el-button>
        </div>
      </div>
      <div v-else class="loading">
        <i class="el-icon-loading"></i>
        <span>加载中...</span>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'SecondhandDetail',
  data() {
    return {
      product: null,
      currentUser: null
    }
  },
  created() {
    // 获取当前登录用户
    this.getCurrentUser()
    // 获取商品详情
    this.getProductDetail()
  },
  methods: {
    getCurrentUser() {
      // 从Vuex或localStorage获取当前登录用户
      if (this.$store.state.user) {
        this.currentUser = this.$store.state.user.username
      } else {
        // 从localStorage获取用户信息
        const userStr = localStorage.getItem('user')
        if (userStr) {
          try {
            const user = JSON.parse(userStr)
            this.currentUser = user.username
          } catch (e) {
            console.error('解析用户信息失败:', e)
          }
        }
      }
    },
    async getProductDetail() {
      try {
        const productId = this.$route.params.id
        
        // 检查是否是模拟商品ID（9991-9996）
        const mockProductIds = ['9991', '9992', '9993', '9994', '9995', '9996']
        
        if (mockProductIds.includes(productId)) {
          // 模拟商品，使用前端模拟数据
          const mockProducts = [
            {
              id: 9991,
              name: '《Python编程从入门到精通》',
              price: 29.99,
              status: 0,
              created_at: '2025-11-27T10:30:00',
              image: 'https://picsum.photos/200/150?random=1',
              seller: 'ershou1',
              contact: '13800138000',
              description: '全新未拆封，Python编程入门经典书籍，适合零基础学习。'
            },
            {
              id: 9992,
              name: '无线鼠标',
              price: 19.99,
              status: 0,
              created_at: '2025-11-26T14:20:00',
              image: 'https://picsum.photos/200/150?random=2',
              seller: 'ershou2',
              contact: '13900139000',
              description: '无线鼠标，电池续航长，灵敏度高，适合办公使用。'
            },
            {
              id: 9993,
              name: '机械键盘',
              price: 89.99,
              status: 1,
              created_at: '2025-11-25T09:15:00',
              image: 'https://picsum.photos/200/150?random=3',
              seller: 'ershou3',
              contact: '13700137000',
              description: '机械键盘，青轴，手感好，适合游戏和打字。'
            },
            {
              id: 9994,
              name: '蓝牙耳机',
              price: 49.99,
              status: 0,
              created_at: '2025-11-24T16:45:00',
              image: 'https://picsum.photos/200/150?random=4',
              seller: 'ershou1',
              contact: '13600136000',
              description: '蓝牙耳机，音质清晰，佩戴舒适，适合运动使用。'
            },
            {
              id: 9995,
              name: '充电宝',
              price: 39.99,
              status: 0,
              created_at: '2025-11-23T11:20:00',
              image: 'https://picsum.photos/200/150?random=5',
              seller: 'ershou2',
              contact: '13500135000',
              description: '充电宝，容量大，充电速度快，适合外出使用。'
            },
            {
              id: 9996,
              name: '台灯',
              price: 24.99,
              status: 0,
              created_at: '2025-11-22T18:30:00',
              image: 'https://picsum.photos/200/150?random=6',
              seller: 'ershou3',
              contact: '13400134000',
              description: '台灯，可调节亮度，保护视力，适合学生使用。'
            }
          ]
          
          // 查找对应的模拟商品
          const mockProduct = mockProducts.find(p => p.id === parseInt(productId))
          if (mockProduct) {
            // 将seller字段转换为user对象，与API返回的数据结构保持一致
            const sellerMap = {
              'ershou1': 4,
              'ershou2': 5,
              'ershou3': 6
            }
            mockProduct.user = {
              id: sellerMap[mockProduct.seller] || 0,
              username: mockProduct.seller
            }
            this.product = mockProduct
          } else {
            throw new Error('未找到模拟商品')
          }
        } else {
          // 真实商品，从后端获取数据
          const response = await this.$axios.get(`/secondhand/products/${productId}/`)
          this.product = response.data
        }
      } catch (error) {
        console.error('获取商品详情失败:', error)
        this.$message.error('获取商品详情失败，请稍后重试')
      }
    },
    addToFavorite() {
      this.$message.success('收藏成功！')
    },
    async contactSeller() {
      try {
        // 添加详细调试信息
        console.log('=== 开始创建对话 ===')
        
        // 检查登录状态
        const token = localStorage.getItem('token')
        const userStr = localStorage.getItem('user')
        console.log('登录状态 - token:', token ? '已存在' : '不存在')
        console.log('登录状态 - user:', userStr ? '已存在' : '不存在')
        
        if (!token || !userStr) {
          this.$message.warning('请先登录')
          this.$router.push('/login')
          return
        }
        
        // 解析用户信息
        const user = JSON.parse(userStr)
        console.log('当前用户:', user)
        
        // 检查商品信息
        console.log('商品信息:', this.product)
        console.log('商品ID:', this.product.id)
        console.log('卖家ID:', this.product.user.id)
        
        // 检查是否是模拟商品（ID：9991-9996）
        const isMockProduct = this.product.id >= 9991 && this.product.id <= 9996
        console.log('是否模拟商品:', isMockProduct)
        
        if (isMockProduct) {
          // 模拟商品，使用前端模拟数据
          console.log('模拟商品，跳过API调用，模拟创建对话')
          
          // 模拟对话数据
          const mockConversation = {
            id: this.product.id + 10000, // 模拟对话ID
            buyer: user,
            seller: this.product.user,
            product: this.product,
            status: 0,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            last_message: '',
            unread_count: 0,
            messages: []
          }
          
          // 跳转到聊天详情页
          console.log('模拟创建对话成功，对话ID:', mockConversation.id)
          this.$router.push(`/chat/${mockConversation.id}`)
          return
        }
        
        // 真实商品，调用后端API
        // 创建或获取对话
        const apiUrl = '/chat/conversations/'
        console.log('请求URL:', apiUrl)
        
        const requestData = {
          product_id: this.product.id,
          seller_id: this.product.user.id
        }
        console.log('请求参数:', requestData)
        
        // 发送请求
        const response = await this.$axios.post(apiUrl, requestData)
        
        // 检查响应
        console.log('响应状态:', response.status)
        console.log('响应数据:', response.data)
        console.log('响应类型:', typeof response.data)
        
        if (response.data && response.data.id) {
          // 跳转到聊天详情页
          console.log('创建对话成功，对话ID:', response.data.id)
          this.$router.push(`/chat/${response.data.id}`)
        } else {
          console.error('创建对话失败：返回数据无效')
          console.error('数据结构:', Object.keys(response.data || {}))
          throw new Error('创建对话失败：返回数据无效')
        }
      } catch (error) {
        console.error('创建对话失败:', error)
        if (error.response) {
          console.error('错误响应状态:', error.response.status)
          console.error('错误响应数据:', error.response.data)
          console.error('错误响应头:', error.response.headers)
        } else if (error.request) {
          console.error('错误请求:', error.request)
        } else {
          console.error('错误消息:', error.message)
        }
        this.$message.error('创建对话失败，请稍后重试')
      } finally {
        console.log('=== 创建对话结束 ===')
      }
    },
    formatTime(time) {
      return new Date(time).toLocaleString()
    }
  }
}
</script>

<style scoped>
.secondhand-detail-container {
  padding: 0;
}

.product-detail {
  padding: 20px 0;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.product-header h3 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.product-price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
}

.product-info {
  margin-bottom: 20px;
}

.product-basic-info {
  margin-bottom: 20px;
}

.product-basic-info p {
  margin: 10px 0;
  font-size: 16px;
  color: #606266;
}

.product-description h4 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.product-description p {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
}

.product-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 50px 0;
  font-size: 18px;
  color: #909399;
}

.loading .el-icon {
  margin-right: 10px;
  font-size: 24px;
}
</style>