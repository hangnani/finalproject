<template>
  <div class="foodorder-orders-container">
    <h2>我的订单</h2>
    
    <div class="orders-content">
      <div class="order-tabs">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="全部订单" name="all"></el-tab-pane>
          <el-tab-pane label="待支付" name="0"></el-tab-pane>
          <el-tab-pane label="已支付" name="1"></el-tab-pane>
          <el-tab-pane label="已接单" name="2"></el-tab-pane>
          <el-tab-pane label="配送中" name="3"></el-tab-pane>
          <el-tab-pane label="已完成" name="4"></el-tab-pane>
          <el-tab-pane label="已取消" name="5"></el-tab-pane>
        </el-tabs>
      </div>
      
      <div class="order-list">
        <el-card
          v-for="order in filteredOrders"
          :key="order.id"
          class="order-card"
          @click="goToOrderDetail(order.id)"
        >
          <div class="order-header">
            <div class="order-info">
              <span class="order-id">订单号：{{ order.id }}</span>
              <span class="order-time">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="order-status" :class="getStatusClass(order.status)">
              {{ getStatusText(order.status) }}
            </div>
          </div>
          
          <div class="order-restaurant">{{ order.restaurant.name }}</div>
          
          <div class="order-items">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <span class="item-name">{{ item.dish.name }}</span>
              <span class="item-quantity">x{{ item.quantity }}</span>
              <span class="item-price">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
          </div>
          
          <div class="order-footer">
            <div class="order-total">
              共{{ getTotalItems(order) }}件商品 总计：
              <span class="total-price">¥{{ order.total_price.toFixed(2) }}</span>
            </div>
            <div class="order-actions">
              <el-button
                v-if="order.status === 0"
                type="primary"
                size="small"
                @click.stop="payOrder(order.id)"
              >
                立即支付
              </el-button>
              <el-button
                v-if="order.status === 1"
                type="danger"
                size="small"
                @click.stop="cancelOrder(order.id)"
              >
                取消订单
              </el-button>
              <el-button
                v-if="order.status === 4 && !order.review"
                type="primary"
                size="small"
                @click.stop="reviewOrder(order.id)"
              >
                去评价
              </el-button>
              <el-button
                v-if="order.status === 4"
                type="default"
                size="small"
                @click.stop="goToOrderDetail(order.id)"
              >
                查看详情
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
      
      <div v-if="filteredOrders.length === 0" class="empty-state">
        <el-empty description="暂无订单数据"></el-empty>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodorderOrders',
  data() {
    return {
      activeTab: 'all',
      orders: [
        // 模拟数据
        {
          id: 1,
          restaurant: { name: '学生餐厅' },
          total_price: 52.00,
          status: 4,
          created_at: '2024-11-27T12:30:00',
          items: [
            { id: 1, dish: { name: '宫保鸡丁' }, quantity: 2, price: 18.00 },
            { id: 2, dish: { name: '鱼香肉丝' }, quantity: 1, price: 16.00 }
          ],
          review: null
        },
        {
          id: 2,
          restaurant: { name: '教工餐厅' },
          total_price: 38.00,
          status: 3,
          created_at: '2024-11-27T18:15:00',
          items: [
            { id: 3, dish: { name: '红烧肉' }, quantity: 1, price: 28.00 },
            { id: 4, dish: { name: '青菜汤' }, quantity: 1, price: 10.00 }
          ],
          review: null
        }
      ]
    }
  },
  computed: {
    filteredOrders() {
      if (this.activeTab === 'all') {
        return this.orders
      }
      return this.orders.filter(order => order.status.toString() === this.activeTab)
    }
  },
  methods: {
    handleTabClick(tab) {
      this.activeTab = tab.name
    },
    getStatusText(status) {
      const statusMap = {
        0: '待支付',
        1: '已支付',
        2: '已接单',
        3: '配送中',
        4: '已完成',
        5: '已取消'
      }
      return statusMap[status] || '未知状态'
    },
    getStatusClass(status) {
      const classMap = {
        0: 'status-waiting',
        1: 'status-paid',
        2: 'status-accepted',
        3: 'status-delivering',
        4: 'status-completed',
        5: 'status-cancelled'
      }
      return classMap[status] || ''
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    },
    getTotalItems(order) {
      return order.items.reduce((total, item) => total + item.quantity, 0)
    },
    goToOrderDetail(orderId) {
      this.$router.push(`/foodorder/order/${orderId}`)
    },
    payOrder(orderId) {
      // 这里应该调用支付API
      this.$message.success('支付成功')
      // 更新订单状态
      const order = this.orders.find(o => o.id === orderId)
      if (order) {
        order.status = 1
      }
    },
    cancelOrder(orderId) {
      this.$confirm('确定要取消这个订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用取消订单API
        this.$message.success('订单已取消')
        // 更新订单状态
        const order = this.orders.find(o => o.id === orderId)
        if (order) {
          order.status = 5
        }
      }).catch(() => {
        this.$message.info('已取消操作')
      })
    },
    reviewOrder(orderId) {
      // 这里应该跳转到评价页面，目前直接模拟评价
      this.$message.success('评价成功')
      // 更新订单评价状态
      const order = this.orders.find(o => o.id === orderId)
      if (order) {
        order.review = { id: Date.now(), rating: 5, content: '非常满意' }
      }
    }
  }
}
</script>

<style scoped>
.foodorder-orders-container {
  padding: 20px;
}

.orders-content {
  max-width: 1000px;
}

.order-tabs {
  margin-bottom: 20px;
}

.order-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.order-info {
  display: flex;
  gap: 20px;
  color: #606266;
  font-size: 14px;
}

.order-status {
  font-weight: bold;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.status-waiting {
  background: #e6f7ff;
  color: #1890ff;
}

.status-paid {
  background: #f0f9eb;
  color: #67c23a;
}

.status-accepted {
  background: #fdf6ec;
  color: #e6a23c;
}

.status-delivering {
  background: #f0f9eb;
  color: #67c23a;
}

.status-completed {
  background: #f0f0f0;
  color: #909399;
}

.status-cancelled {
  background: #fef0f0;
  color: #f56c6c;
}

.order-restaurant {
  font-weight: bold;
  margin-bottom: 10px;
  color: #303133;
}

.order-items {
  margin-bottom: 15px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  color: #606266;
  font-size: 14px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.order-total {
  color: #606266;
  font-size: 14px;
}

.total-price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 16px;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.empty-state {
  margin: 50px 0;
  text-align: center;
}
</style>