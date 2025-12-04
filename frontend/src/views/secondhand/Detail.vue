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
          </div>
          <div class="product-description">
            <h4>商品描述</h4>
            <p>{{ product.description }}</p>
          </div>
        </div>
        <div class="product-actions">
          <el-button type="primary" @click="addToFavorite(product.id)">收藏</el-button>
          <el-button type="success" @click="contactSeller(product.contact)">联系卖家</el-button>
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
      product: null
    }
  },
  created() {
    this.getProductDetail()
  },
  methods: {
    async getProductDetail() {
      try {
        const productId = this.$route.params.id
        const response = await this.$axios.get(`/secondhand/products/${productId}/`)
        this.product = response.data
      } catch (error) {
        console.error('获取商品详情失败:', error)
        this.$message.error('获取商品详情失败，请稍后重试')
      }
    },
    addToFavorite(productId) {
      this.$message.success('收藏成功！')
    },
    contactSeller(contact) {
      this.$message.info(`卖家联系方式：${contact}`)
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