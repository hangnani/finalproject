<template>
  <div class="foodorder-order-detail-container">
    <div class="order-detail-header">
      <el-button icon="el-icon-back" @click="$router.go(-1)">返回</el-button>
      <h2>订单详情</h2>
    </div>
    
    <div class="order-detail-content">
      <el-card class="order-info-card">
        <div slot="header" class="clearfix">
          <span>订单信息</span>
        </div>
        <div class="order-info">
          <div class="info-item">
            <label>订单号：</label>
            <span>{{ order.id }}</span>
          </div>
          <div class="info-item">
            <label>下单时间：</label>
            <span>{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="info-item">
            <label>订单状态：</label>
            <span class="order-status" :class="getStatusClass(order.status)">{{ getStatusText(order.status) }}</span>
          </div>
          <div class="info-item">
            <label>支付方式：</label>
            <span>{{ getPaymentMethodText(order.payment_method) }}</span>
          </div>
          <div class="info-item">
            <label>配送地址：</label>
            <span>{{ order.delivery_address }}</span>
          </div>
        </div>
      </el-card>
      
      <el-card class="restaurant-info-card">
        <div slot="header" class="clearfix">
          <span>餐厅信息</span>
        </div>
        <div class="restaurant-info">
          <h3>{{ order.restaurant.name }}</h3>
          <p>{{ order.restaurant.location }}</p>
          <p>{{ order.restaurant.opening_hours }}</p>
        </div>
      </el-card>
      
      <el-card class="order-items-card">
        <div slot="header" class="clearfix">
          <span>商品信息</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <div class="item-info">
              <div class="item-name">{{ item.dish.name }}</div>
              <div class="item-desc">{{ item.dish.description }}</div>
            </div>
            <div class="item-quantity">x{{ item.quantity }}</div>
            <div class="item-price">¥{{ (item.price * item.quantity).toFixed(2) }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="order-total-card">
        <div slot="header" class="clearfix">
          <span>订单总计</span>
        </div>
        <div class="order-total">
          <div class="total-item">
            <label>商品总价：</label>
            <span>¥{{ order.total_price.toFixed(2) }}</span>
          </div>
          <div class="total-item">
            <label>配送费：</label>
            <span>¥0.00</span>
          </div>
          <div class="total-item total-amount">
            <label>实付金额：</label>
            <span>¥{{ order.total_price.toFixed(2) }}</span>
          </div>
        </div>
      </el-card>
      
      <!-- 评价部分 -->
      <el-card v-if="order.status === 4" class="order-review-card">
        <div slot="header" class="clearfix">
          <span>订单评价</span>
        </div>
        <div v-if="order.review" class="order-review">
          <div class="review-rating">
            <el-rate
              v-model="order.review.rating"
              disabled
              :max="5"
              show-score
              text-color="#ff9900"
              score-template="{value}"
            ></el-rate>
          </div>
          <div class="review-content">{{ order.review.content }}</div>
          <div class="review-time">{{ formatDate(order.review.created_at) }}</div>
        </div>
        <div v-else class="review-form">
          <el-form :model="reviewForm" :rules="reviewRules" ref="reviewForm">
            <el-form-item label="评分" prop="rating">
              <el-rate
                v-model="reviewForm.rating"
                :max="5"
                show-score
                text-color="#ff9900"
                score-template="{value}"
              ></el-rate>
            </el-form-item>
            <el-form-item label="评价内容" prop="content">
              <el-input
                v-model="reviewForm.content"
                type="textarea"
                :rows="4"
                placeholder="请输入您的评价"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitReview">提交评价</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      
      <!-- 操作按钮 -->
      <div class="order-actions">
        <el-button
          v-if="order.status === 0"
          type="primary"
          @click="payOrder"
        >
          立即支付
        </el-button>
        <el-button
          v-if="order.status === 1"
          type="danger"
          @click="cancelOrder"
        >
          取消订单
        </el-button>
        <el-button
          v-if="order.status === 4"
          type="success"
          @click="confirmReceipt"
        >
          确认收货
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodorderOrderDetail',
  data() {
    return {
      orderId: this.$route.params.id,
      order: {
        // 模拟数据
        id: 1,
        restaurant: { name: '学生餐厅', location: '学生食堂一楼', opening_hours: '06:30-22:00' },
        total_price: 52.00,
        status: 4,
        payment_method: 0,
        delivery_address: '学生宿舍1号楼302室',
        created_at: '2024-11-27T12:30:00',
        items: [
          { id: 1, dish: { name: '宫保鸡丁', description: '经典川菜', price: 18.00 }, quantity: 2 },
          { id: 2, dish: { name: '鱼香肉丝', description: '酸甜可口', price: 16.00 }, quantity: 1 }
        ],
        review: null
      },
      reviewForm: {
        rating: 5,
        content: ''
      },
      reviewRules: {
        rating: [
          { required: true, message: '请选择评分', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入评价内容', trigger: 'blur' },
          { min: 10, max: 500, message: '评价内容长度在 10 到 500 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.getOrderDetail()
  },
  methods: {
    getOrderDetail() {
      // 这里应该调用API获取订单详情
      // 目前使用模拟数据
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
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
    getPaymentMethodText(method) {
      const methodMap = {
        0: '微信支付',
        1: '支付宝',
        2: '校园卡'
      }
      return methodMap[method] || '未知支付方式'
    },
    payOrder() {
      // 支付逻辑
      this.$message.success('支付成功')
    },
    cancelOrder() {
      this.$confirm('确定要取消这个订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('订单已取消')
        this.order.status = 5
      }).catch(() => {
        this.$message.info('已取消操作')
      })
    },
    confirmReceipt() {
      this.$confirm('确定已收到商品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        this.$message.success('确认收货成功')
      }).catch(() => {
        this.$message.info('已取消操作')
      })
    },
    submitReview() {
      this.$refs.reviewForm.validate((valid) => {
        if (valid) {
          // 提交评价逻辑
          this.$message.success('评价成功')
          this.order.review = {
            id: Date.now(),
            rating: this.reviewForm.rating,
            content: this.reviewForm.content,
            created_at: new Date().toISOString()
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.foodorder-order-detail-container {
  padding: 20px;
}

.order-detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.order-detail-header h2 {
  margin: 0 0 0 20px;
}

.order-detail-content {
  max-width: 800px;
}

.order-info-card,
.restaurant-info-card,
.order-items-card,
.order-total-card,
.order-review-card {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  margin-bottom: 10px;
}

.info-item label {
  width: 100px;
  font-weight: bold;
  color: #606266;
}

.info-item span {
  color: #303133;
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

.restaurant-info h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.restaurant-info p {
  margin: 5px 0;
  color: #606266;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.order-item:last-child {
  border-bottom: none;
}

.item-info {
  flex: 1;
}

.item-name {
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.item-desc {
  color: #909399;
  font-size: 14px;
}

.item-quantity {
  margin: 0 20px;
  color: #606266;
}

.item-price {
  font-weight: bold;
  color: #f56c6c;
}

.order-total {
  padding: 10px 0;
}

.total-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: #606266;
}

.total-amount {
  font-weight: bold;
  color: #303133;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.total-amount span {
  color: #f56c6c;
  font-size: 18px;
}

.order-review {
  padding: 20px 0;
}

.review-rating {
  margin-bottom: 15px;
}

.review-content {
  margin-bottom: 10px;
  line-height: 1.6;
  color: #303133;
}

.review-time {
  color: #909399;
  font-size: 14px;
  text-align: right;
}

.review-form {
  padding: 20px 0;
}

.order-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
}
</style>